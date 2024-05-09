// All API requests

import { DataResponse, VoteRequestBody } from './schemas';
import { getConfig } from './config';

export async function postDataRequest(email: string, token: string): Promise<DataResponse> {
  const apiHost = getConfig().apiHost;
  const params = new URLSearchParams({ email, token });
  const response = await fetch(`${apiHost}/form/data?${params}`, {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    }
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
  body: VoteRequestBody
): Promise<DataResponse> {
  const apiHost = getConfig().apiHost;
  const params = new URLSearchParams({ email, token });
  const response = await fetch(`${apiHost}/form/vote?${params}`, {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    console.error('API request /form/vote failed:', response);
    return Promise.reject(response);
  }

  const data = await response.json();

  return data;
}
