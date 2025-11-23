locals {
  instance_ids = [
    for i in range(var.instance_count) :
    "i-${md5("${var.environment}-${i}-${var.instance_type}")}"
  ]
}

resource "null_resource" "compute_instances" {
  count = var.instance_count
  
  triggers = {
    subnet_id     = element(var.subnet_ids, count.index % length(var.subnet_ids))
    instance_type = var.instance_type
    environment   = var.environment
  }
}