import React, { useState, useEffect } from 'react';

const Switch = ({ course, i, change }) => {
  const [is_checked, setisChecked] = useState(course.is_acceptable);
  const handleOnChange = (e) => {
    const value =e.target.checked;
    setisChecked(value);
    change(value, i);
  };

  useEffect(() => {
    setisChecked(course.is_acceptable);
  }, [course.is_acceptable]);

  return (
   
    <div className="form-check form-switch end-50">
    <input className="form-check-input" type="checkbox" id="flexSwitchCheckDefault" checked={is_checked} onChange={handleOnChange}/>
    <label className="form-check-label" htmlFor="flexSwitchCheckDefault" >אופציונאלי</label>
  </div>
  );
};

export default Switch;
