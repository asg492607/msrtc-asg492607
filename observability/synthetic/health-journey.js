import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1, // Single virtual user for health checking
  duration: '1m',
};

export default function () {
  // Simulate a user checking routes
  const res = http.get('http://api.msrtc.internal/v1/routes?source=MUM&destination=PUNE');
  check(res, {
    'status was 200': (r) => r.status == 200,
    'transaction time OK': (r) => r.timings.duration < 500,
  });
  sleep(5); // Run every 5 seconds
}
