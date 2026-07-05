# FinOps Runbook

## Overview
The goal of FinOps is not just to cut costs, but to maximize the business value of every dollar spent on AWS/GCP infrastructure.

## Anomalies
If the `finops-service` triggers a `CostAnomaly` alert (e.g., Redis memory usage spiked, driving up Elasticache costs):
1. Review the `/finops/dashboard` API to identify the offending service.
2. Cross-reference with the Prometheus dashboard to find the exact memory leak.

## Capacity Planning
Production node pools are scaled via the Terraform configurations in `terraform/environments/production/main.tf`. Before modifying instance types (e.g., `t3.xlarge` -> `r6g.xlarge`), consult the AI-driven forecasting API.
