import { Navigate, useRoutes } from 'react-router-dom';
// layouts
import DashboardLayout from './layouts/dashboard/DashboardLayout';
import SimpleLayout from './layouts/simple/SimpleLayout';
// pages
import HomePage from './pages/HomePage';
import VotingPage from './pages/VotingPage';
import InfoPage from './pages/InfoPage';
import DashboardPage from './pages/DashboardPage';
import ResultsPage from './pages/ResultsPage';
import LoginPage from './pages/LoginPage';
import SignUPage from './pages/SignUPage';
import ForgetPassPage from './pages/ForgetPassPage';
import AboutUs from './pages/AboutUs';

export default function Router({ setId }) {
  // Define the routes using the useRoutes hook from react-router-dom
  const routes = useRoutes([
    {
      path: '/peoples_budget',
      element: <DashboardLayout />,
      children: [
        { element: <Navigate to="/home" />, index: true },
        { path: 'home', element: <HomePage /> },
        { path: 'voting', element: <VotingPage /> },
        { path: 'information', element: <InfoPage /> },
        { path: 'dashboard', element: <DashboardPage /> },
        { path: 'results', element: <ResultsPage /> },
        { path: 'about_us', element: <AboutUs /> },
      ],
    },
    {
      element: <SimpleLayout />,
      children: [
        { element: <Navigate to="/peoples_budget/login" />, index: true },
        { path: '/peoples_budget/login', element: <LoginPage setId={setId} /> },
        { path: '/peoples_budget/sign_up', element: <SignUPage /> },
        { path: '/peoples_budget/forget_password', element: <ForgetPassPage /> },
      ],
    },
  ]);

  return routes;
}
