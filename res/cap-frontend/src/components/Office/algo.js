import React, { useState, useEffect } from 'react';
import NavbarOffice from './Navbar_Office';
import { API } from '../../api/api-service';

import './office.css'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";


function Algo(props)
{
    const [close, setClose] = useState(false);
    const [loading, setLoading] = useState(false);
    
    const algo = () => {
        setLoading(true);
        API.doAlgo()
        .then(resp => {
            setLoading(false);
            alert(resp)})
        .catch(error => console.log(error))
    };

    useEffect( () => {
        //if(!token['mr-token']) window.location.href = '/';
        API.studentOrOffice()
        .then(resp => {                
            if(resp === 1) //student
                window.location.href = '/courses_info';
            if(resp === 3) //error
                alert("error")
        })
        .catch(error => console.log(error))
        API.isClose()
        .then(resp => setClose(resp))
        .catch(error => console.log(error))
    }, [])

    


    return(
        <div className="office" data-testid="office">
        <NavbarOffice active='אישורים' />
        <header className="App-header">
          <div className="headline">ברוכים/ות הבאים/ות </div>
        </header>
        <div className='container-office'>
          <div className='layout-office'>
            <h2 style={{marginRight: '20%',color:'white'}}> : ביצוע חלוקה הוגנת </h2>
            <div className='fill-in-office'>
                {!close &&  <h4>ההרשמה טרם נסגרה, ניתן להריץ את האלגוריתם רק בסיומה </h4>}
                {close &&
                <div>
                     <h4>שימ/י לב תהליך זה לוקח מספר שניות *</h4>
                     <div style={{marginRight:'30%'}}>
                        {loading && <Loader type="audio" color="#00BFFF" height={100} width={200}   />}
                        {!loading && <button className="btn-algo" style={{}} onClick={algo} >הרץ אלגוריתם</button>}
                     </div>

                </div>
                }


            </div>

          </div>
        </div>


      </div>
    );
    
    
    
}

export default Algo;