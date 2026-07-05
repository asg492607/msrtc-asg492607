variable "environment" {}
variable "project_name" {}
variable "private_subnet_ids" { type = list(string) }
variable "cluster_iam_role_arn" {}
variable "node_iam_role_arn" {}
variable "node_instance_type" {}
variable "node_desired_size" {}
variable "node_max_size" {}
variable "node_min_size" {}
