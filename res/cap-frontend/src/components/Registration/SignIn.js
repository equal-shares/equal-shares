import React, { useState } from 'react';
import { API } from '../../api/api-service';
import { API_AUTH } from '../../api/auth-service';
import './SignForms.css';
import logo1 from '../../logo.png';

function Auth() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [message, setMessage] = useState('');

    const loginClicked = (event) => {
        event.preventDefault(); // Prevent form submission and page refresh

        if (!username || !password) {
            setMessage("אימייל או סיסמא ריקים")
        } else {
            API_AUTH.LoginUser({ 'login': username, 'password': password })
                .then(resp => {
                    console.log(resp)
                    if (resp.detail === 'Login successful') {
                        window.location.href = `/home`;

                    } else {
                        API.getUserStatus(username)
                            .then(resp => {
                                setMessage(resp.message)
                                console.log(message)
                            })
                            .catch(error => console.log(error))
                    }
                })
                .catch(error => console.log(error))
        }
    }


    return (
        <div className="login">

            <main className="form-signin w-100 m-auto">

                <form>
                    <img className="mb-4 center" src={logo1} alt="" width="75" height="65" />
                    <h1 className="h3 mb-3 fw-normal text-center">התחברו ודרגו!</h1>

                    {message && <span>
                        <div className="alert alert-danger d-flex align-items-center" role="alert">{message}</div>
                    </span>}
                    <label className='form-label d-flex text-right mb-1' htmlFor="">אימייל</label>
                    <input data-testid="email" type="email" className="form-control left" id="floatingInput" placeholder="name@example.ariel.ac.il"
                        value={username}
                        onChange={evt => setUsername(evt.target.value)} />
                    <label className='form-label d-flex text-right mt-2 mb-1' htmlFor="">סיסמא</label>
                    <input type="password" data-testid="password" className="form-control left" id="floatingPassword" placeholder="Password"
                        value={password} onChange={evt => setPassword(evt.target.value)} />
 
                    <button className="btn btn-primary w-100 py-2" data-testid="loginButton" type="submit" onClick={loginClicked}>התחברות</button>
                    <div className="text-center text-muted mt-5 mb-0">שכחת את הסיסמא? <a href="/send-email-reset-password"
                    className="fw-bold text-body"><u>איפוס הסיסמא</u></a></div>
                </form>
                <p className="text-center text-muted mt-5 mb-0">עדיין לא נרשמת? <a href="/register"
                    className="fw-bold text-body"><u>הרשמה כאן!</u></a></p>
            </main>
        </div>
    );
}

export default Auth;
