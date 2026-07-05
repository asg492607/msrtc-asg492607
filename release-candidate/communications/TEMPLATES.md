# Stakeholder Communication Templates

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
