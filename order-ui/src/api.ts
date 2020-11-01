import axios, { AxiosResponse } from 'axios';
import { join } from '@fireflysemantics/join';

import { PayloadType } from '@/types';

const origin = 'http://localhost:3000';
const plannerPath = '/api/v1/planning';

export function postShipment(payload: PayloadType): void {
  const url = join(origin, plannerPath);
  console.log(url);
  axios.post(url, payload).then(() => {
    payload.success();
  }).catch((err: {response: AxiosResponse}) => {
    payload.failure(`error occured when accesing ${url}, status_code=${err.response.status}`);
  });
}
