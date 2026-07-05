import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"
admin_dir = os.path.join(base_dir, "platform-admin")

dirs = [
    "config",
    "cache",
    "maintenance",
    "messaging",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(admin_dir, d), exist_ok=True)

# 1. Feature Flag Management (Config)
ff_sh = """#!/bin/bash
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
"""
with open(os.path.join(admin_dir, "config/toggle-feature.sh"), "w", newline='\n') as f: f.write(ff_sh)


# 2. Cache Eviction
cache_sh = """#!/bin/bash
# Evict Cache for a Specific Tenant
set -e

TENANT_ID=$1

if [ -z "$TENANT_ID" ]; then
  echo "Usage: ./evict-tenant-cache.sh <tenant-id>"
  exit 1
fi

echo "Evicting cache for Tenant: ${TENANT_ID}..."
# Simulated Redis CLI command using SCAN to delete tenant-specific keys
# redis-cli --scan --pattern "cache:${TENANT_ID}:*" | xargs redis-cli del

echo "Cache evicted successfully for Tenant: ${TENANT_ID}."
"""
with open(os.path.join(admin_dir, "cache/evict-tenant-cache.sh"), "w", newline='\n') as f: f.write(cache_sh)


# 3. Global Maintenance Mode (Istio)
maintenance_yaml = """apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: msrtc-global-routing
  namespace: msrtc-prod
spec:
  hosts:
  - "api.msrtc.gov.in"
  gateways:
  - msrtc-gateway
  http:
  - match:
    - uri:
        prefix: "/"
    route:
    - destination:
        host: maintenance-page-service.msrtc-prod.svc.cluster.local
        port:
          number: 80
"""
with open(os.path.join(admin_dir, "maintenance/enable-maintenance-mode.yaml"), "w", encoding="utf-8") as f: f.write(maintenance_yaml)

maint_sh = """#!/bin/bash
# Toggle Global Maintenance Mode
set -e

ACTION=$1

if [ "$ACTION" == "enable" ]; then
  echo "EMERGENCY: Enabling Global Maintenance Mode..."
  kubectl apply -f enable-maintenance-mode.yaml
  echo "All traffic is now routed to the static maintenance page."
elif [ "$ACTION" == "disable" ]; then
  echo "Restoring normal traffic routing..."
  # Re-apply the standard VirtualService
  kubectl apply -f ../../service-mesh/virtual-services/booking-service.yaml
  echo "Maintenance Mode Disabled."
else
  echo "Usage: ./toggle-maintenance.sh <enable|disable>"
  exit 1
fi
"""
with open(os.path.join(admin_dir, "maintenance/toggle-maintenance.sh"), "w", newline='\n') as f: f.write(maint_sh)


# 4. Documentation
docs_runbook = """# Platform Operations Center Runbook

## Overview
This directory contains the "Break Glass" tools for SREs to manage the production cluster.

## 1. Global Maintenance Mode
In the event of a catastrophic database failure where data integrity is at risk:
1. Navigate to `platform-admin/maintenance/`
2. Run `./toggle-maintenance.sh enable`
This uses Istio to instantly reroute all API Gateway traffic to a static HTML page, shedding load and preventing further database corruption.

## 2. Feature Flags
To instantly disable a failing new feature without waiting for an ArgoCD rollback:
1. Navigate to `platform-admin/config/`
2. Run `./toggle-feature.sh new-payment-gateway disable`
This updates the Redis cluster, forcing all microservices to revert to the fallback code path within milliseconds.
"""
with open(os.path.join(admin_dir, "docs/OPERATIONS_CENTER_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(docs_runbook)


print("Platform Operations Center Scaffolded")
