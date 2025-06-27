import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Typography,
  Box,
  FormControl,
  Alert,
} from '@mui/material';
import {
  Save as SaveIcon,
  Cancel as CancelIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { format, parseISO } from 'date-fns';

export default function OrderDetailDialog({
  selectedOrder,
  isEditing,
  error,
  closeOrderDetail,
  setIsEditing,
  handleEditChange,
  addProduct,
  deleteProduct,
  saveOrder,
  deleteOrder,
}) {
  if (!selectedOrder) return null;

  const formatDate = (date) =>
    date ? new Date(date).toISOString().slice(0, 10) : '';

  return (
    <Dialog
      open
      onClose={closeOrderDetail}
      maxWidth="sm"
      fullWidth
      aria-labelledby="order-detail-dialog"
    >
      <DialogTitle id="order-detail-dialog">
        Order Details – {selectedOrder.id}
      </DialogTitle>

      <DialogContent dividers>
        {isEditing ? (
          <>
            <TextField
              label="Customer Name"
              fullWidth
              margin="normal"
              value={selectedOrder.customer_name}
              onChange={(e) =>
                handleEditChange('customer_name', e.target.value)
              }
            />

            <TextField
              label="Description"
              fullWidth
              multiline
              margin="normal"
              value={selectedOrder.description}
              onChange={(e) =>
                handleEditChange('description', e.target.value)
              }
              error={!!error?.description}
              helperText={error?.description || ''}
            />

            <FormControl fullWidth margin="normal" />

            <TextField
              label="Date"
              type="date"
              fullWidth
              margin="normal"
              value={formatDate(selectedOrder.date)}
              InputLabelProps={{ shrink: true }}
              onChange={(e) => handleEditChange('date', e.target.value)}
            />

            <Typography variant="subtitle1" mt={2} mb={1}>
              Products
            </Typography>

            {selectedOrder.products.map((product, idx) => (
              <Box key={product.id} sx={{ display: 'flex', gap: 1, mb: 1 }}>
                <TextField
                  label="Name"
                  size="small"
                  value={product.name}
                  onChange={(e) => {
                    const products = [...selectedOrder.products];
                    products[idx].name = e.target.value;
                    handleEditChange('products', products);
                  }}
                  sx={{ flexGrow: 1 }}
                />
                <TextField
                  label="Price"
                  type="number"
                  size="small"
                  inputProps={{ min: 0, step: 0.01 }}
                  value={product.price}
                  onChange={(e) => {
                    const products = [...selectedOrder.products];
                    products[idx].price = parseFloat(e.target.value) || 0;
                    handleEditChange('products', products);
                  }}
                  sx={{ width: 120 }}
                />
                <Button
                  color="error"
                  size="small"
                  onClick={() => deleteProduct(product.id)}
                  sx={{ minWidth: 'auto', p: '6px' }}
                  aria-label={`Delete product ${product.name}`}
                >
                  <DeleteIcon fontSize="small" />
                </Button>
              </Box>
            ))}

            <Button
              variant="outlined"
              onClick={addProduct}
              sx={{ mt: 1, mb: 2 }}
            >
              Add Product
            </Button>
          </>
        ) : (
          <>
            <Typography>
              <strong>Customer:</strong> {selectedOrder.customer_name}
            </Typography>
            <Typography sx={{ mt: 1 }}>
              <strong>Description:</strong> {selectedOrder.description}
            </Typography>
            <Typography variant="body1" gutterBottom>
              Date:{' '}
              {selectedOrder.date
                ? format(parseISO(selectedOrder.date), 'PPP')
                : 'N/A'}
            </Typography>

            <Typography variant="subtitle1" mt={2} mb={1}>
              Products
            </Typography>
            <Box sx={{ pl: 2 }}>
              {selectedOrder.products.map((product) => (
                <Typography
                  key={product.id}
                  variant="body2"
                  color="textPrimary"
                  gutterBottom
                >
                  • {product.name} — Price: € {product.price}
                </Typography>
              ))}
            </Box>
          </>
        )}
      </DialogContent>

      <DialogActions>
        {isEditing ? (
          <>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <Button
              startIcon={<SaveIcon />}
              onClick={() => saveOrder(selectedOrder)}
              variant="contained"
              color="primary"
            >
              Save
            </Button>
            <Button
              startIcon={<CancelIcon />}
              onClick={() => setIsEditing(false)}
              variant="outlined"
            >
              Cancel
            </Button>
          </>
        ) : (
          <>
            <Button
              startIcon={<EditIcon />}
              onClick={() => setIsEditing(true)}
              variant="contained"
            >
              Edit
            </Button>
            <Button
              startIcon={<DeleteIcon />}
              onClick={() => deleteOrder(selectedOrder.id)}
              variant="outlined"
              color="error"
            >
              Delete
            </Button>
            <Button onClick={closeOrderDetail} variant="text">
              Close
            </Button>
          </>
        )}
      </DialogActions>
    </Dialog>
  );
}
