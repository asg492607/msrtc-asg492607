# Disaster Recovery Runbook

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
