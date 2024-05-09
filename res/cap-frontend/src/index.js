import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Footer from './components/Footer/Footer'
import StudentRoutes from "./routes/StudentRoutes";
import PublicRoutes from "./routes/PublicRoutes";
import UnauthRoutes from "./routes/UnauthRoutes";
import Cookies from 'js-cookie';


export default function Router() {

  const router = createBrowserRouter([
    Cookies.get('csrftoken') ? StudentRoutes() : UnauthRoutes(),
     ...PublicRoutes()
  ]);

  return (    
      <React.StrictMode>
        <RouterProvider router={router} />
        <Footer/>
        </React.StrictMode>
          );
}

ReactDOM.render(<Router/>, document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
