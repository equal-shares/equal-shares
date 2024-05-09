import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
// @mui
import { alpha } from '@mui/material/styles';
import { MenuItem, Avatar, IconButton, Popover } from '@mui/material';
// mocks_
import account from '../../../_mock/account';
import UserContext from '../../../contexts/UserContext';
import AddressContext from '../../../contexts/AddressContext';


export default function AccountPopover() {
  const [open, setOpen] = useState(null);
  const [profilePhoto, setProfilePhoto] = useState('');
  const navigate = useNavigate();
  const id = useContext(UserContext) ?? localStorage.getItem('id') ?? '';
  const address = useContext(AddressContext);
  const url = `${address}home?user_id=${id}`;

  const fetchData = async () => {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const information = await response.json();
      if (id === '000000000') {
        setProfilePhoto(account.photoURL3);
      } else if (information.gender === 'Male') {
        setProfilePhoto(account.photoURL1);
      } else {
        setProfilePhoto(account.photoURL2);
      }
    } catch (error) {
      console.error(error);
    }
    return {};
  };

  useEffect(() => {
    fetchData(); // fetch data asynchronously
  }, []);

  const handleOpen = (event) => {
    setOpen(event.currentTarget);
  };

  const handleClose = () => {
    setOpen(null);
  };

  const handleClick = () => {
    navigate('/peoples_budget/login', { replace: true });
  };

  return (
    <>
      <IconButton
        onClick={handleOpen}
        sx={{
          p: 0,
          ...(open && {
            '&:before': {
              zIndex: 1,
              content: "''",
              width: '100%',
              height: '100%',
              borderRadius: '50%',
              position: 'absolute',
              bgcolor: (theme) => alpha(theme.palette.grey[900], 0.8),
            },
          }),
        }}
      >
        <Avatar src={profilePhoto} alt="profilePhoto" />
      </IconButton>

      <Popover
        id="popWindow"
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 0,
            mt: 1.5,
            ml: 0.75,
            textAlign: 'center',
            width: 160,
            '& .MuiMenuItem-root': {
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <MenuItem id="logout" onClick={handleClick} sx={{ m: 1 }}>
          Logout
        </MenuItem>
      </Popover>
    </>
  );
}
