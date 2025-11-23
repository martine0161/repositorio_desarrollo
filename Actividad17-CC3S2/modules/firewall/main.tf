locals {
  firewall_policy = {
    vpc_id      = var.vpc_id
    environment = var.environment
    rules = [
      for idx, rule in var.rules : {
        rule_id     = "rule-${md5("${var.vpc_id}-${idx}")}"
        port        = rule.port
        cidr_blocks = rule.cidr_blocks
        protocol    = rule.protocol
      }
    ]
  }
  
  policy_json = jsonencode(local.firewall_policy)
}

resource "null_resource" "firewall_rules" {
  count = length(var.rules)
  
  triggers = {
    rule = jsonencode(var.rules[count.index])
  }
}