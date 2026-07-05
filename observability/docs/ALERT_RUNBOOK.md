# Alert Runbook

## HighErrorRate (HTTP 5xx > 5%)
1. Open the Grafana **Service Mesh Dashboard**.
2. Identify the specific microservice throwing 5xx errors.
3. Open Jaeger, filter by that service and `error=true`.
4. Look at the trace span to see if the database or Redis failed.
5. If it's a code regression from a recent deployment, trigger an Argo Rollout rollback.
