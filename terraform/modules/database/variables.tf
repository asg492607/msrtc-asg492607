variable "environment" {}
variable "project_name" {}
variable "db_instance_class" {}
variable "db_allocated_storage" {}
variable "db_username" {}
variable "db_password" {}
variable "private_subnet_ids" { type = list(string) }
variable "db_security_group_id" {}
variable "multi_az" { type = bool }
