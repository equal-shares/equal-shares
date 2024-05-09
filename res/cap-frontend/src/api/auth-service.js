import Cookies from 'js-cookie';

import dotenv from 'dotenv';
dotenv.config();


const BASE_URL= process.env.REACT_APP_BASE_URL;

export class API_AUTH {
    static VerifyRegistration(body)
    {
        return fetch(BASE_URL+"api/accounts/verify-registration/",
        {
            method: 'POST',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }

    static RegisterUser(body)
    {
        return fetch(BASE_URL+"api/accounts/register/",
        {
            method: 'POST',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }

    
    static LoginUser(body)
    {
        return fetch(BASE_URL+"api/accounts/login/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }

    static LogoutUser()
    {
        return fetch(BASE_URL+"api/accounts/logout/",
        {
            method: 'POST',
            credentials: 'include',
            headers: 
            {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken')
            },
        })
        .then(resp => resp.json())
    }

    static SendResetPasswordLink(body)
    {
        return fetch(BASE_URL+"api/accounts/send-reset-password-link/",
        {
            method: 'POST',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }

    static ResetPassword(body)
    {
        return fetch(BASE_URL+"api/accounts/reset-password/",
        {
            method: 'POST',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(resp => resp.json())
    }
   
}