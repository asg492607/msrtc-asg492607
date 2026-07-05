variable "vpc_cidr" {}
variable "environment" {}
variable "project_name" {}
variable "private_subnet_cidrs" { type = list(string) }
variable "availability_zones" { type = list(string) }
