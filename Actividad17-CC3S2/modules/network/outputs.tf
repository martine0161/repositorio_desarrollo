output "vpc_id" {
  description = "ID of the VPC"
  value       = local.vpc_id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = var.vpc_cidr
}

output "subnet_ids" {
  description = "List of subnet IDs"
  value       = local.subnet_ids
}

output "subnet_count" {
  description = "Number of subnets created"
  value       = var.subnet_count
}

output "network_metadata" {
  description = "Network metadata for contract validation"
  value = {
    vpc_id       = local.vpc_id
    cidr         = var.vpc_cidr
    subnet_count = var.subnet_count
    environment  = var.environment
  }
}