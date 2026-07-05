#!/bin/bash
# Backup Redis Cache
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./archives/redis"
mkdir -p $BACKUP_DIR
BACKUP_FILE="$BACKUP_DIR/dump_$TIMESTAMP.rdb"

echo "Triggering Redis BGSAVE..."
docker exec -t msrtc-redis redis-cli BGSAVE

echo "Waiting for BGSAVE to complete (sleeping 5s)..."
sleep 5

echo "Copying dump.rdb from container..."
docker cp msrtc-redis:/data/dump.rdb $BACKUP_FILE

echo "Backup successful: $BACKUP_FILE"
