# Production Readiness Checklist

This checklist MUST be 100% completed before any cutover to the Production environment.

## 1. Infrastructure & Networking
- [ ] Kubernetes clusters (EKS/GKE) are provisioned across 3 Availability Zones.
- [ ] Istio Service Mesh is enforcing STRICT mTLS globally.
- [ ] Terraform state is remote and locked.

## 2. Security & Compliance
- [ ] Kyverno policies are active (Root user disabled, etc.).
- [ ] Automated secret rotation is configured.
- [ ] All CI/CD pipelines require successful SAST/DAST scans to merge.

## 3. Reliability & Observability
- [ ] Prometheus, Grafana, Jaeger, and Loki are receiving telemetry.
- [ ] Alertmanager is configured to page PagerDuty/Slack for critical incidents.
- [ ] Litmus Chaos tests passed on Staging.
- [ ] K6 Performance tests passed on Staging (P95 Booking Latency < 300ms).

## 4. Disaster Recovery
- [ ] PostgreSQL point-in-time recovery (PITR) has been successfully tested.
- [ ] Kafka cluster can survive a broker loss without dropping messages.
