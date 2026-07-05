# GitOps Workflow (ArgoCD)

## Overview
The MSRTC platform is deployed using a strict GitOps model. No engineer should ever run `kubectl apply` or `helm upgrade` against the production cluster. Instead, ArgoCD monitors this GitHub repository and automatically synchronizes the cluster state.

## How to Deploy a New Service
1. The CI pipeline builds the Docker image and tags it with the Git commit SHA (e.g., `ghcr.io/msrtc/booking-service:abc1234`).
2. The CI pipeline automatically updates the `helm/environments/production/values-booking-service.yaml` file with the new image tag and commits it back to GitHub.
3. ArgoCD detects the commit on the `main` branch.
4. ArgoCD triggers a rolling deployment in the Kubernetes cluster.

## Universal Helm Chart
Instead of 20 different sets of YAML files, we use the universal `helm/msrtc-service` chart.
To configure a specific microservice, you simply provide a `values-<service-name>.yaml` file that overrides the defaults.

Example `values-api-gateway.yaml`:
```yaml
replicaCount: 3
image:
  repository: ghcr.io/msrtc/api-gateway
ingress:
  enabled: true
  hosts:
    - host: api.msrtc.gov.in
```
