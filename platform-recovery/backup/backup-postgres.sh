#!/bin/bash
# Backup PostgreSQL Database
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./archives/postgres"
mkdir -p $BACKUP_DIR
BACKUP_FILE="$BACKUP_DIR/msrtc_db_$TIMESTAMP.sql.gz"

echo "Starting PostgreSQL backup..."
# Assuming a local docker container named msrtc-postgres
docker exec -t msrtc-postgres pg_dump -U postgres -d msrtc | gzip > $BACKUP_FILE

echo "Backup successful: $BACKUP_FILE"
