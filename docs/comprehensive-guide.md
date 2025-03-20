# Comprehensive Guide to 371GPT

This guide provides detailed instructions for setting up, configuring, and running the 371GPT system for both developers and non-technical users.

## Table of Contents

- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Configuration Options](#configuration-options)
- [Running Individual Components](#running-individual-components)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

## Quick Start

For the fastest way to test 371GPT:

### Using Podman (Windows)

```powershell
# Create pod with PostgreSQL
podman pod create --name 371gpt-quick -p 8000:8000
podman run -d --pod 371gpt-quick --name db -e POSTGRES_USER=demo -e POSTGRES_PASSWORD=demo123 -e POSTGRES_DB=demo postgres:15-alpine

# Run UI service
podman build -t 371gpt-ui ./services/ui
podman run -d --pod 371gpt-quick --name ui -e JWT_SECRET=demo-secret 371gpt-ui
```

Access the UI at http://localhost:8000

## Detailed Installation

### Prerequisites

- Podman or Docker
- Git
- Python 3.10+ (for development)
- PostgreSQL client (optional, for database management)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ab1355/371GPT.git
cd 371GPT
```

### Step 2: Configure Environment Variables

Create a `.env` file based on the example:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferred settings:

```
# Database settings
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=371gpt_db

# Security settings
JWT_SECRET=your_secret_key

# API keys (if needed)
PORTKEY_API_KEY=your_api_key

# Other settings
LOG_LEVEL=INFO
```

### Step 3: Run the System

#### Using Podman

```powershell
# For Windows
.\run-with-podman.ps1

# For Linux/macOS
chmod +x run-with-podman.sh
./run-with-podman.sh
```

#### Using Docker Compose

```bash
docker-compose up -d
```

### Step 4: Access the System

- UI Dashboard: http://localhost:8000
- Database UI (NocoDB): http://localhost:8081
- API (Orchestrator): http://localhost:8080

## Configuration Options

### UI Configuration

The UI is configured through `config/ui/ui-config.json`. This file controls:

- Theme colors and appearance
- Dashboard layout and components
- Feature visibility
- Refresh intervals

Example UI configuration:

```json
{
  "theme": {
    "primary": "#1976D2",
    "secondary": "#26A69A",
    "dark_mode": true
  },
  "dashboard": {
    "refresh_interval": 30,
    "show_system_stats": true
  }
}
```

### Agent Configuration

Agents are configured in `config/agents/agent-config.json`. This file defines:

- Available agent types
- Agent capabilities
- Memory settings
- API configurations

Example agent configuration:

```json
{
  "agents": [
    {
      "name": "research_agent",
      "description": "Performs online research",
      "capabilities": ["web_search", "summarization"],
      "memory_size": 10
    }
  ]
}
```

## Running Individual Components

For development or testing specific components:

### Database Only

```bash
podman run -d --name postgres -p 5432:5432 -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:15-alpine
```

### Orchestrator Only

```bash
# In services/orchestrator directory
podman build -t 371gpt-orchestrator .
podman run -d --name orchestrator -p 8080:8080 -e POSTGRES_HOST=host.containers.internal -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb -e JWT_SECRET=test-secret 371gpt-orchestrator
```

### UI Only

```bash
# In services/ui directory
podman build -t 371gpt-ui .
podman run -d --name ui -p 8000:8000 -e ORCHESTRATOR_URL=http://host.containers.internal:8080 -e JWT_SECRET=test-secret 371gpt-ui
```

## Production Deployment

For production deployment, follow these additional steps:

1. Use stronger passwords and secrets
2. Enable HTTPS/TLS
3. Configure proper backups for the database
4. Set up monitoring with Prometheus/Grafana

### AWS Deployment with Terraform

From the terraform directory:

```bash
terraform init
terraform apply -var-file=environments/prod.tfvars
```

## Troubleshooting

See the [Troubleshooting Guide](troubleshooting.md) for solutions to common issues.

### Common Issues

- **Dependency conflicts**: Make sure you're using the versions specified in requirements.txt
- **Port conflicts**: Change the port mappings if ports are already in use
- **Network issues**: Ensure containers can communicate with each other
- **Database connection failures**: Check database credentials and wait for PostgreSQL to initialize

## Advanced Configuration

### Custom Agent Development

To create custom agents:

1. Create a new directory in `services/agents/`
2. Implement the agent interface (see example in Research Agent)
3. Add the agent to the configuration file
4. Register the agent with the orchestrator

### Extending the UI

To add custom UI components:

1. Modify `services/ui/app.py` to add new routes or components
2. Update UI configuration in `config/ui/ui-config.json`
3. Rebuild the UI container

### Security Hardening

For enhanced security:

1. Use a proper secrets management system
2. Implement role-based access control
3. Regular security audits
4. Enable API rate limiting