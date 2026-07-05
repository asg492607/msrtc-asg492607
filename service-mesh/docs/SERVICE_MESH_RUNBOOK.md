# Service Mesh Runbook (Istio)

## Overview
MSRTC utilizes Istio to decouple network security, routing, and observability from application code. Every pod receives an Envoy proxy sidecar.

## Zero-Trust Architecture
* **STRICT mTLS:** All service-to-service traffic is encrypted. Plaintext requests are rejected by the sidecar.
* **Authorization:** The `booking-service` will ONLY accept traffic if the TLS certificate originates from the `api-gateway` ServiceAccount.

## Traffic Management
Argo Rollouts (Task 39) manages the *Deployments*, but Istio `VirtualServices` and `DestinationRules` manage the *Traffic*.
If you need to manually force traffic to a specific version, modify `service-mesh/virtual-services/booking-service.yaml`.
