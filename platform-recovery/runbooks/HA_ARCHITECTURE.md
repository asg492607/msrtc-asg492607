# High Availability (HA) Architecture

## Overview
To prevent a single point of failure (SPOF) within the MSRTC platform, the following topology must be utilized in the production environment.

## Topology
1. **Load Balancer:** AWS ALB / NGINX Ingress Controller.
2. **API Gateways:** Minimum of 3 replicas distributed across Availability Zones.
3. **Microservices:** All 20 NestJS microservices must run a minimum of 2 Pods in a Kubernetes Cluster, auto-scaled based on CPU/Memory utilization.
4. **PostgreSQL:** Primary/Replica cluster (e.g. AWS RDS Multi-AZ). Read-heavy workloads should hit the Replica.
5. **Redis:** Redis Cluster or Sentinel setup spanning multiple AZs.
6. **Kafka:** Minimum 3-broker cluster with a replication factor of 3 and `min.insync.replicas=2`.

## Network Isolation
* Database and Cache layers must reside in Private Subnets.
* Only the API Gateway is exposed to the Public Internet.
