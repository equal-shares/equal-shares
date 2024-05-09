import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react'
import Office from '../../components/Office/Office';
import { BrowserRouter } from 'react-router-dom'
import { API } from '../../api-service';
import { act } from 'react-dom/test-utils';
import "regenerator-runtime/runtime.js";
import { setupFetchStub } from '../TestUtils';

let officeComponent;

beforeAll(() => {
    jest.spyOn(global, 'alert').mockImplementation(() => { });
    Object.defineProperty(window.document, 'cookie', {
        writable: true,
        value: 'mr-token=omnomnom',
    });
});

beforeEach(async () => {
    await act(async () => { officeComponent = render(<BrowserRouter><Office /></BrowserRouter>) });
});

afterEach(() => {
    officeComponent.unmount();
});

test('change dates', () => {
    fireEvent.change(screen.getByTestId("start_date_field"), { target: { value: "2021-01-30" } });
    fireEvent.change(screen.getByTestId("end_date_field"), { target: { value: "2021-01-31" } })
    fireEvent.click(screen.getByTestId("save_button"));
    expect(global.alert).toBeCalledWith("התאריכים נרשמו במערכת");
});

test('upload file', () => {
    expect(screen.getByTestId("lastModifiedOfFile").textContent).toEqual("עדיין לא הועלה אף קובץ");
    fireEvent.change(screen.getByTestId("fileUpload"), {
        target: {
            files: [
                {
                    lastModifiedDate: new Date("Sat Apr 17 2021 19:13:25 GMT+0300 (Israel Daylight Time)")
                }
            ]
        }
    })
    expect(screen.getByTestId("lastModifiedOfFile").textContent).toEqual("Last Modified: Sat Apr 17 2021");
});
