import React, {Component } from 'react'
import {OfficeItems} from "./OfficeItems"
import './Navbar_Office.css'
import { Link } from 'react-router-dom'
import logo1 from '.../../../public/logo.png';
import Cookies from 'js-cookie';


class NavbarOffice extends Component
{

    state = { clicked: false }
    handleClicked = () => this.setState({clicked: !this.state.clicked})
    logoutUser = () => {
        Cookies.remove('csrftoken');
        window.location.href = '/';
    }

    render()
    {
        return(
                <nav className="NavbarItems">
                    <div><img className="fab fa-react1" src={logo1} alt="" /></div>
                    <div className="logo2">Fair Division</div>
                    <div className="menu-icon" onClick= {this.handleClicked}>
                        <i className={this.state.clicked ? 'fas fa-times': 'fas fa-bars'}></i>
                    </div>
                
                        <ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'}>
                            {OfficeItems.map((item, index)=>{
                                return (
                                    <li key={index}>
                                    {this.props.active === item.title && 
                                    <Link className="active" to={item.url}>
                                        {item.title}
                                    </Link>}
                                    {this.props.active !== item.title && 
                                    <Link className={item.cName} to={item.url}>
                                        {item.title}
                                    </Link>}
                                </li>
                                )
                            })}
                        </ul>
                        <i style={{fontSize:'3rem',marginTop:'1%', marginRight:'3%',position:'inherit',cursor:'pointer' }} className="fas fa-sign-out-alt" onClick={this.logoutUser}></i>

                    
                </nav>
        )
    }
}

export default NavbarOffice