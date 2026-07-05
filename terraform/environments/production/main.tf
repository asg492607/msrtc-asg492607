terraform {
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
