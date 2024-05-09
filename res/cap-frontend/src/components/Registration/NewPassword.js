import React, { useState } from 'react';
import { API_AUTH } from '../../api/auth-service';
import './SignForms.css';
import logo1 from '../../logo.png';
import { useLocation } from 'react-router-dom';


function NewPassword() {

  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [validated, setValidated] = useState('');
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'password1') setPassword1(value);

    if (name === 'password2') setPassword2(value);

  };

  const validateForm = () => {
    const errors = {};

    if (!password1) {
      errors.password1 = 'סיסמא נדרשת';
    }

    if (!password2) {
      errors.password2 = 'אימות סיסמא נדרש';
    } else if (password1 !== password2) {
      errors.password2 = 'סיסמאות לא תואמות';
    }

    setErrors(errors);

    return Object.keys(errors).length === 0;
  };


 

  const setNewPassword = (event) => {
    event.preventDefault(); // Prevent form submission and page refresh

    if (!validateForm()) {
      setValidated(true)
      return;
    }
    const body = {
      'user_id': params.get('user_id'),
      'timestamp': params.get('timestamp'),
      'signature' :params.get('signature'),
      'password': password1
    }
    API_AUTH.ResetPassword(body)
      .then((resp) => {
        alert("סיסמתך החדשה נשמרה בהצלחה") // Add this line
        window.location.href='/'
      })
      .catch((error) => {
        alert("לא הצלחנו לשמור את הסיסמא הזו. נסו שנית") 
        setMessage(error.message);
      })
  };

  return (
    <div className="register" >
      <main className="form-signup w-100 m-auto">
        <form className="needs-validation" novalidate validate={validated}>
          <img className="mb-4" src={logo1} alt="" width="75" height="65" />
          <h1 className="h3 mb-3 fw-normal text-center">יצירת סיסמא חדשה</h1>
          {message && <span>
            <div className="alert alert-danger d-flex align-items-center text-center" role="alert">{message}</div>
          </span>}

         
          <div className=" mb-2">
            <label className="d-flex text-right form-label is-invalid">סיסמא</label>
            <input
              className="form-control field-input left "
              type="password"
              placeholder="סיסמה"
              name="password1"
              value={password1}
              onChange={handleInputChange}
              required
            />

            {errors.password1 && <span className="invalid-feedback">{errors.password1}</span>}
          </div>

          <div className=" mb-2">
            <label className="d-flex text-right form-label is-invalid">אימות סיסמא</label>
            <input
              className="form-control field-input left "
              type="password"
              placeholder="אימות סיסמא"
              name="password2"
              value={password2}
              onChange={handleInputChange}
              required
            />

            {errors.password2 && (
              <span className="invalid-feedback">{errors.password2}</span>
            )}
          </div>
          
          <button className="w-100 btn btn-lg btn-primary mt-3" type="submit" onClick={setNewPassword}>
            שמירה
          </button>
          <p className="text-center text-muted mt-5 mb-0"><a href="/"
            className="fw-bold text-body pr"><u>חזרה להתחברות</u></a></p>
        </form>
      </main>
    </div>
  )
}

export default NewPassword;
