import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '30s', target: 200 },
    { duration: '30s', target: 500 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
  insecureSkipTLSVerify: true,
};

export default function () {
  const res = http.get('https://hackathon.apioai.online/health');
  check(res, {
    'status 200': (r) => r.status === 200,
    'body contiene "ok"': (r) => r.body && r.body.includes('ok'),
  });
}
