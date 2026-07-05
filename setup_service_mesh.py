import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
mesh_dir = os.path.join(base_dir, "service-mesh")

dirs = [
    "mtls",
    "authorization",
    "virtual-services",
    "destination-rules",
    "gateways",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(mesh_dir, d), exist_ok=True)

# 1. mTLS Configuration
mtls_yaml = """apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: msrtc-prod
spec:
  mtls:
    mode: STRICT
"""
with open(os.path.join(mesh_dir, "mtls/peer-authentication.yaml"), "w", encoding="utf-8") as f: f.write(mtls_yaml)


# 2. Authorization Policies (Zero Trust)
auth_yaml = """apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: booking-service-auth
  namespace: msrtc-prod
spec:
  selector:
    matchLabels:
      app: booking-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/msrtc-prod/sa/api-gateway"]
    to:
    - operation:
        methods: ["GET", "POST"]
"""
with open(os.path.join(mesh_dir, "authorization/booking-service-auth.yaml"), "w", encoding="utf-8") as f: f.write(auth_yaml)


# 3. Virtual Service (Traffic Routing)
vs_yaml = """apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: booking-service
  namespace: msrtc-prod
spec:
  hosts:
  - booking-service.msrtc-prod.svc.cluster.local
  http:
  - route:
    - destination:
        host: booking-service.msrtc-prod.svc.cluster.local
        subset: v1
      weight: 90
    - destination:
        host: booking-service.msrtc-prod.svc.cluster.local
        subset: v2
      weight: 10
    retries:
      attempts: 3
      perTryTimeout: 2s
"""
with open(os.path.join(mesh_dir, "virtual-services/booking-service.yaml"), "w", encoding="utf-8") as f: f.write(vs_yaml)


# 4. Destination Rule (Circuit Breaking & Outlier Detection)
dr_yaml = """apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: booking-service
  namespace: msrtc-prod
spec:
  host: booking-service.msrtc-prod.svc.cluster.local
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
"""
with open(os.path.join(mesh_dir, "destination-rules/booking-service.yaml"), "w", encoding="utf-8") as f: f.write(dr_yaml)


# 5. Gateway
gw_yaml = """apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: msrtc-gateway
  namespace: msrtc-prod
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "api.msrtc.gov.in"
"""
with open(os.path.join(mesh_dir, "gateways/msrtc-gateway.yaml"), "w", encoding="utf-8") as f: f.write(gw_yaml)


# 6. Documentation
docs = """# Service Mesh Runbook (Istio)

## Overview
MSRTC utilizes Istio to decouple network security, routing, and observability from application code. Every pod receives an Envoy proxy sidecar.

## Zero-Trust Architecture
* **STRICT mTLS:** All service-to-service traffic is encrypted. Plaintext requests are rejected by the sidecar.
* **Authorization:** The `booking-service` will ONLY accept traffic if the TLS certificate originates from the `api-gateway` ServiceAccount.

## Traffic Management
Argo Rollouts (Task 39) manages the *Deployments*, but Istio `VirtualServices` and `DestinationRules` manage the *Traffic*.
If you need to manually force traffic to a specific version, modify `service-mesh/virtual-services/booking-service.yaml`.
"""
with open(os.path.join(mesh_dir, "docs/SERVICE_MESH_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(docs)

print("Service Mesh Scaffolded")
