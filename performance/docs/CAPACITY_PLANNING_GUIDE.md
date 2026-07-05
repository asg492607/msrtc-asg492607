# Capacity Planning Guide

## Linear Scaling
MSRTC microservices are stateless. To double capacity, double the Kubernetes Pod replicas.

## Bottlenecks
* **PostgreSQL:** Write throughput is capped by disk I/O. For > 5,000 Booking TPS, vertically scale the RDS instance (e.g., `db.r6g.4xlarge`).
* **Redis:** Memory fragmentation can occur under heavy Pub/Sub load. Monitor the `finops-service` anomaly alerts.
