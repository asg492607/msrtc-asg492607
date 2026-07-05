import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp up to 50 users
    { duration: '1m', target: 50 },   // Stay at 50 users
    { duration: '10s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'], // Write operations must be < 300ms
  },
};

export default function () {
  const payload = JSON.stringify({
    routeId: 'MUM-PUN-101',
    seats: ['1A', '1B'],
    passengerDetails: [{ name: 'Test User', age: 30 }]
  });
  const headers = { 'Content-Type': 'application/json' };

  // Step 1: Create Booking
  const res = http.post('http://api.msrtc.internal/v1/bookings', payload, { headers });
  
  check(res, {
    'booking created successfully': (r) => r.status === 201,
  });
  sleep(1);
}
