# Simulación de VPC (sin proveedor real)
locals {
  vpc_id = "vpc-${md5(var.vpc_cidr)}"
  subnet_ids = [
    for i in range(var.subnet_count) : 
    "subnet-${md5("${var.vpc_cidr}-${i}")}"
  ]
}

# Generar información de red simulada
resource "null_resource" "network_info" {
  triggers = {
    vpc_cidr      = var.vpc_cidr
    subnet_count  = var.subnet_count
    environment   = var.environment
  }
}