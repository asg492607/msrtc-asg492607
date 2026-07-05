#!/bin/bash
# Toggle a Global Feature Flag
set -e

FLAG_NAME=$1
STATUS=$2 # 'enable' or 'disable'

if [ -z "$FLAG_NAME" ] || [ -z "$STATUS" ]; then
  echo "Usage: ./toggle-feature.sh <flag-name> <enable|disable>"
  exit 1
fi

echo "Connecting to Feature Flag Service (Redis)..."
# Simulated Redis CLI command to update flag state globally
# redis-cli -h redis-cluster.msrtc-prod.svc.cluster.local set "feature:${FLAG_NAME}" "${STATUS}"

echo "Feature '${FLAG_NAME}' has been ${STATUS}d globally."
