output "bucket_id" {
  description = "ID of the storage bucket"
  value       = local.bucket_id
}

output "bucket_name" {
  description = "Name of the storage bucket"
  value       = var.bucket_name
}

output "bucket_arn" {
  description = "ARN of the storage bucket"
  value       = local.bucket_arn
}

output "storage_metadata" {
  description = "Storage metadata for contract validation"
  value = {
    bucket_id          = local.bucket_id
    bucket_name        = var.bucket_name
    bucket_arn         = local.bucket_arn
    versioning_enabled = var.versioning_enabled
    environment        = var.environment
  }
}