locals {
  hostname_ip_map = {
    for key, record in var.records :
    record.hostname => record.ip
  }
  
  zone_id = "zone-${md5(var.zone_name)}"
}

resource "null_resource" "dns_records" {
  for_each = var.records
  
  triggers = {
    hostname = each.value.hostname
    ip       = each.value.ip
    zone     = var.zone_name
  }
}