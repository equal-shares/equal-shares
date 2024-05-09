import React, { useState } from 'react';
import { API_AUTH } from '../../api/auth-service';

import './SignForms.css';
import { validate } from 'email-validator';
import {isEmailAriel} from './FieldValidators'
import logo1 from '../../logo.png';
import { isNumber } from 'mathjs';


function Register() {

  const [username,setUserName] = useState('');
  const [first_name, setFirstname] = useState('');
  const [last_name, setLastname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setpassword] = useState('');
  const [password_confirm, setpassword_confirm] = useState('');
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [validated, setValidated] = useState('');
  //const [user_type, setUserType] = useState('student');
  const [amount_elective, setAmountElective] = useState(6);
  const [program, setProgram] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'first_name') setFirstname(value);
    if (name === 'last_name') setLastname(value);
    if (name === 'email') {
      setEmail(value);
      setUserName(value);
    }
    if (name === 'password') setpassword(value);

    if (name === 'password_confirm') setpassword_confirm(value);

    if (name === 'amount_elective') {
      if (isNumber(value) &&(value > 0 && value <= 6))
        setAmountElective(value);
    }
    if (name === 'program') {
      setProgram(value)
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!first_name) {
      errors.firstname = 'שם פרטי נדרש';
    }
    if (!last_name) {
      errors.lastname = 'שם משפחה נדרש';
    }


    if (!email) {
      errors.email = 'כתובת אימייל נדרשת';
    } else if (!isEmailValid(email)) {
      errors.email = 'כתובת אימייל לא חוקית';
    } else if (!isEmailAriel(email)) {
      errors.email = 'כתובת האימייל חייבת להסתיים בariel.ac.il';
    }

    if (!password) {
      errors.password = 'סיסמא נדרשת';
    }

    if (!password_confirm) {
      errors.password_confirm = 'אימות סיסמא נדרש';
    } else if (password !== password_confirm) {
      errors.password_confirm = 'סיסמאות לא תואמות';
    }
    if (!amount_elective){
      errors.amount_elective = 'מספר קורסי בחירה נדרש'
    }

    if (!program){
      errors.program = 'מסלול לימודים נדרש'
    }
    setErrors(errors);

    return Object.keys(errors).length === 0;
  };

  const isEmailValid = (email) => {
    return validate(email);

  };

  const registerClicked = (event) => {
    event.preventDefault(); // Prevent form submission and page refresh

    if (!validateForm()) {
      setValidated(true)
      return;
    }

    let user_req = {
      'username': username,
      'first_name': first_name, 
      'last_name':last_name,
      'email': email,
      'password': password,
      'password_confirm': password_confirm,
      'amount_elective':amount_elective,
      'program': program,
    }

    API_AUTH.RegisterUser(user_req)
    .then((resp) => {
      if (resp['id'])
        {alert('קישור לאימות חשבונך נשלח לכתובת האימייל שהזנת (בדקו בספאם)')}
      else
      {console.log(resp);

      setErrors(resp)
    }

    })
    .catch((error) => {
      console.log(user_req)
      setMessage(error);
      console.log(error);
    })

  };

  return (
    <div className="register" >
      <main className="form-signup w-100 m-auto">
        <form className="needs-validation" noValidate validate={validated}>
          <img className="mb-4" src={logo1} alt="" width="75" height="65" />
          <h1 className="h3 mb-3 fw-normal text-center">הרשמו והתחילו לדרג!</h1>
          {message && <span>
            <div className="alert alert-danger d-flex align-items-center text-center" role="alert">{message}</div>
          </span>}
          <div className="mb-2 ">
            <label className=" d-flex text-right form-label is-invalid">שם פרטי</label>
            <input
              className="form-control field-input "
              type="text"
              placeholder="שם פרטי"
              name="first_name"
              value={first_name}
              onChange={handleInputChange}
              required
            />

            {errors.firstname && <div className="invalid-feedback">{errors.firstname}</div>}
          </div>

          <div className=" mb-2">
            <label className="d-flex text-right form-label is-invalid">שם משפחה</label>
            <input
              className="form-control  "
              type="text"
              placeholder="שם משפחה"
              name="last_name"
              value={last_name}
              onChange={handleInputChange}
              required
            />

            {errors.lastname && <div className="invalid-feedback">{errors.lastname} </div>}
          </div>

          <div className=" mb-2">
            <label className="d-flex text-right form-label is-invalid">אימייל</label>
            <input
              className="form-control field-input left "
              type="email"
              placeholder="כתובת המייל הארגוני"
              name="email"
              value={email}
              onChange={handleInputChange}
              required
            />

            {errors.email && <span className="invalid-feedback">{errors.email}</span>}
            {errors.username && <span className="invalid-feedback">{errors.username}. אם נרשמתם בעבר אנו וודאו כי אימתתם את חשבנוכם באמצעות כתובת המייל.</span>}

          </div>

          <div className=" mb-2">
            <label className="d-flex text-right form-label is-invalid">סיסמא</label>
            <input
              className="form-control field-input left "
              type="password"
              placeholder="סיסמה"
              name="password"
              value={password}
              onChange={handleInputChange}
              required
            />

            {errors.password && <span className="invalid-feedback">{errors.password}</span>}
          </div>

          <div className=" mb-2">
            <label className="d-flex text-right form-label is-invalid">אימות סיסמא</label>
            <input
              className="form-control field-input left "
              type="password"
              placeholder="אימות סיסמא"
              name="password_confirm"
              value={password_confirm}
              onChange={handleInputChange}
              required
            />

            {errors.password_confirm && (
              <span className="invalid-feedback">{errors.password_confirm}</span>
            )}
          </div>
          <div className=" mb-2">

          <label className="d-flex text-right form-label is-invalid">מסלול לימודים</label>
          <div className="dropdown">
            <select name="program" value={program} onChange={handleInputChange}  required>
              <option value="">בחרו מסלול</option>
              <option value="1">אחר</option>
              <option value="2">מצטיינים</option>
            </select>
          </div>
          {errors.program && (
              <span className="invalid-feedback">{errors.program}</span>
            )}
          </div>
          <div className=" mb-2">
            <label className="d-flex text-right form-label">מספר קורסי בחירה נדרשים</label>
            <input
              type="number"
              name="amount_elective"
              onChange={handleInputChange}
              value={amount_elective}
              min={0}
              max={6} 
              required
              />
              
               {errors.amount_elective && (
              <span className="invalid-feedback">{errors.amount_elective}</span>
            )}
          </div>
          {/*<div className="btn-group item-center w-100">
            <input type="radio" className="btn-check" name="userType" id="student" autocomplete="off" onClick={() => setUserType('student')} checked={user_type === 'student'} />
            <label className="btn btn-outline-primary" for="student">סטודנטים</label>

            <input type="radio" className="btn-check" name="userType" id="guest" autocomplete="off" onClick={() => setUserType('guest')} checked={user_type === 'guest'} />
            <label className="btn btn-outline-primary" for="guest">אורחים</label>
               </div>*/}
          <button className="w-100 btn btn-lg btn-primary mt-3" type="submit" onClick={registerClicked}>
            הרשמה
          </button>
          <p className="text-center text-muted mt-5 mb-0">כבר יש לך חשבון? <a href="/"
            className="fw-bold text-body pr"><u>התחברו כאן!</u></a></p>
        </form>
      </main>
    </div>
  )
}

export default Register;
