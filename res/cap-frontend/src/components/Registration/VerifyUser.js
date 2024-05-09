import React, { useEffect } from 'react';
import { useLocation } from "react-router-dom"
import logo1 from '../../logo.png';
import {API_AUTH} from '../../api/auth-service'

function VerifyUser() {
    const location = useLocation()
    const params = new URLSearchParams(location.search)
  

    useEffect(() => {
        const body = {
            'user_id': params.get('user_id'),
            'timestamp': params.get('timestamp'),
            'signature' :params.get('signature')
        }
        API_AUTH.VerifyRegistration(body)
        .then(resp => {
            console.log(resp)
        })
        .catch(error => console.log(error))
    })


    return (
        <div className='text-center'>
            <img className="mb-4" src={logo1} alt="" width="75" height="65" />
            <h1>חשבונך אומת בהצלחה</h1>
            <a href="/">
                <button className='btn btn-primary'>מעבר להתחברות</button>
            </a>
      </div>
    )
}

export default VerifyUser;