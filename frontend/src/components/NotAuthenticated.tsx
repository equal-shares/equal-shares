import { Container, Typography } from '@mui/material';

export default function NotAuthenticated() {
  return (
    <Container component="main" maxWidth={false} sx={{ maxWidth: 800 }}>
      <div className="justify-items-center item-center">
        <Typography className="text-center" variant="h3" component="h1" gutterBottom>
          כדי להצביע במערכת התקציב ולהיכנס להגרלה
        </Typography>
        <Typography className="text-center" variant="h3" component="h1" gutterBottom>
          אנא התחבר תחילה
        </Typography>
      </div>
    </Container>
  );
}
