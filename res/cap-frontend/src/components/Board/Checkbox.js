import React, { useState, useEffect } from 'react';

const Checkbox = ({ course, i, change }) => {
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
   
    <div className="form-check">
        <input className="form-check-input" type="checkbox" checked={is_checked} id="flexCheckChecked" onChange={handleOnChange}/>
        <label className="form-check-label" htmlFor="flexCheckChecked">
        מוכן/ה לקחת
        </label>
    </div>
  );
};

export default Checkbox;
