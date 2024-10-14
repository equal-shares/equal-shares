// All API requests

import { DataResponse, VoteRequestBody } from './schemas';
import { getConfig } from './config';

export async function postFakeDataRequest(email: string, token: string): Promise<DataResponse> {
  // Fake data for testing
  console.log(email, token);

  return Promise.resolve<DataResponse>({
    voted: false,
    max_total_points: 3000000,
    points_step: 1000,
    open_for_voting: true,
    results: {},
    note: '',
    projects: [...Array(20).keys()].map((i) => {
      return {
        id: i,
        name: `Project ${i}`,
        description_1: 'Description 1',
        description_2: 'Description 2',
        fixed: false,
        min_points: 1000,
        max_points: 3000000,
        rank: i,
        points: 0,
        points_text: '0',
        marked: false,
      };
    }),
  });
}

export async function postDataRequest(email: string, token: string): Promise<DataResponse> {
  const apiHost = getConfig().apiHost;
  const params = new URLSearchParams({ email, token });
  const response = await fetch(`${apiHost}/form/data?${params}`, {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    console.error('API request /form/data failed:', response);
    return Promise.reject(response);
  }

  const data = await response.json();

  return data;
}

export async function postVoteRequest(
  email: string,
  token: string,
  body: VoteRequestBody,
): Promise<DataResponse> {
  const apiHost = getConfig().apiHost;
  const params = new URLSearchParams({ email, token });
  const response = await fetch(`${apiHost}/form/vote?${params}`, {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    console.error('API request /form/vote failed:', response);
    return Promise.reject(response);
  }

  const data = await response.json();

  return data;
}
