#!/bin/bash
# Restore Redis Cache
set -e

if [ -z "$1" ]; then
  echo "Usage: ./restore-redis.sh <path-to-dump.rdb>"
  exit 1
fi

FILE=$1
echo "Restoring Redis from $FILE..."

echo "Stopping Redis container..."
docker stop msrtc-redis

echo "Replacing dump.rdb..."
docker cp $FILE msrtc-redis:/data/dump.rdb

echo "Starting Redis container..."
docker start msrtc-redis

echo "Restore complete!"
