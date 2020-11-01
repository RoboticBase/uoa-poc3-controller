import axios, { AxiosResponse } from 'axios';
import { join } from '@fireflysemantics/join';

import { PayloadType } from '@/types';

const origin = process.env.VUE_APP_APIHOST;
const token = process.env.VUE_APP_APITOKEN || 'dummyToken';
const plannerPath = '/api/v1/planning';

export function postShipment(payload: PayloadType): void {
  const url = join(origin, plannerPath);
  const headers: { [key: string]: string } = {
    'Authorization': token,
  };
  axios.post(url, payload, {
    headers: headers,
  }).then(() => {
    payload.success();
  }).catch((err: {response: AxiosResponse}) => {
    payload.failure(`error occured when accesing ${url}, status_code=${err.response.status}`);
  });
}
