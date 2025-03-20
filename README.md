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

## Quick Start for Testing

For the fastest way to test individual components:

```powershell
# Test just the UI component
.\simple-test.ps1 -Component ui -Port 8000

# Test just the database
.\simple-test.ps1 -Component db -Port 5432

# Clean up after testing
.\simple-test.ps1 -CleanUp
```

This allows you to test components in isolation before trying the full system.

## Getting Started

### Prerequisites

- Docker and Docker Compose OR Podman
- Terraform 1.4+ (for cloud deployment)
- OVH Cloud Account (for hosting) or local Kubernetes setup
- Python 3.10+

### Running with Docker

1. Clone this repository:
   ```
   git clone https://github.com/ab1355/371GPT.git
   cd 371GPT
   ```

2. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Run the local development stack:
   ```
   docker-compose up -d
   ```

4. Access the admin interface at http://localhost:8000

### Running with Podman

#### Linux/macOS

1. Clone this repository:
   ```
   git clone https://github.com/ab1355/371GPT.git
   cd 371GPT
   ```

2. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Run the system using the provided script:
   ```
   chmod +x run-with-podman.sh
   ./run-with-podman.sh
   ```

4. Access the admin interface at http://localhost:8000

#### Windows

1. Clone this repository:
   ```
   git clone https://github.com/ab1355/371GPT.git
   cd 371GPT
   ```

2. Set up environment variables:
   ```
   copy .env.example .env
   # Edit .env with your settings
   ```

3. Run the system using the provided PowerShell script:
   ```
   .\run-with-podman.ps1
   ```

4. Access the admin interface at http://localhost:8000

### Podman Management Commands

- Stop all services: `podman pod stop 371gpt-pod`
- Start all services: `podman pod start 371gpt-pod`
- Remove all services: `podman pod rm -f 371gpt-pod`
- View logs: `podman logs -f <container-name>` (e.g., `podman logs -f ui`)

See [Podman Commands Reference](docs/podman-commands.md) for more details.

## Documentation

### Core System
- [Comprehensive Guide](docs/comprehensive-guide.md): Detailed setup, configuration, and usage instructions
- [Architecture Overview](docs/architecture.md): Detailed system design
- [Testing Guide](docs/testing-guide.md): Comprehensive testing instructions
- [Quick Test Guide](docs/quick-test.md): Simplified testing procedures
- [Podman Commands](docs/podman-commands.md): Reference for Podman commands
- [Troubleshooting](docs/troubleshooting.md): Solutions to common issues

### 371 Minds Business Implementation
- [371 Minds Implementation Plan](docs/371-minds-implementation.md): Complete plan for implementing XaaS offerings
- [Pimcore & Odoo Integration](docs/pimcore-odoo-integration.md): Guide to integrating these complementary systems
- [RapidAPI & XPipe Integration](docs/rapidapi-xpipe-integration.md): Implementation of API monetization and data flows

### User Guides
- [Solopreneur Guide](docs/solopreneur-guide.md): Tailored guidance for solopreneurs
- [User Guide](docs/user-guide.md): How to use the 371GPT system
- [Administrator Guide](docs/admin-guide.md): System configuration and management
- [Development Guide](docs/dev-guide.md): How to extend and customize 371GPT

## For Businesses

If you're looking to use 371GPT as the foundation for an "Everything as a Service" (XaaS) business model, our [371 Minds Implementation Plan](docs/371-minds-implementation.md) covers:

- Comprehensive technology stack including Odoo, Pimcore, RapidAPI, and XPipe
- Industry-specific implementations and customizations
- Multiple revenue stream development
- Phased implementation approach with clear timelines

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The DSF Model creators
- The open source community behind NiceGUI, Terraform, and other tools used in this project