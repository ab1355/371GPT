# Podman Commands Reference for 371GPT

This document provides a reference of essential Podman commands for working with the 371GPT system.

## Basic Podman Commands

### Check Podman Installation
```bash
podman --version
podman run quay.io/podman/hello
```

### Container Management
```bash
# List all containers
podman ps -a

# List running containers
podman ps

# Stop a container
podman stop <container-name>

# Start a container
podman start <container-name>

# Remove a container
podman rm <container-name>

# Force remove a running container
podman rm -f <container-name>

# View container logs
podman logs <container-name>

# Follow container logs
podman logs -f <container-name>
```

### Image Management
```bash
# List all images
podman images

# Pull an image
podman pull <image-name>

# Build an image from a Dockerfile
podman build -t <tag-name> <path-to-dockerfile-directory>

# Remove an image
podman rmi <image-name>
```

## Pod Management Commands

```bash
# Create a pod
podman pod create --name <pod-name> -p <host-port>:<container-port>

# List all pods
podman pod ps

# Start a pod
podman pod start <pod-name>

# Stop a pod
podman pod stop <pod-name>

# Remove a pod
podman pod rm <pod-name>

# Force remove a pod and all its containers
podman pod rm -f <pod-name>
```

## 371GPT-Specific Commands

### Create Testing Environment
```bash
# Create the pod
podman pod create --name 371gpt-pod -p 8000:8000 -p 8080:8080 -p 8081:8080 -p 5432:5432

# Run PostgreSQL
podman run -d --pod 371gpt-pod \
  --name postgres \
  -e POSTGRES_USER=dbadmin \
  -e POSTGRES_PASSWORD=dbpassword \
  -e POSTGRES_DB=371gpt_db \
  postgres:15-alpine
```

### Build and Run Services
```bash
# Build Orchestrator service
podman build -t 371gpt-orchestrator ./services/orchestrator

# Run Orchestrator service
podman run -d --pod 371gpt-pod \
  --name orchestrator \
  -e POSTGRES_HOST=localhost \
  -e POSTGRES_USER=dbadmin \
  -e POSTGRES_PASSWORD=dbpassword \
  -e POSTGRES_DB=371gpt_db \
  -e JWT_SECRET=test-secret \
  371gpt-orchestrator

# Build UI service
podman build -t 371gpt-ui ./services/ui

# Run UI service
podman run -d --pod 371gpt-pod \
  --name ui \
  -e ORCHESTRATOR_URL=http://localhost:8080 \
  -e JWT_SECRET=test-secret \
  371gpt-ui
```

### Executing Commands Inside Containers
```bash
# Execute a command in a running container
podman exec -it <container-name> <command>

# Get a shell in a container
podman exec -it <container-name> /bin/bash
# or if bash isn't available
podman exec -it <container-name> /bin/sh

# Examples
podman exec -it postgres psql -U dbadmin -d 371gpt_db
podman exec -it ui python -c "import os; print(os.environ)"
```

### Monitoring Container Resources
```bash
# Show resource usage of all containers
podman stats

# Show resource usage of specific containers
podman stats <container-name-1> <container-name-2>
```

### Volume Management
```bash
# Create a volume
podman volume create <volume-name>

# List volumes
podman volume ls

# Inspect a volume
podman volume inspect <volume-name>

# Remove a volume
podman volume rm <volume-name>
```

## Troubleshooting Commands

```bash
# Check container health
podman healthcheck run <container-name>

# Inspect container details
podman inspect <container-name>

# View container events
podman events

# Check network settings
podman network ls
podman network inspect <network-name>
```

These commands should help you manage and troubleshoot the 371GPT system when running with Podman.