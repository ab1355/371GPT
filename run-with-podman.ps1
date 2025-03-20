# PowerShell script to run 371GPT using Podman on Windows

Write-Host "Starting 371GPT with Podman on Windows..." -ForegroundColor Green

# Load environment variables from .env file if it exists
if (Test-Path .env) {
    Write-Host "Loading environment variables from .env file..." -ForegroundColor Yellow
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            Write-Host "Set $name environment variable"
        }
    }
}
else {
    Write-Host "No .env file found, using default values..." -ForegroundColor Yellow
    # Set default environment variables
    $env:DB_USER = "dbadmin"
    $env:DB_PASSWORD = "dbpassword"
    $env:DB_NAME = "371gpt_db"
    $env:JWT_SECRET = "371gpt-jwt-secret"
}

# Create Podman pod for the application
Write-Host "Creating 371GPT pod..." -ForegroundColor Green
podman pod create --name 371gpt-pod -p 8000:8000 -p 8080:8080 -p 8081:8080 -p 5432:5432

# Create volumes for persistent storage
Write-Host "Creating Podman volumes..." -ForegroundColor Green
podman volume create postgres_data
podman volume create prometheus_data
podman volume create grafana_data

# Start PostgreSQL database
Write-Host "Starting PostgreSQL database..." -ForegroundColor Green
podman run -d --pod 371gpt-pod `
    --name postgres `
    -e POSTGRES_USER=$env:DB_USER `
    -e POSTGRES_PASSWORD=$env:DB_PASSWORD `
    -e POSTGRES_DB=$env:DB_NAME `
    -v postgres_data:/var/lib/postgresql/data `
    postgres:15-alpine

Write-Host "Waiting for PostgreSQL to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Start NocoDB
Write-Host "Starting NocoDB UI for database management..." -ForegroundColor Green
podman run -d --pod 371gpt-pod `
    --name nocodb `
    -e "NC_DB=pg://$env:DB_USER:$env:DB_PASSWORD@localhost:5432/$env:DB_NAME" `
    -e "NC_AUTH_JWT_SECRET=$env:JWT_SECRET" `
    nocodb/nocodb:latest

# Get the current directory
$currentDir = (Get-Location).Path

# Convert Windows paths to Podman-compatible paths
$configDir = "$currentDir\config".Replace("\", "/")

# Build and start the Orchestrator service
Write-Host "Building and starting Orchestrator service..." -ForegroundColor Green
podman build -t 371gpt-orchestrator ./services/orchestrator
podman run -d --pod 371gpt-pod `
    --name orchestrator `
    -e PORTKEY_API_KEY=$env:PORTKEY_API_KEY `
    -e POSTGRES_HOST=localhost `
    -e POSTGRES_PORT=5432 `
    -e POSTGRES_USER=$env:DB_USER `
    -e POSTGRES_PASSWORD=$env:DB_PASSWORD `
    -e POSTGRES_DB=$env:DB_NAME `
    -e JWT_SECRET=$env:JWT_SECRET `
    -e AGENT_CONFIG_PATH=/app/config/agents/agent-config.json `
    -e LOG_LEVEL=INFO `
    -v "${configDir}:/app/config:Z" `
    371gpt-orchestrator

# Build and start the UI service
Write-Host "Building and starting UI service..." -ForegroundColor Green
podman build -t 371gpt-ui ./services/ui
podman run -d --pod 371gpt-pod `
    --name ui `
    -e ORCHESTRATOR_URL=http://localhost:8080 `
    -e JWT_SECRET=$env:JWT_SECRET `
    -v "${configDir}:/app/config:Z" `
    371gpt-ui

Write-Host "371GPT is now running!" -ForegroundColor Green
Write-Host "Access the UI at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Access NocoDB at: http://localhost:8081" -ForegroundColor Cyan
Write-Host ""
Write-Host "Use the following commands to manage the system:" -ForegroundColor Yellow
Write-Host "  - Stop all services: podman pod stop 371gpt-pod" -ForegroundColor White
Write-Host "  - Start all services: podman pod start 371gpt-pod" -ForegroundColor White
Write-Host "  - Remove all services: podman pod rm -f 371gpt-pod" -ForegroundColor White
Write-Host "  - View logs: podman logs -f <container-name> (e.g., podman logs -f ui)" -ForegroundColor White