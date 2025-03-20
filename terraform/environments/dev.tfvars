environment = "dev"
vpc_cidr    = "10.0.0.0/16"
aws_region  = "us-west-2"

# Kubernetes node groups for development (smaller instances)
node_groups = {
  orchestrator = {
    instance_types = ["t3.small"]
    desired_size   = 1
    min_size       = 1
    max_size       = 2
  },
  agents = {
    instance_types = ["t3.medium"]
    desired_size   = 1
    min_size       = 1
    max_size       = 3
  },
  ui = {
    instance_types = ["t3.small"]
    desired_size   = 1
    min_size       = 1
    max_size       = 2
  }
}

# Tags specific to development environment
tags = {
  Project     = "371GPT"
  Environment = "dev"
  ManagedBy   = "Terraform"
}