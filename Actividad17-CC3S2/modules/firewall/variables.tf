variable "rules" {
  description = "List of firewall rules"
  type = list(object({
    port        = number
    cidr_blocks = list(string)
    protocol    = string
  }))
  
  validation {
    condition = alltrue([
      for rule in var.rules :
      rule.port >= 1 && rule.port <= 65535
    ])
    error_message = "Port numbers must be between 1 and 65535."
  }
  
  validation {
    condition = alltrue([
      for rule in var.rules :
      contains(["tcp", "udp", "icmp"], rule.protocol)
    ])
    error_message = "Protocol must be tcp, udp, or icmp."
  }
}

variable "vpc_id" {
  description = "VPC ID where firewall rules apply"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}