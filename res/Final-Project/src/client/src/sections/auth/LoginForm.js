import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Stack, IconButton, InputAdornment, TextField, Link } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import PropTypes from 'prop-types';
import UserContext from '../../contexts/UserContext';
import AddressContext from '../../contexts/AddressContext';
import Iconify from '../../components/iconify/Iconify';
import account from '../../_mock/account';

export default function LoginForm({ setId }) {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [password, setPassword] = useState('');

  const [idError, setIdError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const id = useContext(UserContext || JSON.stringify(localStorage.getItem('id')));
  const address = useContext(AddressContext);

  useEffect(() => {
    localStorage.setItem('id', id);
  }, [id]);

  const handleClick = async () => {
    const url = `${address}login`;
    localStorage.setItem('id', id); // Set the user id in localStorage

    // Validate the input fields
    if (id.length !== 9) {
      setIdError('Invalid ID: Please enter a 9 digit number.');
      return;
    }
    setIdError('');

    if (password.length < 5) {
      setPasswordError('Invalid password: Please enter a password with at least 5 characters.');
      return;
    }
    setPasswordError('');

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, password }),
      });

      const responseData = await response.json();

      if (responseData.status === 'Succeeded') {
        navigate('/peoples_budget/home', { replace: true });
      } else {
        throw new Error('Please check your credentials and try again. \nIf you do not have an account, click "Sign Up" to create one.');
      }
    } catch (error) {
      console.log(error);
      alert(error.message);
    }
  };

  const handleClickGuest = async () => {
    const url = `${address}login`;
    setId(account.id);
    setPassword(account.password);
    localStorage.setItem('id', id); // Set the user id in localStorage

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, password }),
      });
      const responseData = await response.json();
      await new Promise((resolve) => setTimeout(resolve, 1000));
      if (responseData.status !== null) {
        navigate('/peoples_budget/home', { replace: true });
      }
      // if (responseData.status === 'Succeeded') {
      //   navigate('/peoples_budget/home', { replace: true });
      // } else {
      //   alert('Error, please refresh the page and try again.');
      // }
    } catch (error) {
      console.log(error);
      alert('Error, please refresh the page and try again.');
    }
  };

  const handleForgetPass = async () => {
    navigate('/peoples_budget/forget_password', { replace: true });
  };

  return (
    <>
      <Stack spacing={3}>
        <TextField
          id="logId"
          label="ID"
          value={id}
          onChange={(e) => setId(e.target.value)}
          error={Boolean(idError)}
          helperText={idError}
        />

        <TextField
          id="logPassword"
          label="Password"
          type={showPassword ? 'text' : 'password'}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={Boolean(passwordError)}
          helperText={passwordError}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                  <Iconify icon={showPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Stack>

      <Stack sx={{ my: 1 }}>
        <div
          className="forgot-password-link"
          role="button"
          tabIndex="0"
          onClick={handleForgetPass}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleForgetPass();
            }
          }}
          style={{
            cursor: 'pointer',
            textDecoration: 'underline',
            color: 'blue', 
            fontWeight: 'bold',
            fontSize: '15px',
          }}
        >
          Forgot Password?
        </div>

        {/* <Link
          variant="subtitle2"
          underline="always"
          alignItems="left"
          sx={{ cursor: 'pointer' }}
          onClick={handleForgetPass}
        >
          Forgot Password ?
        </Link> */}
      </Stack>

      <LoadingButton
        id="loginGuest"
        sx={{ '&:hover': { border: 'solid 2 black' } }}
        size="large"
        fullWidth
        type="submit"
        variant="outlined"
        onClick={handleClickGuest}
      >
        guest mode
      </LoadingButton>

      <LoadingButton
        id="loginBtn"
        sx={{ my: 1, fontSize: '1rem' }}
        fullWidth
        size="large"
        type="submit"
        variant="contained"
        onClick={handleClick}
      >
        Login
      </LoadingButton>
    </>
  );
}

LoginForm.propTypes = {
  setId: PropTypes.func.isRequired,
};
