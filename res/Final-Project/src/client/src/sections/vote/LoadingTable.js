import * as React from 'react';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';

export default function LoadingTable() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Box sx={{ width: '75%', marginTop: 20 }}>
        <LinearProgress />
      </Box>
    </div>
  );
}
