import React from 'react';
import { useEffect } from 'react';
import PropTypes from 'prop-types';
import { Grid } from '@mui/material';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

// The design of the information card modal
const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '550px',
  height: '250px',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 20,
  p: 4,
  overflowY: 'auto',
};

// The background color of the buttons
const colorBg = [
  'rgb(100, 181, 246, 0.15)',
  'rgb(100, 181, 246, 0.35)',
  'rgb(100, 181, 246, 0.55)',
  'rgb(100, 181, 246, 0.75)',
];

export default function InfoCards(props) {
  const [open, setOpen] = React.useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <div>
      <Grid container spacing={3}>
        <Button
          id={props.index}
          xs={12}
          sm={6}
          md={3}
          sx={{
            ...props.styleCards,
            marginTop: { xs: 2, sm: 2 },
            backgroundColor: colorBg[props.index % 4],
          }}
          onClick={handleOpen}
        >
          {props.keys}
        </Button>
      </Grid>

      <Modal
        keepMounted
        open={open}
        onClose={handleClose}
        aria-labelledby="keep-mounted-modal-title"
        aria-describedby="keep-mounted-modal-description"
        lang="he"
      >
        <Box sx={style}>
          <Typography
            id="keep-mounted-modal-title"
            variant="h3"
            component="h2"
            sx={{ marginTop: '-15px', textAlign: 'center', color: 'rgb(10, 88, 202, 1)' }}
            dir="rtl"
          >
            {props.keys}
          </Typography>
          <Typography
            id="keep-mounted-modal-description"
            sx={{ mt: 1, textAlign: 'right', color: 'rgb(13, 71, 161, 0.8)' }}
            dir="rtl"
          >
            {props.value}
          </Typography>
          <button
            type="button"
            id={`close-button${props.index}`}
            onClick={handleClose}
            style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              padding: '5px 10px',
              backgroundColor: '#2196f3',
              color: '#fff',
              border: 'none',
              borderRadius: '50%',
              cursor: 'pointer',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
            }}
          >
            X
          </button>
        </Box>
      </Modal>
    </div>
  );
}

InfoCards.propTypes = {
  keys: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  styleCards: PropTypes.object.isRequired,
};
