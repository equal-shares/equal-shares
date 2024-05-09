import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react'
import App from '../../App';
import { BrowserRouter } from 'react-router-dom'
import { API } from '../../api-service';
import { act } from 'react-dom/test-utils';
import "regenerator-runtime/runtime.js";
import { setupFetchStub, compareElementsTextToArray } from '../TestUtils';
import { coursesDetailsTestJson } from './CoursesDetailsTestJson';
import { courseAData } from './CourseAData';
import { courseBData } from './CourseBData';

let appComponent;

beforeAll(() => {
  jest.spyOn(API, 'getCourse_group').mockImplementation(setupFetchStub(coursesDetailsTestJson));
  jest.spyOn(API, 'getCoursesA').mockImplementation(setupFetchStub(courseAData));
  jest.spyOn(API, 'getCoursesB').mockImplementation(setupFetchStub(courseBData));
  Object.defineProperty(window.document, 'cookie', {
    writable: true,
    value: 'mr-token=omnomnom',
  });
});

beforeEach(async () => {
  await act(async () => { appComponent = render(<BrowserRouter><App /></BrowserRouter>) });
});

afterEach(() => {
  appComponent.unmount();
});

test('click course', async () => {
  const courseGroups = screen.getAllByTestId('courseGroup');
  expect(courseGroups.length).toEqual(coursesDetailsTestJson.length);

  fireEvent.click(courseGroups[0]);
  const courseDetails = screen.getAllByTestId("courseDetails");
  expect(courseDetails.length).toEqual(2);

  expect(screen.getByTestId("selectedCourseName").textContent).toEqual("למידת מכונה")

  expect(screen.getByTestId("courseOption0").textContent).toEqual("אופצייה: 1");
  expect(screen.getByTestId("courseSemester0").textContent).toEqual("סמסטר: א");
  expect(screen.getByTestId("teacherName0").textContent).toEqual("שם המרצה: ליעד גוטליב");
  expect(screen.getByTestId("numOfStudents0").textContent).toEqual("מכסת סטודנטים: 30");
  expect(screen.getByTestId("courseDayOfWeek0").textContent).toEqual("יום בשבוע: א");
  expect(screen.getByTestId("hoursRange0").textContent).toEqual("שעות: 09:00:00-12:00:00");

  expect(screen.getByTestId("courseOption1").textContent).toEqual("אופצייה: 2");
  expect(screen.getByTestId("courseSemester1").textContent).toEqual("סמסטר: ב");
  expect(screen.getByTestId("teacherName1").textContent).toEqual("שם המרצה: ליעד גוטליב");
  expect(screen.getByTestId("numOfStudents1").textContent).toEqual("מכסת סטודנטים: 30");
  expect(screen.getByTestId("courseDayOfWeek1").textContent).toEqual("יום בשבוע: ב");
  expect(screen.getByTestId("hoursRange1").textContent).toEqual("שעות: 11:00:00-14:00:00");
})

test('toggle courses', async () => {
  const courseGroups = screen.getAllByTestId('courseGroup');
  expect(courseGroups.length).toEqual(coursesDetailsTestJson.length);

  fireEvent.click(courseGroups[0]);
  const courseDetails = screen.getAllByTestId("courseDetails");
  expect(courseDetails.length).toEqual(2);

  expect(screen.getByTestId("selectedCourseName").textContent).toEqual("למידת מכונה")
  expect(screen.getByTestId("courseSemester0").textContent).toEqual("סמסטר: א");
  expect(screen.getByTestId("teacherName0").textContent).toEqual("שם המרצה: ליעד גוטליב");

  fireEvent.click(courseGroups[5]);
  const sixthCourseDetails = screen.getAllByTestId("courseDetails");
  expect(sixthCourseDetails.length).toEqual(1);

  expect(screen.getByTestId("selectedCourseName").textContent).toEqual("למידה יישומית בראייה ממוחשבת")
  expect(screen.getByTestId("courseSemester0").textContent).toEqual("סמסטר: ב");
  expect(screen.getByTestId("teacherName0").textContent).toEqual("שם המרצה: גיל בן ארצי");
})

test('toggle between semesters', async () => {
  const userCoursesA = screen.getAllByTestId('userCourseId');
  expect(userCoursesA.length).toEqual(courseAData.length);
  compareElementsTextToArray(userCoursesA, courseAData.map(course => course.course_id))

  fireEvent.click(screen.getByTestId("semesterB"));
  const userCoursesB = screen.getAllByTestId('userCourseId');
  expect(userCoursesB.length).toEqual(courseBData.length);
  compareElementsTextToArray(userCoursesB, courseBData.map(course => course.course_id))
})