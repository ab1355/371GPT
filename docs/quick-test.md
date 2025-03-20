# Quick Test Guide for 371GPT

This is a simplified guide for quickly testing 371GPT with Podman without setting up environment variables.

## Single-Command Testing

For the fastest testing experience, you can use these commands:

### Windows (PowerShell)

```powershell
# Create pod and run PostgreSQL
podman pod create --name 371gpt-test -p 8000:8000
podman run -d --pod 371gpt-test --name db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:15-alpine

# Wait a moment for PostgreSQL to initialize
Start-Sleep -Seconds 10

# Run UI service with minimal settings
podman build -t 371gpt-ui-test ./services/ui
podman run -d --pod 371gpt-test --name ui-test -e JWT_SECRET=test-secret 371gpt-ui-test
```

### Linux/macOS

```bash
# Create pod and run PostgreSQL
podman pod create --name 371gpt-test -p 8000:8000
podman run -d --pod 371gpt-test --name db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:15-alpine

# Wait a moment for PostgreSQL to initialize
sleep 10

# Run UI service with minimal settings
podman build -t 371gpt-ui-test ./services/ui
podman run -d --pod 371gpt-test --name ui-test -e JWT_SECRET=test-secret 371gpt-ui-test
```

## Accessing the Test Environment

- Access 371GPT UI at: http://localhost:8000

## Clean Up

When you're done testing:

```bash
podman pod rm -f 371gpt-test
```

For more detailed testing instructions, see the [full testing guide](testing-guide.md).