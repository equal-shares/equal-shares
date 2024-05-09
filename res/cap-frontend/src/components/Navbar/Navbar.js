import React from 'react';
import { MenuItems } from "./MenuItems"
import './Navbar.css'
import { Link } from 'react-router-dom'
import { API_AUTH } from '../../api/auth-service';
import logo1 from '../../logo.png';
import Cookies from 'js-cookie';

function Navbar(props) {

  const logoutUser = () => {
    API_AUTH.LogoutUser()
      .then(resp => {
      Cookies.remove('csrftoken')
      console.log(resp)
      window.location.href = '/';

      })
      .catch(error => console.log(error))
    };


    return (
      <nav className="navbar sticky-top navbar-dark bg-primary navbar-expand-lg ">
        <div className="container-fluid">
          <div className="navbar-brand">
            <img src={logo1} alt="Logo" />
          </div>

          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              {MenuItems.map((item, index) => (
                <li className="nav-item" key={index}>
                  <Link
                    className={`nav-link ${props.active === item.title ? 'active' : ''}`}
                    to={item.url}
                  >
                    {item.title}
                  </Link>
                </li>
              ))}
              <li className="nav-item">
                <i
                  className="fas fa-sign-out-alt"
                  style={{ color: 'white', fontSize: '1.8rem', cursor: 'pointer' }}
                  onClick={logoutUser}
                ></i>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    );
}
export default Navbar;