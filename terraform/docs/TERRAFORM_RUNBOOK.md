# Terraform Infrastructure Provisioning Runbook

## Overview
The MSRTC cloud infrastructure is fully managed by Terraform. This ensures our Staging and Production environments are identical in architecture, differing only in capacity (instance types).

## State Management
* **Backend:** Remote S3 bucket (`msrtc-terraform-state-prod`).
* **Locking:** DynamoDB table (`msrtc-terraform-locks`). This prevents two engineers (or CI/CD pipelines) from running `terraform apply` concurrently and corrupting the state.

## Deployment Workflow
To deploy changes to an environment (e.g., Staging):

1. **Initialize:** Download providers and configure the S3 backend.
   ```bash
   cd terraform/environments/staging
   terraform init
   ```
2. **Format & Validate:** Ensure code quality.
   ```bash
   terraform fmt -check
   terraform validate
   ```
3. **Plan:** See exactly what AWS resources will be created/modified/destroyed.
   ```bash
   terraform plan -out=tfplan
   ```
4. **Apply:** Execute the plan (in CI/CD, this step requires manual approval for Production).
   ```bash
   terraform apply tfplan
   ```
