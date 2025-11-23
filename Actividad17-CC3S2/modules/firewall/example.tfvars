vpc_id      = "vpc-test123"
environment = "production"

rules = [
  {
    port        = 80
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
  },
  {
    port        = 443
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
  },
  {
    port        = 22
    cidr_blocks = ["10.0.0.0/8"]
    protocol    = "tcp"
  }
]
