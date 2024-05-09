import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import CircularProgress from '@mui/material/CircularProgress';

export default function Loading() {
  return (
    <Box marginTop={15} sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
      <Button startdecorator={<CircularProgress variant="indeterminate" thickness={2} />}>Loading...</Button>
      <IconButton>
        <CircularProgress thickness={2} />
      </IconButton>
    </Box>
  );
}
