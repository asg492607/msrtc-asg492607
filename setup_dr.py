import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\platform-recovery"

os.makedirs(os.path.join(base_dir, "backup"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "restore"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "runbooks"), exist_ok=True)

# 1. Backup Scripts
backup_pg = """#!/bin/bash
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
"""
with open(os.path.join(base_dir, "backup/backup-postgres.sh"), "w", newline='\n') as f: f.write(backup_pg)

backup_redis = """#!/bin/bash
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
"""
with open(os.path.join(base_dir, "backup/backup-redis.sh"), "w", newline='\n') as f: f.write(backup_redis)

backup_minio = """#!/bin/bash
# Backup MinIO Object Storage (requires MinIO Client 'mc')
set -e

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./archives/minio_$TIMESTAMP"
mkdir -p $BACKUP_DIR

echo "Starting MinIO mirror..."
# Assuming 'myminio' is configured locally
mc mirror myminio/msrtc-bucket $BACKUP_DIR

echo "Backup successful: $BACKUP_DIR"
"""
with open(os.path.join(base_dir, "backup/backup-minio.sh"), "w", newline='\n') as f: f.write(backup_minio)


# 2. Restore Scripts
restore_pg = """#!/bin/bash
# Restore PostgreSQL Database
set -e

if [ -z "$1" ]; then
  echo "Usage: ./restore-postgres.sh <path-to-sql.gz>"
  exit 1
fi

FILE=$1
echo "Restoring PostgreSQL from $FILE..."

# Drop and recreate DB (DANGER in production, this is a local DR script)
docker exec -t msrtc-postgres psql -U postgres -c "DROP DATABASE IF EXISTS msrtc;"
docker exec -t msrtc-postgres psql -U postgres -c "CREATE DATABASE msrtc;"

# Restore
gunzip -c $FILE | docker exec -i msrtc-postgres psql -U postgres -d msrtc

echo "Restore complete!"
"""
with open(os.path.join(base_dir, "restore/restore-postgres.sh"), "w", newline='\n') as f: f.write(restore_pg)

restore_redis = """#!/bin/bash
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
"""
with open(os.path.join(base_dir, "restore/restore-redis.sh"), "w", newline='\n') as f: f.write(restore_redis)


# 3. Runbooks
ha_runbook = """# High Availability (HA) Architecture

## Overview
To prevent a single point of failure (SPOF) within the MSRTC platform, the following topology must be utilized in the production environment.

## Topology
1. **Load Balancer:** AWS ALB / NGINX Ingress Controller.
2. **API Gateways:** Minimum of 3 replicas distributed across Availability Zones.
3. **Microservices:** All 20 NestJS microservices must run a minimum of 2 Pods in a Kubernetes Cluster, auto-scaled based on CPU/Memory utilization.
4. **PostgreSQL:** Primary/Replica cluster (e.g. AWS RDS Multi-AZ). Read-heavy workloads should hit the Replica.
5. **Redis:** Redis Cluster or Sentinel setup spanning multiple AZs.
6. **Kafka:** Minimum 3-broker cluster with a replication factor of 3 and `min.insync.replicas=2`.

## Network Isolation
* Database and Cache layers must reside in Private Subnets.
* Only the API Gateway is exposed to the Public Internet.
"""
with open(os.path.join(base_dir, "runbooks/HA_ARCHITECTURE.md"), "w", encoding="utf-8") as f: f.write(ha_runbook)

dr_runbook = """# Disaster Recovery Runbook

## Objective
To safely recover the MSRTC platform in the event of partial or complete regional infrastructure failure.

## Targets
* **RTO (Recovery Time Objective):** 1 Hour
* **RPO (Recovery Point Objective):** 5 Minutes (assuming continuous WAL archiving)

## Scenario 1: Complete Database Corruption
1. Inform stakeholders of unexpected downtime.
2. Ensure no microservices are writing to the database (Stop the API Gateway).
3. Locate the latest nightly `sql.gz` backup.
4. If WAL archiving is enabled, replay WAL logs up to the exact minute of failure.
5. If WAL archiving is absent, use `./restore/restore-postgres.sh` with the nightly backup (Data loss: up to 24 hours).
6. Verify data integrity.
7. Restart API Gateways.

## Scenario 2: Redis Cluster Failure
* Because Redis is configured with `AOF` and `RDB` snapshots, data loss is minimal.
* If a total node wipe occurs, use `./restore/restore-redis.sh` with the latest RDB file.
* **Impact:** Active locks (Seat holds) might be lost. Booking validation will degrade to database checks until the cache warms up.
"""
with open(os.path.join(base_dir, "runbooks/DISASTER_RECOVERY_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(dr_runbook)

print("Disaster Recovery Platform scaffolded successfully.")
