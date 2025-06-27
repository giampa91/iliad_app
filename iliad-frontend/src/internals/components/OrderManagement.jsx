import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  FormControl,
  OutlinedInput,
  TextField,
  Typography,
  InputAdornment,
} from '@mui/material';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';

import OrderDetailDialog from './OrderDetailDialog';
import OrdersDataGrid from './OrdersDataGrid';

// API base URL constant
const API_BASE_URL = 'http://localhost:8000/api/orders/';

function OrderManagement() {
  // ------------------------------
  // State
  // ------------------------------
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [productsToDelete, setProductsToDelete] = useState([]);
  const [error, setError] = useState('');

  const [search, setSearch] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [totalOrders, setTotalOrders] = useState(0);

  // ------------------------------
  // Fetch Orders
  // ------------------------------
  useEffect(() => {
    fetchOrders();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, pageSize]);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(API_BASE_URL, {
        params: {
          page: page + 1,
          page_size: pageSize,
          search: search || undefined,
          date_start: dateFrom || undefined,
          date_end: dateTo || undefined,
        },
      });
      setOrders(response.data.results);
      setTotalOrders(response.data.count);
    } catch (err) {
      console.error('Failed to fetch orders:', err);
    }
  };

  // ------------------------------
  // Dialog Handlers
  // ------------------------------
  const openOrderDetail = (order) => {
    setSelectedOrder(order);
    setIsEditing(false);
  };

  const closeOrderDetail = () => {
    setSelectedOrder(null);
    setIsEditing(false);
  };

  // ------------------------------
  // CRUD Operations
  // ------------------------------
  const saveOrder = async (editedOrder) => {
    setError('');

    // Validate products
    for (const product of editedOrder.products) {
      if (!product.name?.trim()) {
        setError('Each product must have a name.');
        return;
      }
      if (product.price == null || product.price <= 0) {
        setError('Each product must have a valid price greater than zero.');
        return;
      }
    }

    try {
      const payload = {
        customer_name: editedOrder.customer_name,
        description: editedOrder.description,
        date: editedOrder.date,
        products: editedOrder.products,
        products_to_delete: productsToDelete,
      };

      let savedOrder;
      if (orders.find((o) => o.id === editedOrder.id)) {
        payload.version = editedOrder.version
        const res = await axios.put(
          API_BASE_URL + editedOrder.id + '/',
          payload
        );
        savedOrder = res.data;
        setOrders((prev) =>
          prev.map((o) => (o.id === savedOrder.id ? savedOrder : o))
        );
      } else {
        const res = await axios.post(API_BASE_URL, payload);
        savedOrder = res.data;
        setOrders((prev) => [...prev, savedOrder]);
      }

      setProductsToDelete([]);
      setSelectedOrder(savedOrder);
      setIsEditing(false);
    } catch (err) {
      if (
        err.response && 
        err.response.status === 400 &&
        Array.isArray(err.response.data) &&
        err.response.data.includes("Order has been modified by another user. Please refresh and try again.")
      ) {
        setError('Please refresh the page: The order was updated by someone else. Please refresh the page and try again.');
      } else {
        setError('Error saving order and products: ' + (err.message || 'Unknown error'));
      }
    }
  };

  const deleteOrder = async (id) => {
    try {
      await axios.delete(API_BASE_URL + id +'/');
      setOrders((prev) => prev.filter((o) => o.id !== id));
      closeOrderDetail();
    } catch (err) {
      console.error('Error deleting order:', err);
    }
  };

  const handleEditOrder = (field, value) => {
    setSelectedOrder((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const addProduct = () => {
    if (!selectedOrder) return;
    const newProduct = { id: null, name: '', price: 0 };
    handleEditOrder('products', [...selectedOrder.products, newProduct]);
  };

  const deleteProduct = (productId) => {
    if (!selectedOrder) return;
    if (typeof productId === 'number') {
      setProductsToDelete((prev) => [...prev, productId]);
    }
    const updatedProducts = selectedOrder.products.filter((p) => p.id !== productId);
    handleEditOrder('products', updatedProducts);
  };

  // ------------------------------
  // Columns
  // ------------------------------
  const columns = [
    { field: 'id', headerName: 'Order ID', width: 130 },
    { field: 'customer_name', headerName: 'Customer', width: 180 },
    { field: 'description', headerName: 'Description', flex: 1, minWidth: 150 },
    { field: 'date', headerName: 'Date', width: 120 },
  ];

  // ------------------------------
  // Render
  // ------------------------------
  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" mb={3}>
        Order Management
      </Typography>

      {/* Filters */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
        <form
          onSubmit={(e) => {
            e.preventDefault(); // prevent full page reload
            setPage(0);
            fetchOrders(); // call your fetch logic
          }}
        >
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
            <FormControl sx={{ flex: '1 1 300px' }}>
              <OutlinedInput
                size="small"
                placeholder="Search by name or description"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                name="search" // ensures it's part of the form
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault(); // prevent duplicate submit
                    setPage(0);
                    fetchOrders();
                  }
                }}
                startAdornment={
                  <InputAdornment position="start">
                    <SearchRoundedIcon />
                  </InputAdornment>
                }
              />
            </FormControl>

            <TextField
              label="Date From"
              type="date"
              size="small"
              InputLabelProps={{ shrink: true }}
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              name="dateFrom"
            />
            <TextField
              label="Date To"
              type="date"
              size="small"
              InputLabelProps={{ shrink: true }}
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              name="dateTo"
            />

            <Button type="submit" variant="contained">
              Search
            </Button>
            <Button
              variant="outlined"
              onClick={() => {
                setSearch('');
                setDateFrom('');
                setDateTo('');
                setPage(0);
              }}
            >
              Clear Filters
            </Button>
          </Box>
        </form>
      </Box>

      {/* Orders Table */}
      <Box sx={{ height: 500, width: '100%' }}>
        <OrdersDataGrid
          orders={orders}
          columns={columns}
          page={page}
          pageSize={pageSize}
          totalOrders={totalOrders}
          setPage={setPage}
          setPageSize={setPageSize}
          openOrderDetail={openOrderDetail}
        />
      </Box>

      {/* Detail Dialog */}
      <OrderDetailDialog
        selectedOrder={selectedOrder}
        isEditing={isEditing}
        error={error}
        closeOrderDetail={closeOrderDetail}
        setIsEditing={setIsEditing}
        handleEditChange={handleEditOrder}
        addProduct={addProduct}
        deleteProduct={deleteProduct}
        saveOrder={saveOrder}
        deleteOrder={deleteOrder}
      />
    </Box>
  );
}

export default OrderManagement;
