import { Navigate } from "react-router-dom";
import Auth from '../components/Registration/SignIn';
import Reg from '../components/Registration/SignUp'
import ResetPass from '../components/Registration/ResetPassword'
import VerifyUser from '../components/Registration/VerifyUser'
import NewPassword from '../components/Registration/NewPassword'

export default function PublicRoutes() {
  return {
    children:[   
      { path: "/login", element: <Auth /> },
      { path: "/register", element: <Reg /> },
      { path: "/send-email-reset-password", element: <NewPassword /> },
      { path: "/reset-password", element: <ResetPass /> },
      { path: "/verify-user", element: <VerifyUser /> },
      { path: "*", element: <Navigate to="/login" replace /> },
    ]
  }
}