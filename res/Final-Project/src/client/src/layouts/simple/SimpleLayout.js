import { Outlet } from 'react-router-dom';
// @mui
import { styled } from '@mui/material/styles';

const StyledHeader = styled('header')(({ theme }) => ({
  top: 0,
  left: 0,
  lineHeight: 0,
  width: '100%',
  position: 'absolute',
  padding: theme.spacing(3, 3, 0),
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(5, 5, 0),
  },
  display: 'flex',
  alignItems: 'flex-start',
  height: '100%',
  boxSizing: 'border-box',
}));

export default function SimpleLayout() {
  return (
    <>
      {/* <StyledHeader sx={{ fontWeight: 'bold', fontSize: '20px' }}> */}
      <StyledHeader>
        {/* People's Budget */}
        {/* <img
          src={`${process.env.PUBLIC_URL}/pLogo.png`}
          alt="Logo"
          style={{ alignSelf: 'flex-start', marginTop: '-80px', marginLeft: '-85px', width: '35%'}}
        /> */}
      </StyledHeader>

      <Outlet />
    </>
  );
}
