# 371GPT

A scalable, ethical AI orchestration system for non-coders based on the DSF (Discover, Space, Flow) model. This system enables non-technical users to harness the power of AI agents through intuitive interfaces and automated deployment.

## Overview

371GPT is a comprehensive framework that implements a multi-agent AI system with an emphasis on:

- **Accessibility**: No-code interfaces for system configuration and management
- **Scalability**: Microservice architecture with dynamic agent creation
- **Ethics**: Built-in guardrails and monitoring for responsible AI use
- **Robustness**: Self-healing error handling and comprehensive logging

The system follows the DSF model:
- **Discover**: AI-driven research and adaptive learning
- **Space**: Collaborative low-code interface for configuration
- **Flow**: Seamless AI task execution and automation

## Architecture

The system consists of several key components:

- **CEO Orchestrator Agent**: Central coordinator that manages all specialized agents
- **Specialized Agents**: Domain-specific agents (Research, Development, Communication, etc.)
- **NiceGUI Interface**: Web-based dashboard for system configuration and monitoring
- **PluginBoard**: Tool management system for agent capabilities
- **Infrastructure Layer**: Terraform-managed cloud resources for scalable deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Terraform 1.4+
- AWS Account (for cloud deployment) or local Kubernetes setup
- Python 3.10+

### Quick Start

1. Clone this repository:
   ```
   git clone https://github.com/ab1355/371GPT.git
   cd 371GPT
   ```

2. Set up local development environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the local development stack:
   ```
   docker-compose up -d
   ```

4. Access the admin interface at http://localhost:8080

### Deployment

For cloud deployment:

1. Configure your AWS credentials
2. Initialize Terraform:
   ```
   cd terraform
   terraform init
   ```

3. Deploy to development environment:
   ```
   terraform apply -var-file=environments/dev.tfvars
   ```

## Documentation

- [User Guide](docs/user-guide.md): How to use the 371GPT system
- [Administrator Guide](docs/admin-guide.md): System configuration and management
- [Development Guide](docs/dev-guide.md): How to extend and customize 371GPT
- [Architecture Overview](docs/architecture.md): Detailed system design

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The DSF Model creators
- The open source community behind NiceGUI, Terraform, and other tools used in this project