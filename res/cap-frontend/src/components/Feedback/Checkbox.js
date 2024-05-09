import React, { useState, useEffect } from 'react';

const Checkbox = ({ course, i, change }) => {
  const [is_checked, setisChecked] = useState(course.result);

  const handleOnChange = (e) => {
    const value =e.target.checked;
    setisChecked(value);
    change(value, i);
  };

  useEffect(() => {
    setisChecked(course.result);
  }, [course.result]);

  return (
   
    <div className="form-check">
        <input className="form-check-input" type="checkbox" checked={is_checked} id="flexCheckChecked" onChange={handleOnChange}/>
        <label className="form-check-label" htmlFor="flexCheckChecked">
        </label>
    </div>
  );
};

export default Checkbox;
