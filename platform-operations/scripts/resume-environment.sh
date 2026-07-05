#!/bin/bash
# Environment Resume Script (Designed for Monday 8:00 AM CronJob)
set -e

NAMESPACE="msrtc-staging"
echo "Resuming all workloads in $NAMESPACE..."

# Wake up Deployments (Rely on HPA to scale up from 1 to required)
kubectl scale deployment --all --replicas=1 -n $NAMESPACE

echo "Environment resumed."
