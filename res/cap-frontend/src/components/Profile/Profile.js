import React, { useEffect, useState } from 'react';
import { API } from '../../api/api-service';
import './Profile.css';
import Navbar from "../Navbar/Navbar";

function Homepage() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {

    API.getStudentDetails()
      .then((resp) => {
        setProfile(resp);
      })
      .catch((error) => console.log(error));
  }, []);


  const handleUserFieldChange = (fieldName, value) => {
      setProfile(prevState => ({
        ...prevState,
        user: {
          ...prevState.user,
          [fieldName]: value
        }
      }));
  };
  const handleStudentFieldChange = (fieldName, value) => {
      if (fieldName==='amount_elective' && ( isNaN(value) || (value < 1 || value > 6))){
        return;
      }
      setProfile(prevState => ({
        ...prevState,
        [fieldName]: value
      }));
  };

  const handleSaveChanges = () => {
    if (!profile.user.first_name || !profile.user.last_name) {
      alert("שם נדרש");
    }

    else {
      console.log("trying to save changes...")
      API.updateStudentDetails({ profile })
        .then((resp) => {
          localStorage.setItem('studentDetails', JSON.stringify(profile));
          alert(resp["message"]);
        })
        .catch((error) => console.log(error));
    }
  };

  return (
    <div className="homepage">
      <Navbar active="פרטים אישיים" />

      {profile ? (
        <div className="container">
          <div className="welcome-message">
            <h2>שלום, {profile.user.first_name}!</h2>
          </div>
          <div className="user-details-container">
            <div className="form-group row">
              <label className="col-sm-4 col-form-label">אימייל:</label>
              <div className="col-sm-8">
                <input
                  type="text"
                  className="form-control"
                  value={profile.user.email}
                  disabled

                />
              </div>
            </div>
            <div className="form-group row">
              <label className="col-sm-4 col-form-label">שם פרטי:</label>
              <div className="col-sm-8">
                <input
                  type="text"
                  className="form-control"
                  value={profile.user.first_name}
                  onChange={(e) => handleUserFieldChange('first_name', e.target.value)}
                  required
                />
              </div>
            </div>
            <div className="form-group row">
              <label className="col-sm-4 col-form-label">שם משפחה:</label>
              <div className="col-sm-8">
                <input
                  type="text"
                  className="form-control"
                  value={profile.user.last_name}
                  onChange={(e) => handleUserFieldChange('last_name', e.target.value)}
                />
              </div>
            </div>
            <div className="form-group row">
              <label className="col-sm-4 col-form-label">מסלול לימודים:</label>
                <div className="dropdown">
                <select name="program" value={profile.program} onChange={(e) => handleStudentFieldChange('program', parseInt(e.target.value))}>
                  <option value="1">אחר</option>
                  <option value="2">מצטיינים</option>
                </select>
            </div>
          </div>
            <div className="form-group row">
              <label className="col-sm-4 col-form-label">קורסי בחירה נדרשים:</label>
              <div className="col-sm-8">
                <input
                  type="number"
                  className="form-control"
                  value={profile.amount_elective}
                  min={1}
                  max={6}
                  onChange={(e) => handleStudentFieldChange('amount_elective', parseInt(e.target.value))}
                />
              </div>
            </div>
            
            <div className="form-group row">
              <div className="col-sm-12 text-center">
                <button className="btn btn-primary " onClick={handleSaveChanges}>
                  שמירת שינויים
                </button>
                <a href="/home"> <button className="btn btn-secondary ">
                  ביטול
                </button></a>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div class="d-flex justify-content-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default Homepage;
