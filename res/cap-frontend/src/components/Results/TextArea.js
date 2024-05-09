import React from 'react';

function TextArea ({title, text, rows}) {

    return (
    
    <div className="m-4">
        <h4 className='text-center'>{title}</h4>
        <textarea rows={rows} className="form-control bg-white" readOnly value={text}/>
    </div>
    )
      

}
export default TextArea;