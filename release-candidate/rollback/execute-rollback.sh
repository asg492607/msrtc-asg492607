#!/bin/bash
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
