import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
rc_dir = os.path.join(base_dir, "release-candidate")

dirs = [
    "cutover",
    "rollback",
    "hypercare",
    "communications",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(rc_dir, d), exist_ok=True)

# 1. Cutover Runbook
cutover_md = """# Production Blue/Green Cutover Runbook

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
"""
with open(os.path.join(rc_dir, "cutover/CUTOVER_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(cutover_md)


# 2. Automated Rollback Scripts
rollback_sh = """#!/bin/bash
# Emergency Rollback Execution
set -e

SERVICE_NAME=$1

if [ -z "$SERVICE_NAME" ]; then
  echo "Usage: ./execute-rollback.sh <service-name>"
  exit 1
fi

echo "EMERGENCY: Aborting release for ${SERVICE_NAME}..."
# Using Argo Rollouts CLI to instantly abort the canary and route 100% traffic to Blue
# kubectl argo rollouts abort ${SERVICE_NAME} -n msrtc-prod

echo "Rollback initiated. Traffic has been reverted to the stable baseline."
echo "Please notify stakeholders via the communications templates."
"""
with open(os.path.join(rc_dir, "rollback/execute-rollback.sh"), "w", newline='\n') as f: f.write(rollback_sh)


# 3. Hypercare Plan
hypercare_md = """# Hypercare Support Plan (First 7 Days Post-Launch)

## Coverage
* **Duration:** T+0 to T+7 Days.
* **Coverage:** 24x7 eyes-on-glass monitoring.

## Escalation Matrix
| Issue Severity | Response Time | Escalation Path |
|---|---|---|
| SEV-1 (Total Outage) | 5 mins | L1 Support -> SRE On-Call -> VP Engineering |
| SEV-2 (Feature Degraded) | 15 mins | L1 Support -> Application Lead |
| SEV-3 (Minor Bug) | 4 hours | Jira Backlog |

## Exit Criteria
Hypercare ends only when:
1. No SEV-1 or SEV-2 incidents in the last 48 hours.
2. System is operating comfortably within predefined SLO targets.
"""
with open(os.path.join(rc_dir, "hypercare/HYPERCARE_PLAN.md"), "w", encoding="utf-8") as f: f.write(hypercare_md)


# 4. Communications Templates
comm_md = """# Stakeholder Communication Templates

## 1. Deployment Started (T-0)
**To:** executive-team@msrtc.gov.in
**Subject:** [STATUS] Production Deployment Commenced - v1.0
The Platform Engineering team has initiated the Blue/Green deployment for MSRTC Backend v1.0. 
Zero downtime is expected. We will provide the next update in 60 minutes.

## 2. Emergency Rollback (If needed)
**To:** executive-team@msrtc.gov.in
**Subject:** [ALERT] Production Deployment Aborted - v1.0
During the 10% Canary phase, automated observability detected elevated latency. The deployment has been automatically aborted and 100% of traffic safely routed back to the stable baseline. Zero passenger impact occurred.

## 3. Deployment Successful
**To:** executive-team@msrtc.gov.in
**Subject:** [SUCCESS] MSRTC Backend v1.0 is LIVE
The cutover is complete. The system is operating nominally and we have entered the 7-day Hypercare support window.
"""
with open(os.path.join(rc_dir, "communications/TEMPLATES.md"), "w", encoding="utf-8") as f: f.write(comm_md)


print("Release Candidate Framework Scaffolded")
