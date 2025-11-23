locals {
  bucket_id  = "bucket-${md5(var.bucket_name)}"
  bucket_arn = "arn:aws:s3:::${var.bucket_name}"
}

resource "null_resource" "storage_bucket" {
  triggers = {
    bucket_name        = var.bucket_name
    versioning_enabled = var.versioning_enabled
    environment        = var.environment
  }
}