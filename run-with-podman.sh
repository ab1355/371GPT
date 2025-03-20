#!/bin/bash
# Script to run 371GPT using Podman instead of Docker

set -e

echo "Starting 371GPT with Podman..."

# Check if podman-compose is installed
if ! command -v podman-compose &> /dev/null; then
    echo "podman-compose is not installed. Installing..."
    pip install podman-compose
fi

# Create Podman pod for the application
echo "Creating 371GPT pod..."
podman pod create --name 371gpt-pod -p 8000:8000 -p 8080:8080 -p 8081:8080 -p 5432:5432

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    source .env
else
    echo "No .env file found, using default values..."
    # Set default environment variables
    export DB_USER=dbadmin
    export DB_PASSWORD=dbpassword
    export DB_NAME=371gpt_db
    export JWT_SECRET=371gpt-jwt-secret
fi

# Create volumes for persistent storage
echo "Creating Podman volumes..."
podman volume create postgres_data
podman volume create prometheus_data
podman volume create grafana_data

# Start PostgreSQL database
echo "Starting PostgreSQL database..."
podman run -d --pod 371gpt-pod \
    --name postgres \
    -e POSTGRES_USER=${DB_USER:-dbadmin} \
    -e POSTGRES_PASSWORD=${DB_PASSWORD:-dbpassword} \
    -e POSTGRES_DB=${DB_NAME:-371gpt_db} \
    -v postgres_data:/var/lib/postgresql/data \
    postgres:15-alpine

echo "Waiting for PostgreSQL to start..."
sleep 10

# Start NocoDB
echo "Starting NocoDB UI for database management..."
podman run -d --pod 371gpt-pod \
    --name nocodb \
    -e NC_DB="pg://${DB_USER:-dbadmin}:${DB_PASSWORD:-dbpassword}@localhost:5432/${DB_NAME:-371gpt_db}" \
    -e NC_AUTH_JWT_SECRET=${JWT_SECRET:-371gpt-jwt-secret} \
    nocodb/nocodb:latest

# Build and start the Orchestrator service
echo "Building and starting Orchestrator service..."
podman build -t 371gpt-orchestrator ./services/orchestrator
podman run -d --pod 371gpt-pod \
    --name orchestrator \
    -e PORTKEY_API_KEY=${PORTKEY_API_KEY:-your-portkey-api-key} \
    -e POSTGRES_HOST=localhost \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_USER=${DB_USER:-dbadmin} \
    -e POSTGRES_PASSWORD=${DB_PASSWORD:-dbpassword} \
    -e POSTGRES_DB=${DB_NAME:-371gpt_db} \
    -e JWT_SECRET=${JWT_SECRET:-371gpt-jwt-secret} \
    -e AGENT_CONFIG_PATH=/app/config/agents/agent-config.json \
    -e LOG_LEVEL=INFO \
    -v ./config:/app/config:Z \
    371gpt-orchestrator

# Build and start the UI service
echo "Building and starting UI service..."
podman build -t 371gpt-ui ./services/ui
podman run -d --pod 371gpt-pod \
    --name ui \
    -e ORCHESTRATOR_URL=http://localhost:8080 \
    -e JWT_SECRET=${JWT_SECRET:-371gpt-jwt-secret} \
    -v ./config:/app/config:Z \
    371gpt-ui

echo "371GPT is now running!"
echo "Access the UI at: http://localhost:8000"
echo "Access NocoDB at: http://localhost:8081"
echo ""
echo "Use the following commands to manage the system:"
echo "  - Stop all services: podman pod stop 371gpt-pod"
echo "  - Start all services: podman pod start 371gpt-pod"
echo "  - Remove all services: podman pod rm -f 371gpt-pod"
echo "  - View logs: podman logs -f <container-name> (e.g., podman logs -f ui)"