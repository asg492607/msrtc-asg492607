# RDS PostgreSQL Module
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
