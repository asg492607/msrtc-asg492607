# Environment Scheduling Policy

## Policy
All non-production Kubernetes environments (Development, Staging, QA) **must** be suspended during off-hours to prevent cloud waste.

## Implementation
Kubernetes `CronJobs` automatically execute:
* `suspend-environment.sh` on Friday at 6:00 PM (Scales all Deployments to 0 replicas).
* `resume-environment.sh` on Monday at 8:00 AM.

This single automation saves approximately 28% of total non-production compute costs monthly.
