import { useState } from 'react';

import { Button, Container, Input, Typography } from '@mui/material';

import MainPage from './MainPage';

export default function WithoutAuthPage() {
  const [email, setEmail] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const emailOnChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const logginOnClick = () => {
    setLoggedIn(true);
  };

  if (loggedIn) {
    return <MainPage email={email} token="---" />;
  }

  return (
    <Container component="main" maxWidth={false} sx={{ maxWidth: 800 }}>
      <div className="justify-items-center item-center">
        <Typography className="text-center" variant="h3" component="h1" gutterBottom>
          כניסה ללא אבטחה
        </Typography>
        <div className="mt-[10px] flex justify-center">
          <Input
            value={email}
            onChange={emailOnChange}
            placeholder="email"
            style={{ direction: 'ltr' }}
          />
        </div>
        <div className="mt-[10px] flex justify-center">
          <Button color="primary" variant="contained" onClick={logginOnClick}>
            התחבר
          </Button>
        </div>
      </div>
    </Container>
  );
}
