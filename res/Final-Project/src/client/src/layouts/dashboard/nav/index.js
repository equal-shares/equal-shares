import PropTypes from 'prop-types';
import { useState, useEffect, useContext } from 'react';
import { useLocation } from 'react-router-dom';
// @mui
import { styled, alpha } from '@mui/material/styles';
import { Box, Link, Drawer, Typography, Avatar } from '@mui/material';
// mock
import account from '../../../_mock/account';
// hooks
import useResponsive from '../../../hooks/useResponsive';
// components
import Scrollbar from '../../../components/scrollbar/Scrollbar';
import NavSection from '../../../components/nav-section/NavSection';
//
import navConfig from './config';
import UserContext from '../../../contexts/UserContext';
import AddressContext from '../../../contexts/AddressContext';

// ----------------------------------------------------------------------

const NAV_WIDTH = 280;

const StyledAccount = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(2, 2.5),
  borderRadius: Number(theme.shape.borderRadius) * 1.5,
  backgroundColor: alpha(theme.palette.grey[500], 0.12),
}));

// ----------------------------------------------------------------------

Nav.propTypes = {
  openNav: PropTypes.bool,
  onCloseNav: PropTypes.func,
};

export default function Nav({ openNav, onCloseNav }) {
  const { pathname } = useLocation();

  const isDesktop = useResponsive('up', 'lg');
  const [name, setName] = useState(JSON.stringify.apply(localStorage.getItem('name') ?? ''));
  const [profilePhoto, setProfilePhoto] = useState('');
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
        setName(account.displayName);
        setProfilePhoto(account.photoURL3);
      } else {
        setName(`${information.first_name} ${information.last_name}`);
        if (information.gender === 'Male') {
          setProfilePhoto(account.photoURL1);
        } else {
          setProfilePhoto(account.photoURL2);
        }
      }
    } catch (error) {
      console.error(error);
    }
    return {};
  };

  useEffect(() => {
    fetchData(); // fetch data asynchronously
  }, []);

  useEffect(() => {
    if (openNav) {
      onCloseNav();
    }
  }, [pathname]);

  const renderContent = (
    <Scrollbar
      sx={{
        height: 1,
        '& .simplebar-content': { height: 1, display: 'flex', flexDirection: 'column' },
      }}
    >
      <Box sx={{ py: 3, textAlign: 'center' }}>
        <img src={`${process.env.PUBLIC_URL}/img_bg/pLogo.png`} alt="Logo" style={{ marginTop: '-30px' }} />
      </Box>

      <Box sx={{ width: '94%', mb: 4, mx: 1.1, marginTop: '-15px' }}>
        <Link underline="none">
          <StyledAccount>
            <Avatar src={profilePhoto} alt="profilePhoto" />

            <Box sx={{ margin: 'auto' }}>
              <Typography variant="subtitle2" sx={{ fontSize: '16px', color: 'text.primary' }}>
                {name}
              </Typography>
            </Box>
          </StyledAccount>
        </Link>
      </Box>

      <NavSection data={navConfig} />
    </Scrollbar>
  );

  return (
    <Box
      component="nav"
      sx={{
        flexShrink: { lg: 0 },
        width: { lg: NAV_WIDTH },
      }}
    >
      {isDesktop ? (
        <Drawer
          open
          variant="permanent"
          PaperProps={{
            sx: {
              width: NAV_WIDTH,
              bgcolor: 'background.default',
              borderRightStyle: 'dashed',
            },
          }}
        >
          {renderContent}
        </Drawer>
      ) : (
        <Drawer
          open={openNav}
          onClose={onCloseNav}
          ModalProps={{
            keepMounted: true,
          }}
          PaperProps={{
            sx: { width: NAV_WIDTH },
          }}
        >
          {renderContent}
        </Drawer>
      )}
    </Box>
  );
}
