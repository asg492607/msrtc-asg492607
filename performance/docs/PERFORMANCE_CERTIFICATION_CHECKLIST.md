# Performance Certification Checklist

Before handing the backend platform over to the frontend team, the following tests MUST be certified passing.

## Mandatory Tests
- [ ] **Route Search Read Capacity:** Can sustain 10,000 TPS with P95 latency < 250ms (Cache hit ratio > 95%).
- [ ] **Booking Write Capacity:** Can sustain 1,000 TPS with P95 latency < 300ms (Saga pattern validates correctly).
- [ ] **Spike Tolerance:** Can absorb a sudden 10x traffic spike (e.g., Diwali release) without HPA thrashing.
- [ ] **Soak Test:** Platform runs at 50% capacity for 72 hours with NO memory leaks detected in Prometheus.

## Sign-Off
Any failure in the K6 pipeline strictly prevents a production release tag from being generated.
