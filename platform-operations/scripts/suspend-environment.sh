#!/bin/bash
# Environment Suspension Script (Designed for Friday 6:00 PM CronJob)
set -e

NAMESPACE="msrtc-staging"
echo "Suspending all workloads in $NAMESPACE..."

# Scale Deployments to 0
kubectl scale deployment --all --replicas=0 -n $NAMESPACE

# Scale StatefulSets (if any) to 0
kubectl scale statefulset --all --replicas=0 -n $NAMESPACE

echo "Environment suspended. Cloud costs slashed."
