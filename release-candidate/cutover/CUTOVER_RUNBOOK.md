# Production Blue/Green Cutover Runbook

## Phase 1: Deploy Green (Background)
1. ArgoCD syncs the Release Candidate tag to the `msrtc-prod` namespace.
2. Argo Rollouts deploys the new pods alongside the existing pods.
3. **Traffic:** 100% of external traffic remains on the old (Blue) pods.

## Phase 2: Smoke Testing
1. Execute the OAT Postman collection against the internal Green service endpoint.
2. Verify database migrations completed successfully without locking core tables.

## Phase 3: Traffic Shifting (Canary)
1. Instruct Argo Rollouts to shift 10% of traffic to the Green environment.
2. **Monitor:** Watch the `HighErrorRate` Prometheus alert for 15 minutes.

## Phase 4: Full Cutover
1. If SLOs are stable, promote Argo Rollouts to 100%.
2. The old Blue pods scale down after a 30-minute grace period.
