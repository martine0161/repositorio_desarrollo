variable "records" {
  description = "DNS records to create"
  type = map(object({
    hostname = string
    ip       = string
  }))
  
  validation {
    condition = alltrue([
      for key, record in var.records :
      can(regex("^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$", record.hostname))
    ])
    error_message = "Hostnames must be valid DNS names without spaces or special characters."
  }
  
  validation {
    condition = alltrue([
      for key, record in var.records :
      can(regex("^([0-9]{1,3}\\.){3}[0-9]{1,3}$", record.ip))
    ])
    error_message = "IP addresses must be valid IPv4 addresses."
  }
}

variable "zone_name" {
  description = "DNS zone name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}