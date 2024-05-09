import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react'
import Ranking from '../../components/Ranking/Ranking';
import { BrowserRouter } from 'react-router-dom'
import { API } from '../../api-service';
import { act } from 'react-dom/test-utils';
import "regenerator-runtime/runtime.js";
import { setupFetchStub, compareElementsTextToArray } from '../TestUtils';
import { rankingTestJson } from './RankingJson';

let rankingComponent;

beforeAll(() => {
  jest.spyOn(API, 'getLast_ranking').mockImplementation(setupFetchStub(rankingTestJson));
  Object.defineProperty(window.document, 'cookie', {
    writable: true,
    value: 'mr-token=omnomnom',
  });
});

beforeEach(async () => {
  await act(async () => { rankingComponent = render(<BrowserRouter><Ranking /></BrowserRouter>) });
});

afterEach(() => {
  rankingComponent.unmount();
});

test('rank courses', async () => {
  compareElementsTextToArray(screen.getAllByTestId('groupName'), rankingTestJson.map(course => course.name));
  expect(screen.queryByTestId('editableCard')).toBeNull;
  expect(screen.queryByTestId('card')).not.toBeNull;

  await act(async () => { fireEvent.click(screen.getByTestId("editButton")) });
  expect(screen.queryByTestId('editButton')).toBeNull;
  expect(screen.queryByTestId('saveButton')).not.toBeNull;
  expect(screen.queryByTestId('editableCard')).not.toBeNull;
  expect(screen.queryByTestId('card')).toBeNull;

  // let startDragZone = screen.getAllByTestId('groupName')[0];
  // let endDropZone = screen.getByTestId('dragAndDropCourse5');

  // fireEvent.dragStart(startDragZone);
  // fireEvent.dragEnter(endDropZone);
  // fireEvent.dragOver(endDropZone);
  // fireEvent.drop(endDropZone);
  // expect(screen.getAllByTestId('groupName')[0].textContent).toEqual(rankingTestJson[1].name);
})