# Troubleshooting 371GPT

This guide helps you resolve common issues when running 371GPT with Podman.

## Dependency Issues

### UI Service Dependencies

If you encounter this error with the UI service:

```
ERROR: Cannot install -r requirements.txt (line 1) and python-multipart==0.0.7 because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested python-multipart==0.0.7
    nicegui 1.4.6 depends on python-multipart<0.0.7 and >=0.0.6
```

**Solution**: Use python-multipart==0.0.6 in your requirements.txt (fixed in latest version)

### Orchestrator Service Dependencies

If you encounter this error with the orchestrator service:

```
ERROR: Could not find a version that satisfies the requirement portkey-ai==1.2.6
ERROR: No matching distribution found for portkey-ai==1.2.6
```

**Solution**: Use portkey-ai==1.11.1 in your requirements.txt (fixed in latest version)

## Container Networking Issues

### Container Can't Connect to Another Container

If services can't connect to each other (like UI to Orchestrator):

**Solution**: 
1. Ensure all containers are in the same pod
2. Use `localhost` for internal pod communication
3. Check logs with `podman logs -f <container-name>`

## Port Conflicts

If you see errors about ports already being in use:

**Solution**: Change the port mappings in the pod creation command:

```bash
podman pod create --name 371gpt-pod -p 8001:8000 -p 8082:8080 -p 8083:8080 -p 5433:5432
```

Then access the UI at http://localhost:8001 instead.

## Database Issues

### Services Can't Connect to Database

If services can't connect to PostgreSQL:

**Solution**:
1. Ensure PostgreSQL container is running: `podman ps | grep postgres`
2. Check PostgreSQL logs: `podman logs -f postgres`
3. Wait longer for PostgreSQL to initialize before starting other services
4. Verify environment variables match (DB name, username, password)

## Testing Individual Components

If you're having trouble with the full system, you can test components individually:

### Test UI Service Only

```bash
# Create pod for UI only
podman pod create --name ui-test -p 8000:8000

# Run UI service
podman build -t 371gpt-ui ./services/ui
podman run -d --pod ui-test --name ui -e JWT_SECRET=test-secret 371gpt-ui
```

### Test Database Only

```bash
# Create pod for database only
podman pod create --name db-test -p 5432:5432

# Run PostgreSQL
podman run -d --pod db-test --name postgres -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:15-alpine

# Check database logs
podman logs -f postgres
```

## Cleanup

If you need to start fresh:

```bash
# Remove all pods and containers
podman pod rm -f 371gpt-pod
podman pod rm -f 371gpt-test
podman pod rm -f ui-test
podman pod rm -f db-test

# Remove all images
podman rmi 371gpt-ui
podman rmi 371gpt-orchestrator
```