output "instance_ids" {
  description = "List of instance IDs"
  value       = local.instance_ids
}

output "instance_count" {
  description = "Number of instances created"
  value       = var.instance_count
}

output "compute_metadata" {
  description = "Compute metadata for contract validation"
  value = {
    instance_ids  = local.instance_ids
    instance_type = var.instance_type
    count         = var.instance_count
    environment   = var.environment
  }
}