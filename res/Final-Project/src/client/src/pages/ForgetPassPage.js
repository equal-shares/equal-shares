import { Helmet } from 'react-helmet-async';
import { useNavigate } from 'react-router-dom';
// @mui
import { styled } from '@mui/material/styles';
import { Link, Container, Typography } from '@mui/material';
// sections
import ForgetPassForm from '../sections/auth/ForgetPassForm';
import useResponsive from '../hooks/useResponsive';

// Styled components for custom styling
const StyledContent = styled('div')(({ theme }) => ({
  maxWidth: 480,
  margin: 'auto',
  minHeight: '100vh',
  display: 'flex',
  justifyContent: 'center',
  flexDirection: 'column',
  padding: theme.spacing(6, 0),
  objectFit: 'cover',
  position: 'relative',
  zIndex: 1, // Set a higher z-index value to make it appear above the background
}));

const StyledImageContainer = styled('div')({
  position: 'fixed',
  top: 0,
  left: 0,
});

export default function ForgetPassPage() {
  const navigate = useNavigate();
  const mdUp = useResponsive('up', 'md');

  // Handle click event to navigate to the login page
  const handleClick = () => {
    navigate('/peoples_budget/login', { replace: true });
  };

  return (
    <>
      <Helmet>
        <title> Forget Password </title>
      </Helmet>

      {mdUp && (
        <StyledImageContainer>
          <Typography variant="h3" sx={{ px: 0, mt: 0, mb: -10 }}>
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/pLogo.png`}
              alt="Logo"
              style={{ alignSelf: 'flex-start', width: '400px' }}
            />
          </Typography>

          <div style={{ marginLeft: '30px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/QuestionMarks.png`}
              alt=""
              style={{ marginTop: '50px', width: '250px' }}
            />
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/ForgetPass.png`}
              alt=""
              style={{ marginTop: '-100px', width: '440px' }}
            />
          </div>
        </StyledImageContainer>
      )}

      <Container maxWidth="sm" style={{ marginRight: '100px' }}>
        <StyledContent>
          {/* <Typography variant="h4" gutterBottom sx={{ marginTop: '-50px', display: 'flex', justifyContent: 'center' }}>
            Forget Password ?
          </Typography> */}

          <ForgetPassForm />

          <Typography variant="body2" sx={{ mb: 5 }}>
            Have an account?
            <br />
            <button
              type="button"
              className="login-button"
              onClick={handleClick}
              style={{
                background: 'none',
                border: 'none',
                padding: 0,
                font: 'inherit',
                textDecoration: 'underline',
                cursor: 'pointer',
                color: 'blue',
                fontWeight: 'bold',
                fontSize: '14px',
              }}
            >
              Login
            </button>{' '}
            {/* <Link variant="subtitle2" onClick={handleClick} sx={{ cursor: 'pointer' }}>
              Login
            </Link>{' '} */}
            here.
          </Typography>
        </StyledContent>
      </Container>
    </>
  );
}
