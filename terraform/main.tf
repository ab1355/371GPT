terraform {
  required_version = ">= 1.0.0"
  
  backend "s3" {
    # Configured via CLI params or environment variables
    # The following values are provided at runtime:
    # bucket, key, region, etc.
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.10"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.5"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = var.tags
  }
}

module "networking" {
  source = "./modules/networking"
  
  vpc_cidr      = var.vpc_cidr
  project_name  = var.project_name
  environment   = var.environment
}

module "database" {
  source = "./modules/database"
  
  vpc_id        = module.networking.vpc_id
  subnet_ids    = module.networking.private_subnet_ids
  db_name       = var.db_name
  db_user       = var.db_user
  db_password   = var.db_password
  project_name  = var.project_name
  environment   = var.environment
}

module "kubernetes" {
  source = "./modules/kubernetes"
  
  vpc_id        = module.networking.vpc_id
  subnet_ids    = module.networking.private_subnet_ids
  cluster_name  = "${var.project_name}-${var.environment}"
  node_groups   = var.node_groups
  project_name  = var.project_name
  environment   = var.environment
}

# Configure Kubernetes providers after the cluster is created
provider "kubernetes" {
  host                   = module.kubernetes.cluster_endpoint
  cluster_ca_certificate = base64decode(module.kubernetes.cluster_ca_certificate)
  token                  = module.kubernetes.cluster_token
}

provider "helm" {
  kubernetes {
    host                   = module.kubernetes.cluster_endpoint
    cluster_ca_certificate = base64decode(module.kubernetes.cluster_ca_certificate)
    token                  = module.kubernetes.cluster_token
  }
}

# Agent configuration storage bucket
resource "aws_s3_bucket" "agent_config" {
  bucket = "${var.project_name}-agent-config-${var.environment}"
  
  tags = {
    Name        = "Agent Configuration Storage"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "agent_config_versioning" {
  bucket = aws_s3_bucket.agent_config.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Outputs for use in other processes
output "kubernetes_cluster_endpoint" {
  value     = module.kubernetes.cluster_endpoint
  sensitive = true
}

output "kubernetes_cluster_name" {
  value = module.kubernetes.cluster_name
}

output "database_endpoint" {
  value     = module.database.endpoint
  sensitive = true
}

output "database_name" {
  value = var.db_name
}

output "config_bucket" {
  value = aws_s3_bucket.agent_config.bucket
}