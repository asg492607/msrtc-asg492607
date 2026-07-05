#!/bin/bash
# Storage Lifecycle Automation
set -e

echo "Cleaning up Postgres archives older than 30 days..."
# Simulating cleanup of old backups
find /var/backups/postgres -type f -mtime +30 -name '*.sql.gz' -exec rm {} \;

echo "Storage lifecycle complete."
