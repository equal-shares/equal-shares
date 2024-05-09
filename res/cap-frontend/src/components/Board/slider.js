import React, { useState, useEffect } from 'react';

const Slider = ({ course, i, balance, change }) => {
  const [value, setValue] = useState(course.score);
  const handleOnChange = (e) => {
    const value = e.target.value;
    const diff = value - course.score;
    if (diff>0 && (balance-diff)<0) {
      if (balance>0){
        const max_value = course.score+balance
        setValue(max_value)
        change(course.score+balance, i);
      }
      return;
    }
    setValue(value);
    change(value, i);
  };

  useEffect(() => {
    setValue(course.score);
  }, [course.score]);

  return (
   
    <div className="slide"> 
     <div className="value" style={{ fontSize: "1.3em"}}>{value}</div>
      <input
        type="range"
        min={0}
        max={1000}
        value={value}
        className="slider"
        onChange={handleOnChange}
        disabled={!course.is_acceptable}
      /> 
    </div>
  );
};

export default Slider;
