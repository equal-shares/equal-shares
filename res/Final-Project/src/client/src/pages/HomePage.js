import { Helmet } from 'react-helmet-async';
import { Typography, Box, CardContent, Card } from '@mui/material';

export default function HomePage() {
  // Card design
  const contentStyles = {
    position: 'absolute',
    right: '2%',
    zIndex: 1,
    marginBottom: '20px',
  };

  return (
    <Box>
      <Helmet>
        <title> Home </title>
      </Helmet>

      <Box sx={{ marginTop: '-35px' }}>
        <Typography
          style={{
            textAlign: 'center',
            fontFamily: 'Ubuntu',
            fontWeight: 'bold',
            fontSize: '35px',
            marginBottom: '20px',
            color: 'rgba(0, 0, 75, 0.95)',
          }}
        >
          YOUR VOTE, YOUR BUDGET!
        </Typography>
      </Box>

      <Box sx={{ minWidth: '860px', width: '75%', mt: '20px' }} style={contentStyles}>
        <Card
          sx={{
            backgroundColor: 'rgb(0, 150, 200, 0.99)',
            color: 'white',
            marginBottom: '25px',
            display: 'flex',
            alignItems: 'center',
            borderRadius: '40px',
          }}
        >
          <CardContent>
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/welcome.png`}
              alt="Logo"
              style={{
                width: '220px',
                float: 'right',
                marginRight: '23px',
                zIndex: -1,
              }}
            />
            <Typography
              variant="body1"
              dir="rtl"
              style={{
                maxWidth: '66%',
                float: 'left',
                marginLeft: '30px',
                fontFamily: 'Alef',
                fontSize: '19px',
                lineHeight: '1.5',
                zIndex: 1,
              }}
            >
              תקציב העם: עוצמת האזרחים לעצב את העתיד.
              <br />
              ברוכים הבאים לתקציב העם, פלטפורמה פורצת דרך המעמידה את כוח קבלת ההחלטות בידי העם. האתר שלנו מספק גישה
              כוללת ודמוקרטית לקביעת אופן הקצאת תקציבי המדינה. אנחנו מאמינים שכל אזרח צריך להביע דעה בעיצוב עתיד הקהילה
              שלו, וזה בדיוק מה שאנחנו מציעים. בתקציב העם, אנו מבינים שלכל אדם יש סדרי עדיפויות ודאגות ייחודיים. לכן אנו
              מספקים מגוון מקיף של פרויקטים ויוזמות, כל אחד מלווה במידע מפורט, מבטיח שקיפות וקבלת החלטות מושכלת.
              <br /> בין אם זה חינוך, שירותי בריאות, תשתיות או תוכניות חברתיות, תמצא הכל כאן.
            </Typography>
          </CardContent>
        </Card>

        <Card
          sx={{
            backgroundColor: 'rgb(0, 150, 200, 0.83)',
            color: 'white',
            marginBottom: '25px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '40px',
          }}
        >
          <CardContent>
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/explorer.png`}
              alt="Logo"
              style={{
                width: '150px',
                float: 'right',
                marginTop: '10px',
                marginRight: '35px',
                zIndex: -1,
              }}
            />
            <Typography
              variant="body1"
              dir="rtl"
              style={{
                maxWidth: '66%',
                float: 'left',
                marginLeft: '30px',
                fontFamily: 'Alef',
                fontSize: '19px',
                lineHeight: '1.5',
                zIndex: 1,
              }}
            >
              הממשק הידידותי שלנו מאפשר לך לחקור ולהצביע בנושאים החשובים לך ביותר. אנו מעריכים את קולך ורוצים להבטיח
              שהקול שלך ייספר. על ידי השתתפות בתהליך קבלת ההחלטות, אתה הופך לתורם פעיל לפיתוח והתקדמות הקהילה שלך. אבל
              זה לא נגמר שם. אנו הולכים צעד קדימה על ידי מתן נתונים סטטיסטיים בזמן אמת על ההצבעות וחלוקת התקציב.
              הפלטפורמה שלנו משתמשת בשני אלגוריתמי חלוקה מתקדמים המציעים תובנות לגבי אופן חלוקת התקציב על סמך הבחירות
              הקולקטיביות שנעשו על ידי האזרחים. <br />
            </Typography>
          </CardContent>
        </Card>

        <Card
          sx={{
            backgroundColor: 'rgb(0, 150, 200, 0.66)',
            color: 'white',
            margin: 'auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '25px',
            borderRadius: '40px',
            height: '180px',
          }}
        >
          <CardContent>
            <img
              src={`${process.env.PUBLIC_URL}/img_bg/fun.png`}
              alt="Logo"
              style={{
                width: '230px',
                float: 'right',
                marginTop: '30px',
                marginRight: '-10px',
                zIndex: -1,
              }}
            />
            <Typography
              variant="body1"
              dir="rtl"
              style={{
                maxWidth: '66%',
                float: 'left',
                marginLeft: '30px',
                fontFamily: 'Alef',
                fontSize: '19px',
                lineHeight: '1.5',
                zIndex: 1,
                marginTop: '90px',
              }}
            >
              {' '}
              הישארו מעודכנים וצפו בתוצאות האחרונות כדי לראות את ההשפעה של ההצבעה שלך על חלוקת התקציב הכוללת. הצטרפו עוד
              היום לתקציב העם ותשפיעו. ביחד, בואו נעצב עתיד טוב יותר, ונגרום למדינה שלנו לפרוח.
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}
