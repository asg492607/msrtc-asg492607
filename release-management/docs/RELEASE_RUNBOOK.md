# Release Runbook

## Overview
MSRTC utilizes **Argo Rollouts** to provide Zero-Downtime deployments. We no longer use standard Kubernetes `Deployments`; we use `Rollouts`.

## Canary Strategy
When a new container image is synced by ArgoCD:
1. **10% Traffic:** Argo spins up a small subset of the new Pods and routes 10% of live traffic to them.
2. **Analysis:** The `AnalysisTemplate` constantly queries Prometheus. If the HTTP 500 error rate spikes or latency drops below 95% success, Argo **automatically aborts and rolls back**.
3. **50% Traffic:** If healthy after 10 minutes, traffic shifts to 50%.
4. **100% Traffic:** If healthy, the old Pods are completely terminated.
