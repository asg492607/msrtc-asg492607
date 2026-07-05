import os

base_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc\terraform"

# Directory structure
dirs = [
    "modules/network",
    "modules/kubernetes",
    "modules/database",
    "modules/redis",
    "modules/kafka",
    "environments/production",
    "environments/staging",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Network Module
network_main = """# VPC and Subnets Module
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name        = "${var.project_name}-${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = element(var.availability_zones, count.index)
  tags = {
    Name = "${var.project_name}-${var.environment}-private-${count.index + 1}"
  }
}
"""
with open(os.path.join(base_dir, "modules/network/main.tf"), "w", encoding="utf-8") as f: f.write(network_main)
with open(os.path.join(base_dir, "modules/network/variables.tf"), "w", encoding="utf-8") as f:
    f.write('variable "vpc_cidr" {}\nvariable "environment" {}\nvariable "project_name" {}\nvariable "private_subnet_cidrs" { type = list(string) }\nvariable "availability_zones" { type = list(string) }\n')

# 2. Kubernetes Module
k8s_main = """# EKS Cluster Module
resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-${var.environment}-cluster"
  role_arn = var.cluster_iam_role_arn

  vpc_config {
    subnet_ids = var.private_subnet_ids
  }
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-${var.environment}-nodes"
  node_role_arn   = var.node_iam_role_arn
  subnet_ids      = var.private_subnet_ids

  scaling_config {
    desired_size = var.node_desired_size
    max_size     = var.node_max_size
    min_size     = var.node_min_size
  }
  instance_types = [var.node_instance_type]
}
"""
with open(os.path.join(base_dir, "modules/kubernetes/main.tf"), "w", encoding="utf-8") as f: f.write(k8s_main)
with open(os.path.join(base_dir, "modules/kubernetes/variables.tf"), "w", encoding="utf-8") as f:
    f.write('variable "environment" {}\nvariable "project_name" {}\nvariable "private_subnet_ids" { type = list(string) }\nvariable "cluster_iam_role_arn" {}\nvariable "node_iam_role_arn" {}\nvariable "node_instance_type" {}\nvariable "node_desired_size" {}\nvariable "node_max_size" {}\nvariable "node_min_size" {}\n')

# 3. Database Module
db_main = """# RDS PostgreSQL Module
resource "aws_db_instance" "postgres" {
  identifier           = "${var.project_name}-${var.environment}-postgres"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = var.db_instance_class
  allocated_storage    = var.db_allocated_storage
  storage_type         = "gp3"
  db_name              = "msrtc"
  username             = var.db_username
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.db_security_group_id]
  multi_az             = var.multi_az
  backup_retention_period = 7
  storage_encrypted    = true
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet"
  subnet_ids = var.private_subnet_ids
}
"""
with open(os.path.join(base_dir, "modules/database/main.tf"), "w", encoding="utf-8") as f: f.write(db_main)
with open(os.path.join(base_dir, "modules/database/variables.tf"), "w", encoding="utf-8") as f:
    f.write('variable "environment" {}\nvariable "project_name" {}\nvariable "db_instance_class" {}\nvariable "db_allocated_storage" {}\nvariable "db_username" {}\nvariable "db_password" {}\nvariable "private_subnet_ids" { type = list(string) }\nvariable "db_security_group_id" {}\nvariable "multi_az" { type = bool }\n')

# 4. Production Environment
prod_main = """terraform {
  backend "s3" {
    bucket         = "msrtc-terraform-state-prod"
    key            = "platform/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "msrtc-terraform-locks"
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "network" {
  source = "../../modules/network"
  project_name = "msrtc"
  environment  = "prod"
  vpc_cidr     = "10.0.0.0/16"
  private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  availability_zones   = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
}

module "kubernetes" {
  source = "../../modules/kubernetes"
  project_name = "msrtc"
  environment  = "prod"
  private_subnet_ids = module.network.private_subnet_ids
  cluster_iam_role_arn = "arn:aws:iam::123456789012:role/eksClusterRole"
  node_iam_role_arn    = "arn:aws:iam::123456789012:role/eksNodeRole"
  node_instance_type = "t3.xlarge"
  node_desired_size = 5
  node_max_size = 20
  node_min_size = 3
}

module "database" {
  source = "../../modules/database"
  project_name = "msrtc"
  environment  = "prod"
  db_instance_class = "db.r6g.xlarge"
  db_allocated_storage = 500
  db_username = "admin"
  db_password = var.db_password # Injected via TF_VAR_db_password or Secrets Manager
  private_subnet_ids = module.network.private_subnet_ids
  db_security_group_id = "sg-12345"
  multi_az = true
}
"""
with open(os.path.join(base_dir, "environments/production/main.tf"), "w", encoding="utf-8") as f: f.write(prod_main)
with open(os.path.join(base_dir, "environments/production/variables.tf"), "w", encoding="utf-8") as f:
    f.write('variable "db_password" { type = string, sensitive = true }\n')

# 5. Terraform Runbook
runbook = """# Terraform Infrastructure Provisioning Runbook

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
"""
with open(os.path.join(base_dir, "docs/TERRAFORM_RUNBOOK.md"), "w", encoding="utf-8") as f: f.write(runbook)

print("Terraform Platform scaffolded successfully.")
