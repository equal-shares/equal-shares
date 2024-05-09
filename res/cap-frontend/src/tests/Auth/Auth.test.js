import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { API } from '../../api-service';
import { act } from 'react-dom/test-utils';
import "regenerator-runtime/runtime.js";
import { setupFetchStub } from '../TestUtils';
import Auth from '../../auth';

let authComponent;
describe("my asynchronous testsa", () => {

    beforeAll(() => {
        jest.spyOn(API, 'loginUser').mockImplementation(loginMock);
        global.window = Object.create(window);
        const url = "http://dummy.com";
        Object.defineProperty(window, 'location', {
            value: {
                href: url
            }
        });
    });

    beforeEach(async () => {
        jest.spyOn(global, 'alert').mockImplementation(() => { });
        await act(async () => { authComponent = render(<BrowserRouter><Auth /></BrowserRouter>) });
    });

    afterEach(() => {
        authComponent.unmount();
    });

    test('empty user and password', () => {
        fireEvent.click(screen.getByTestId("loginButton"));
        expect(global.alert).toBeCalledWith("שם משתמש או סיסמא ריקים");
    })

    test('empty password', () => {
        fireEvent.change(screen.getByTestId("username"), { target: { value: 'gjkjhk' } })
        fireEvent.click(screen.getByTestId("loginButton"));
        expect(global.alert).toBeCalledWith("שם משתמש או סיסמא ריקים");
    })

    test('empty user', () => {
        fireEvent.change(screen.getByTestId("password"), { target: { value: 'gjkjhk' } })
        fireEvent.click(screen.getByTestId("loginButton"));
        expect(global.alert).toBeCalledWith("שם משתמש או סיסמא ריקים");
    })

    test('correct user', async () => {
        fireEvent.change(screen.getByTestId("username"), { target: { value: 'a' } })
        fireEvent.change(screen.getByTestId("password"), { target: { value: 'b' } })
        await act(async () => { fireEvent.click(screen.getByTestId("loginButton")) });
        expect(window.location.href).toEqual("/courses_info");
    })
})

function loginMock(userData) {
    if (userData.username === 'a' && userData.password === 'b') {
        return setupFetchStub({ token: 'IAmAUser' })()
    }
    else {
        return setupFetchStub({})()
    }
}