#!/bin/bash
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
