
const randomNumW = Math.floor(Math.random() *14) ;
const randomNumM = 14 + Math.floor(Math.random() * 17) ;
const account = {
  displayName: 'Guest User',
  id: '000000000',
  password: '00000',  
  photoURL1: `/assets/images/avatars/avatar_${randomNumM}.jpg`,
  photoURL2: `/assets/images/avatars/avatar_${randomNumW}.jpg`,
  photoURL3: `/assets/images/avatars/avatar_default.jpg`,
};

export default account;
