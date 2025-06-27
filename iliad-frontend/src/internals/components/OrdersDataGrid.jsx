import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Typography } from '@mui/material';

export default function OrdersDataGrid({
  orders,
  columns,
  page,
  pageSize,
  totalOrders,
  setPage,
  setPageSize,
  openOrderDetail,
}) {
  return (
    <DataGrid
      rows={orders}
      columns={columns}
      pageSize={pageSize}
      page={page}
      rowCount={totalOrders}
      onRowClick={(params) => openOrderDetail(params.row)}
      paginationMode="server"
      paginationModel={{ page, pageSize }}
      onPaginationModelChange={({ page, pageSize }) => {
        const maxPage = Math.floor((totalOrders - 1) / pageSize);
        if (page > maxPage) {
          setPage(maxPage); // prevent going beyond last valid page
        } else {
          setPage(page);
        }
        setPageSize(pageSize);
      }}
      pageSizeOptions={[1, 2, 5, 10, 25, 50, 100]}
      components={{
        NoRowsOverlay: () => (
          <Typography
            sx={{ mt: 2, textAlign: 'center', width: '100%' }}
            variant="subtitle1"
          >
            No orders match the criteria.
          </Typography>
        ),
      }}
      disableRowSelectionOnClick
      keepNonExistentRowsSelected
      getRowId={(row) => row.id}
    />
  );
}
