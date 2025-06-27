import * as React from 'react';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import OrderManagement from '../internals/components/OrderManagement';

export default function MainGrid() {
  return (
    <Box sx={{ width: '100%', maxWidth: { sm: '100%', md: '1700px' } }}>
      <Grid >
        <OrderManagement />
      </Grid>
    </Box>
  );
}
