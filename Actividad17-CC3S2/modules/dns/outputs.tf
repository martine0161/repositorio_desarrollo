output "hostname_ip_map" {
  description = "Map of hostname to IP address"
  value       = local.hostname_ip_map
}

output "zone_id" {
  description = "DNS zone ID"
  value       = local.zone_id
}

output "record_count" {
  description = "Number of DNS records"
  value       = length(var.records)
}

output "dns_metadata" {
  description = "DNS metadata for contract validation"
  value = {
    zone_id     = local.zone_id
    zone_name   = var.zone_name
    records     = local.hostname_ip_map
    record_count = length(var.records)
    environment = var.environment
  }
}