import { Helmet } from 'react-helmet-async';
import { Container, Typography, Grid, Paper, Card, CardMedia, CardContent } from '@mui/material';

const styles = {
  header: {
    backgroundColor: 'rgba(0, 150, 200, 0.99)',
    borderRadius: '20px',
    padding: '30px 0',
    marginBottom: '20px',
    marginTop: '-20px',
    color: 'rgba(255, 255, 255, 1)',
  },
  paper: {
    padding: '20px',
    boxShadow: '0px 5px 5px rgba(0, 0, 0, 0.2)',
    marginBottom: '30px',
  },
};

export default function AboutUs() {
  return (
    <>
      <Helmet>
        <title> About Us </title>
      </Helmet>

      <div>
        <header style={styles.header}>
          <nav>
            <Typography variant="h3" align="center">
              ABOUT US
            </Typography>
          </nav>
        </header>

        <Grid item xs={12} sm={6}>
          <Paper style={styles.paper}>
            <Typography variant="h4" textAlign={'right'} gutterBottom>
              המשימה שלנו
            </Typography>
            <Typography dir="rtl" variant="body1" fontFamily="Alef" textAlign={'right'} fontSize={'18px'}>
              ב - ״תקציב העם״ אנו מאמינים שלכל אזרח צריכה להיות השפעה על האופן שבו המדינה עושה שימוש במיסים אותם הוא
              משלם.
              <br /> אנו מכירים בכך שתהליכי התקצוב המסורתיים יכולים לעתים קרובות להשאיר את האזרחים בתחושת ניתוק מההחלטות
              המשפיעות עליהם ועל הקהילות שלהם. המשימה שלנו היא לגשר על הפער הזה ולספק פלטפורמה שבה הדעות והרצונות שלך
              נלקחות בחשבון.
              <br /> הקול שלך, התקציב שלך! תאר לעצמך עולם שבו אתה יכול להשפיע ישירות על אופן הקצאת התקציבים במדינה שלך.
              עם״תקציב העם״, אתה לא צריך לדמיין יותר. אנו מציעים פלטפורמה ידידותית למשתמש המאפשרת לך להשתתף בתהליך קבלת
              החלטות התקציב בקלות.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Paper style={styles.paper}>
            <Typography variant="h4" textAlign={'right'} gutterBottom>
              מטרות עיקריות
            </Typography>
            <Typography dir="rtl" variant="body1" fontFamily="Alef" textAlign={'right'} fontSize={'18px'}>
              ● נגישות: אנו שואפים להפוך את ההשתתפות לנגישה לכל האזרחים, ללא קשר לידע טכני קודם.
              <br /> ● שקיפות: המחויבות שלנו לשקיפות מבטיחה שתוכל לעקוב אחר ההתקדמות והתוצאות של חלוקת התקציב כמעט בזמן
              אמת.
              <br /> ● העצמה: אנו מאמינים שאזרחים אשר נחשפים ליותר מידע, יכולים לקבל החלטות מושכלות יותר. הפלטפורמה שלנו
              מספקת לך את המידע שאתה צריך כדי לקבל החלטות משמעותיות.
              <br /> ● קבלת החלטות קולקטיבית: אנו מקדמים את כוחה של קבלת החלטות קולקטיבית, שבה רצון העם משפיע ישירות על
              חלוקת התקציב.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Paper style={styles.paper}>
            <Typography variant="h4" textAlign={'right'} gutterBottom>
              אלגוריתמים
            </Typography>
            <Typography dir="rtl" variant="body1" fontFamily="Alef" textAlign={'right'} fontSize={'18px'}>
              מאחורי הקלעים, ״תקציב העם״ משלב אלגוריתמים מתקדמים כדי להבטיח את היושרה וההגינות של תהליך הקצאת התקציב:{' '}
              <br /> ● אלגוריתם החציון: מבטיח שהקצאת התקציב תעשה בדרך: אנונימית, יעילה פארטו ומעודדות הצבעת אמת.
              <br /> ● אלגוריתם החציון המוכלל: בהתבסס על אלגוריתם החציון, אלגוריתם זה מרחיב את ההוגנות של הקצאת התקציב
              לקבוצות מגוונות בתוך האוכלוסייה תוך שמירה על אנונימיות הבוחרים ועידוד השתתפות בצורה כנה.
              <br /> אלגוריתמים אלו שומרים על שלמות תהליך הקצאת התקציב, תוך כיבוד הפרטיות וההעדפות של האזרחים המשתתפים.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Paper style={styles.paper}>
            <Typography variant="h4" textAlign={'right'} gutterBottom>
              הכירו את הצוות
            </Typography>
            <Typography dir="rtl" variant="body1" fontFamily="Alef" textAlign={'right'} fontSize={'18px'}>
              פרויקט ״תקציב העם״ פותח על ידי צוות מסור של אנשים החולקים תשוקה לדמוקרטיה ומעורבות אזרחית.
              <br /> ● <a href='#elhai' style={{ textDecoration: 'none', color: 'rgba(0, 150, 200, 0.99)' }}>אלחי מנצבך</a>
              <br /> ● <a href='#lioz' style={{ textDecoration: 'none', color: 'rgba(0, 150, 200, 0.99)' }}>ליעוז עקירב</a>
              <br /> ● <a href='#ofir' style={{ textDecoration: 'none', color: 'rgba(0, 150, 200, 0.99)' }}>אופיר עובדיה</a>
              <br /> הצוות שלנו מחויב ליצור חברה מכילה ודמוקרטית יותר שבה כל קול נשמע.
              <br /> הפיתוח נעשה תחת ההכוונה והליווי של{' '}
              <a style={{ textDecoration: 'none', color: 'rgba(0, 150, 200, 0.99)' }}>ד"ר אראל סגל הלוי</a>, שמילא
              תפקיד חיוני בעיצוב הפרויקט שלנו ובהבטחת התאמתו לעקרונות הדמוקרטיה ומעורבות האזרחים.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Paper style={styles.paper}>
            <Typography variant="h4" textAlign={'right'} gutterBottom>
              הצטרפו אלינו
            </Typography>
            <Typography dir="rtl" variant="body1" fontFamily="Alef" textAlign={'right'} fontSize={'18px'}>
              אנו מזמינים אתכם להצטרף אלינו למסע לקראת דמוקרטיה שקופה וישירה יותר.
              <br /> עם ״תקציב העם״, הקול שלך חשוב, ויחד נוכל לעצב את עתיד קבלת ההחלטות התקציביות.
              <br /> תודה שאתה חלק מקהילת ״תקציב העם״!
            </Typography>
          </Paper>
        </Grid>
      </div>

      <div>
        <Container>
          <Grid container spacing={4}>
            <Grid item xs={12} sm={4}>
              <a
                href="https://lioo7.github.io/My-Personal-Website/"
                target="_blank"
                rel="noopener noreferrer"
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <Card style={{ backgroundColor: 'rgba(145, 158, 171, 0.2)' }}>
                  <div id= 'lioz' style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <CardMedia
                      component="img"
                      alt="Team Member 1"
                      height="150"
                      style={{ width: '35%', borderRadius: '45%' }}
                      image="/about/lioz.png"
                    />
                    <CardContent>
                      <Typography variant="h6" align="center" fontFamily="Alef">
                        ליעוז עקירב
                      </Typography>
                    </CardContent>
                  </div>
                </Card>
              </a>
            </Grid>

            <Grid item xs={12} sm={4}>
              <a
                href="https://elhaimansbach.github.io/Personal-Website/"
                target="_blank"
                rel="noopener noreferrer"
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <Card style={{ backgroundColor: 'rgba(145, 158, 171, 0.2)' }}>
                  <div id= 'elhai' style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <CardMedia
                      component="img"
                      alt="Team Member 1"
                      height="150"
                      style={{ width: '35%', borderRadius: '45%' }}
                      image="/about/elhai.png"
                    />
                    <CardContent>
                      <Typography variant="h6" align="center" fontFamily="Alef">
                        אלחי מנצבך
                      </Typography>
                    </CardContent>
                  </div>
                </Card>
              </a>
            </Grid>

            <Grid item xs={12} sm={4}>
              <a
                href="https://github.com/OfirOvadia96"
                target="_blank"
                rel="noopener noreferrer"
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <Card style={{ backgroundColor: 'rgba(145, 158, 171, 0.2)' }}>
                  <div id= 'ofir' style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <CardMedia
                      component="img"
                      alt="Team Member 1"
                      height="150"
                      style={{ width: '35%', borderRadius: '45%' }}
                      image="/about/ofir.png"
                    />
                    <CardContent>
                      <Typography variant="h6" align="center" fontFamily="Alef">
                        אופיר עובדיה
                      </Typography>
                    </CardContent>
                  </div>
                </Card>
              </a>
            </Grid>
          </Grid>
        </Container>
      </div>
    </>
  );
}
