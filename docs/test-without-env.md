# Testing 371GPT Without Environment Variables

This guide shows how to quickly test 371GPT components with Podman without setting up any environment variables.

## Simplest UI-Only Test

If you just want to test the UI functionality:

```powershell
# Create minimal test pod
podman pod create --name ui-only -p 8000:8000

# Build and run UI only
podman build -t 371gpt-ui ./services/ui
podman run -d --pod ui-only --name ui -e JWT_SECRET=test-secret 371gpt-ui
```

Access the UI at http://localhost:8000

## Testing UI and Orchestrator

For a more complete test with both UI and orchestrator services:

```powershell
# Create test pod with all required ports
podman pod create --name 371gpt-mini -p 8000:8000 -p 8080:8080

# Run PostgreSQL with minimal settings
podman run -d --pod 371gpt-mini --name postgres -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:15-alpine

# Wait for PostgreSQL to initialize
Start-Sleep -Seconds 15

# Build and run the orchestrator
podman build -t 371gpt-orchestrator ./services/orchestrator
podman run -d --pod 371gpt-mini --name orchestrator \
  -e POSTGRES_HOST=localhost \
  -e POSTGRES_USER=test \
  -e POSTGRES_PASSWORD=test \
  -e POSTGRES_DB=testdb \
  -e JWT_SECRET=test-secret \
  371gpt-orchestrator

# Build and run the UI
podman build -t 371gpt-ui ./services/ui
podman run -d --pod 371gpt-mini --name ui \
  -e ORCHESTRATOR_URL=http://localhost:8080 \
  -e JWT_SECRET=test-secret \
  371gpt-ui
```

## Checking if Services are Running

```powershell
# List all pods and their status
podman pod ps

# List all containers
podman ps -a

# Check UI logs
podman logs -f ui

# Check orchestrator logs  
podman logs -f orchestrator
```

## Cleaning Up

When you're done testing:

```powershell
# Remove everything
podman pod rm -f ui-only
podman pod rm -f 371gpt-mini
```

## Troubleshooting

If you encounter issues:

1. Make sure you're in the correct directory (where the project is cloned)
2. Check that the Dockerfiles exist in services/ui and services/orchestrator
3. Verify that all containers in the pod are running: `podman ps -a --pod`
4. Look at the logs for each failing service: `podman logs -f <container-name>`

For detailed troubleshooting, see [Troubleshooting Guide](troubleshooting.md)