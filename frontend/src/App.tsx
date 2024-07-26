import { useEffect } from 'react';

import { ToastContainer } from 'react-toastify';

import 'react-toastify/dist/ReactToastify.css';

import MainPage from './components/MainPage';
import { getConfig } from './config';
import WithoutAuthPage from './components/WithoutAuthPage';
import NotAuthenticated from './components/NotAuthenticated';
import { registerPostMessage } from './postMessage';

export default function App() {
  const searchParams = new URLSearchParams(window.location.search);

  const config = getConfig();

  const email = searchParams.get('email');
  const token = searchParams.get('token');

  useEffect(registerPostMessage, []);

  // load config for checking that all the environment variables are set
  try {
    getConfig();
  } catch (error) {
    console.error(error);
    if (error instanceof Error) {
      return <>{error.message}</>;
    }
    return <></>;
  }

  if ((!email || !token) && !config.withoutAuthMode) {
    return <NotAuthenticated />;
  }

  return (
    <div dir="rtl">
      <div className="h-fit">
        <div className="w-fit mx-auto py-[10px]">
          {config.withoutAuthMode ? (
            <WithoutAuthPage />
          ) : (
            <MainPage email={email as string} token={token as string} />
          )}
        </div>
      </div>
      <div className="w-full min-h-[50px] p-[10px] border border-[#DEE2E6] border-t-1">
        <div className="w-fit mx-auto">© 2023 המעבדה לאלגוריתמים כלכליים</div>
      </div>
      <ToastContainer position="top-left" newestOnTop={false} rtl />
    </div>
  );
}
