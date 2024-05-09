import { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { Stack, IconButton, InputAdornment, TextField, Typography } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import Iconify from '../../components/iconify/Iconify';
import AddressContext from '../../contexts/AddressContext';


export default function ForgetPass(props) {
  const navigate = useNavigate();
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfPassword, setShowConfPassword] = useState(false);

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [newPasswordError, setNewPasswordError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');

  const [id, setId] = useState(props.id);
  const address = useContext(AddressContext);

  useEffect(() => {
    setId(props.id);
  }, [props.id]);

  const handleClick = async () => {
    const url = `${address}forget_password`;

    // Validate the input fields
    if (newPassword.length < 5) {
      setNewPasswordError('Invalid password: Please enter a password with at least 5 characters.');
      return;
    }
    setNewPasswordError('');

    if (confirmPassword.length < 5) {
      setConfirmPasswordError('Invalid password: Please enter a password with at least 5 characters.');
      return;
    }
    setConfirmPasswordError('');

    if (newPassword !== confirmPassword) {
      alert('The passwords are not the same, please enter the same password.');
      return;
    }
    setConfirmPasswordError('');

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, newPassword }),
      });

      const responseData = await response.json();
      if (responseData.status === 'Succeeded') {
        navigate('/peoples_budget/login', { replace: true });
        props.setIsShowed(false);
      }
    } catch (error) {
      console.error(error);
      alert('An error was received, please refresh the page and try again');
    }
  };

  return (
    <>
      <Typography variant="h4" gutterBottom sx={{ marginTop: '-191px', display: 'flex', justifyContent: 'center' }}>
        Forget Password ?
      </Typography>
      <Stack spacing={2}>
        <TextField
          id="NewPassword"
          label="New Password"
          type={showNewPassword ? 'text' : 'password'}
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          error={Boolean(newPasswordError)}
          helperText={newPasswordError}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowNewPassword(!showNewPassword)} edge="end">
                  <Iconify icon={showNewPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <TextField
          id="ConfirmPassword"
          label="Confirm Password"
          type={showConfPassword ? 'text' : 'password'}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          error={Boolean(confirmPasswordError)}
          helperText={confirmPasswordError}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowConfPassword(!showConfPassword)} edge="end">
                  <Iconify icon={showConfPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Stack>
      <Stack sx={{ marginTop: 2 }}>
        <LoadingButton
          id="SaveBtn"
          fullWidth
          size="large"
          type="submit"
          variant="contained"
          sx={{ fontSize: '1rem' }}
          onClick={handleClick}
        >
          Save
        </LoadingButton>
      </Stack>
    </>
  );
}

ForgetPass.propTypes = {
  setIsShowed: PropTypes.func.isRequired,
  id: PropTypes.string.isRequired,
};
