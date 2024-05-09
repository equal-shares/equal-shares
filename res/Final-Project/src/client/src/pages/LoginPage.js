import { useState, useEffect, useContext } from 'react';
import { Helmet } from 'react-helmet-async';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import { Container, Typography, Button } from '@mui/material';
import PropTypes from 'prop-types';
import useResponsive from '../hooks/useResponsive';
import LoginForm from '../sections/auth/LoginForm';
import OldBudget from '../sections/auth/OldBudget';
import AddressContext from '../contexts/AddressContext';

// Styled components for custom styling
const StyledContent = styled('div')(({ theme }) => ({
  maxWidth: 480,
  margin: 'auto',
  minHeight: '80vh',
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

export default function LoginPage({ setId }) {
  const navigate = useNavigate();
  const mdUp = useResponsive('up', 'md');
  const [tableData, setTableData] = useState(JSON.parse(localStorage.getItem('table')) ?? []);
  const [isClicked, setIsClicked] = useState(false);
  const address = useContext(AddressContext);
  const url = `${address}login`;

  // Fetching data of the old budget table
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        const information = JSON.parse(await response.json());
        setTableData(information.children);
        localStorage.setItem('table', JSON.stringify(information.children));
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, []);

  // Event handlers
  const handleClick = () => {
    navigate('/peoples_budget/sign_up', { replace: true });
  };

  const handleBudgetClick = () => {
    setIsClicked((prev) => !prev);
  };

  return (
    <>
      <Helmet>
        <title> Login </title>
      </Helmet>

      {mdUp && (
        <StyledImageContainer>
          <Typography variant="h3" sx={{ px: 0, mt: 0, mb: -5 }}>
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/pLogo.png`}
              alt="Logo"
              style={{ alignSelf: 'flex-start', width: '400px' }}
            />
          </Typography>
          <img src={`${process.env.PUBLIC_URL}/img_bg/login.png`} alt="login" />
        </StyledImageContainer>
      )}

      <Container maxWidth="sm" style={{ marginRight: '100px' }}>
        <StyledContent>
          <Typography variant="h4" gutterBottom sx={{ display: 'flex', justifyContent: 'center' }}>
            Login to People's Budget
          </Typography>

          <LoginForm setId={setId} />

          <Typography variant="body2" sx={{ mb: 3 }}>
            Don't have an account?
            <br />
            <button
              type="button"
              id="toSign"
              className="sign-up-button"
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
              Sign up
            </button>{' '}
            {/* <Link id="toSign" variant="subtitle2" onClick={handleClick} sx={{ cursor: 'pointer' }}>
              Sign up
            </Link>{' '} */}
            here.
          </Typography>
          <Button
            id="budgetBtn"
            size="medium"
            onClick={handleBudgetClick}
            type="submit"
            variant="text"
            style={{
              color: 'black',
              margin: '0 auto',
              width: '200px',
              marginTop: '43px',
              marginBottom: '30px',
              border: '2mm double rgb(51, 102, 255, 0.65)',
            }}
          >
            State Budget - 2022
          </Button>
          {isClicked && <OldBudget tableData={tableData} />}
        </StyledContent>
      </Container>
    </>
  );
}

LoginPage.propTypes = {
  setId: PropTypes.func.isRequired,
};
