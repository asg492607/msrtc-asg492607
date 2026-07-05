# Platform Operations Center Runbook

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
