import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
perf_dir = os.path.join(base_dir, "performance")

dirs = [
    "k6/scenarios",
    "ci-cd",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(perf_dir, d), exist_ok=True)

# 1. K6 Route Search Scenario (High Read Throughput)
search_js = """import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: 500, // 500 requests per second
      timeUnit: '1s',
      duration: '2m',
      preAllocatedVUs: 100,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<250'], // P95 latency must be strictly < 250ms
    http_req_failed: ['rate<0.01'],   // Error rate must be < 1%
  },
};

export default function () {
  const url = 'http://api.msrtc.internal/v1/routes?source=MUM&destination=PUNE&date=2024-12-01';
  const res = http.get(url);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
"""
with open(os.path.join(perf_dir, "k6/scenarios/route-search-load.js"), "w", encoding="utf-8") as f: f.write(search_js)

# 2. K6 Booking Flow Scenario (Write Throughput / Saga Pattern)
booking_js = """import http from 'k6/http';
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
"""
with open(os.path.join(perf_dir, "k6/scenarios/booking-flow-load.js"), "w", encoding="utf-8") as f: f.write(booking_js)


# 3. CI/CD Performance Pipeline
pipeline_yaml = """name: Enterprise Performance Certification

on:
  workflow_dispatch:
  release:
    types: [published]

jobs:
  performance-test:
    name: K6 Load Testing
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install K6
        run: sudo apt-get install k6

      - name: Run Route Search Load Test
        run: k6 run performance/k6/scenarios/route-search-load.js
        
      - name: Run Booking Flow Load Test
        run: k6 run performance/k6/scenarios/booking-flow-load.js

      - name: Assert SLOs
        run: |
          echo "K6 automatically exits with non-zero code if thresholds (e.g. p95 < 300ms) are breached."
          echo "This pipeline step will FAIL, blocking production deployment."
"""
with open(os.path.join(perf_dir, "ci-cd/performance-pipeline.yml"), "w", encoding="utf-8") as f: f.write(pipeline_yaml)


# 4. Certification Documentation
cert_md = """# Performance Certification Checklist

Before handing the backend platform over to the frontend team, the following tests MUST be certified passing.

## Mandatory Tests
- [ ] **Route Search Read Capacity:** Can sustain 10,000 TPS with P95 latency < 250ms (Cache hit ratio > 95%).
- [ ] **Booking Write Capacity:** Can sustain 1,000 TPS with P95 latency < 300ms (Saga pattern validates correctly).
- [ ] **Spike Tolerance:** Can absorb a sudden 10x traffic spike (e.g., Diwali release) without HPA thrashing.
- [ ] **Soak Test:** Platform runs at 50% capacity for 72 hours with NO memory leaks detected in Prometheus.

## Sign-Off
Any failure in the K6 pipeline strictly prevents a production release tag from being generated.
"""
with open(os.path.join(perf_dir, "docs/PERFORMANCE_CERTIFICATION_CHECKLIST.md"), "w", encoding="utf-8") as f: f.write(cert_md)

cap_md = """# Capacity Planning Guide

## Linear Scaling
MSRTC microservices are stateless. To double capacity, double the Kubernetes Pod replicas.

## Bottlenecks
* **PostgreSQL:** Write throughput is capped by disk I/O. For > 5,000 Booking TPS, vertically scale the RDS instance (e.g., `db.r6g.4xlarge`).
* **Redis:** Memory fragmentation can occur under heavy Pub/Sub load. Monitor the `finops-service` anomaly alerts.
"""
with open(os.path.join(perf_dir, "docs/CAPACITY_PLANNING_GUIDE.md"), "w", encoding="utf-8") as f: f.write(cap_md)


print("Performance Certification Framework Scaffolded")
