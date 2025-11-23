variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "subnet_count" {
  description = "Number of subnets to create"
  type        = number
  default     = 2
  
  validation {
    condition     = var.subnet_count > 0 && var.subnet_count <= 10
    error_message = "Subnet count must be between 1 and 10."
  }
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}