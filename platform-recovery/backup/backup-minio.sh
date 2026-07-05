#!/bin/bash
# Backup MinIO Object Storage (requires MinIO Client 'mc')
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./archives/minio_$TIMESTAMP"
mkdir -p $BACKUP_DIR

echo "Starting MinIO mirror..."
# Assuming 'myminio' is configured locally
mc mirror myminio/msrtc-bucket $BACKUP_DIR

echo "Backup successful: $BACKUP_DIR"
