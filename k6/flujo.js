import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 100,
  duration: '60s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
  insecureSkipTLSVerify: true,
};

export default function () {
  const home = http.get('https://hackathon.apioai.online/');
  check(home, {
    'home status 200': (r) => r.status === 200,
  });

  const hello = http.get('https://hackathon.apioai.online/api/hello');
  check(hello, {
    'hello status 200': (r) => r.status === 200,
  });
}
