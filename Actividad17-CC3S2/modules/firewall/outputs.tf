output "policy_json" {
  description = "Complete firewall policy in JSON format"
  value       = local.policy_json
}

output "rule_count" {
  description = "Number of firewall rules"
  value       = length(var.rules)
}

output "firewall_metadata" {
  description = "Firewall metadata for contract validation"
  value = {
    vpc_id      = var.vpc_id
    rule_count  = length(var.rules)
    environment = var.environment
    policy      = local.firewall_policy
  }
}