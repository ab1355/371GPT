# 371GPT Testing Guide

This guide provides quick instructions for testing 371GPT with minimal setup requirements.

## Quick Testing with Podman

For testing purposes, you can run 371GPT without setting up environment variables. The system will use default values suitable for testing.

### Option 1: Using the Provided Scripts

#### Windows (PowerShell)
```powershell
.\run-with-podman.ps1
```

#### Linux/macOS
```bash
chmod +x run-with-podman.sh
./run-with-podman.sh
```

### Option 2: Direct Podman Commands

If you prefer to run commands directly with Podman, here's a minimal test sequence:

```bash
# Create a pod for all services
podman pod create --name 371gpt-pod -p 8000:8000 -p 8080:8080 -p 8081:8080 -p 5432:5432

# Run PostgreSQL with default test values
podman run -d --pod 371gpt-pod \
  --name postgres \
  -e POSTGRES_USER=dbadmin \
  -e POSTGRES_PASSWORD=dbpassword \
  -e POSTGRES_DB=371gpt_db \
  postgres:15-alpine

# Start NocoDB for database management
podman run -d --pod 371gpt-pod \
  --name nocodb \
  -e "NC_DB=pg://dbadmin:dbpassword@localhost:5432/371gpt_db" \
  -e "NC_AUTH_JWT_SECRET=371gpt-jwt-secret" \
  nocodb/nocodb:latest

# Build and run the Orchestrator service
podman build -t 371gpt-orchestrator ./services/orchestrator
podman run -d --pod 371gpt-pod \
  --name orchestrator \
  -e POSTGRES_HOST=localhost \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_USER=dbadmin \
  -e POSTGRES_PASSWORD=dbpassword \
  -e POSTGRES_DB=371gpt_db \
  -e JWT_SECRET=371gpt-jwt-secret \
  -e LOG_LEVEL=INFO \
  371gpt-orchestrator

# Build and run the UI service
podman build -t 371gpt-ui ./services/ui
podman run -d --pod 371gpt-pod \
  --name ui \
  -e ORCHESTRATOR_URL=http://localhost:8080 \
  -e JWT_SECRET=371gpt-jwt-secret \
  371gpt-ui
```

### Accessing the System

Once running, you can access:
- The 371GPT UI at http://localhost:8000
- NocoDB for database management at http://localhost:8081

### Managing the Test Environment

```bash
# Check status of all containers
podman pod ps
podman ps -a --pod

# View logs for a specific service
podman logs -f ui
podman logs -f orchestrator

# Stop all services
podman pod stop 371gpt-pod

# Start all services again
podman pod start 371gpt-pod

# Remove everything when done testing
podman pod rm -f 371gpt-pod
```

## Troubleshooting Common Issues

### Port Conflicts
If you see errors about ports already being in use, change the port mappings in the pod creation command:

```bash
podman pod create --name 371gpt-pod -p 8001:8000 -p 8082:8080 -p 8083:8080 -p 5433:5432
```

Then access the UI at http://localhost:8001 instead.

### Container Build Failures
If container builds fail, check that you're in the root directory of the project when building:

```bash
cd /path/to/371GPT
podman build -t 371gpt-ui ./services/ui
```

### Database Connection Issues
If services can't connect to the database, ensure the database container is fully initialized before starting other services:

```bash
# Wait for PostgreSQL to be ready
podman logs -f postgres
# Start other services after seeing "database system is ready to accept connections"
```