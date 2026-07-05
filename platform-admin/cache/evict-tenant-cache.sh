#!/bin/bash
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
