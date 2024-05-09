import { Navigate } from "react-router-dom";
import Layout from "./Layout";
import App from '../components/Info/CoursesInfo';
import Ranking from '../components/Ranking/Ranking';
import Results from '../components/Results/Results';
import Feedback from '../components/Feedback/Feedback';
import Homepage from '../components/Profile/Profile'

export default function StudentRoutes() {
  return {
    element: <Layout />,
    children: [
      { path: "/courses_info", element: <App /> },
      { path: "/ranking", element: <Ranking /> },
      { path: "/results", element: <Results /> },
      { path: "/feedback", element: <Feedback /> },
      { path: "/home", element: <Homepage /> },
      { path: "*", element: <Navigate to="/home" replace /> },
    ],
  };
}