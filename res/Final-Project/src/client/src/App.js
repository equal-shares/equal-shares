import { useState } from 'react';
import Router from './routes';
// theme
import ThemeProvider from './theme';
// components
import ScrollToTop from './components/scroll-to-top/ScrollToTop';
// context
import UserContext from './contexts/UserContext';
import AddressContext from './contexts/AddressContext';

export default function App() {
  // Define a state variable 'id' and initialize it with the value of 'localStorage.getItem('id')' or an empty string if it's not available
  const [id, setId] = useState(localStorage.getItem('id') ?? '');

  const serverUrl = process.env.REACT_APP_SERVER_URL || 'http://localhost';
  const serverPort = process.env.REACT_APP_SERVER_PORT || 5002;
  const [address] = useState(`${serverUrl}:${serverPort}/peoples_budget/server/`);

  return (
    // Provide the 'id' value to the UserContext using UserContext.Provider
    <UserContext.Provider value={id}>
      {/* Provide the 'address' to the AddressContext using AddressContext.Provider */}
      <AddressContext.Provider value={address}>
        {/* Wrap the entire app with ThemeProvider to apply a theme */}
        <ThemeProvider>
          {/* Render the ScrollToTop component to handle scrolling behavior */}
          <ScrollToTop />
          {/* Render the Router component and pass the 'setId' function as a prop */}
          <Router setId={setId} />
        </ThemeProvider>
      </AddressContext.Provider>
    </UserContext.Provider>
  );
}
