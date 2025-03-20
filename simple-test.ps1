# Simple test script for 371GPT components
# This simplifies testing by focusing on one component at a time

param (
    [Parameter()]
    [string]$Component = "ui",
    
    [Parameter()]
    [int]$Port = 8000,
    
    [Parameter()]
    [switch]$CleanUp = $false
)

function Test-UI {
    Write-Host "Testing UI component..." -ForegroundColor Green
    
    # Clean up existing resources
    podman pod rm -f 371gpt-ui-test 2>$null
    
    # Create pod
    podman pod create --name 371gpt-ui-test -p ${Port}:8000
    
    # Build and run
    Write-Host "Building UI component..." -ForegroundColor Yellow
    podman build -t 371gpt-ui-test ./services/ui
    
    Write-Host "Running UI component..." -ForegroundColor Yellow
    podman run -d --pod 371gpt-ui-test --name ui-test -e JWT_SECRET=test-secret 371gpt-ui-test
    
    Write-Host "UI should be accessible at: http://localhost:${Port}" -ForegroundColor Cyan
}

function Test-Database {
    Write-Host "Testing Database component..." -ForegroundColor Green
    
    # Clean up existing resources
    podman pod rm -f 371gpt-db-test 2>$null
    
    # Create pod
    podman pod create --name 371gpt-db-test -p ${Port}:5432
    
    # Run
    Write-Host "Running PostgreSQL..." -ForegroundColor Yellow
    podman run -d --pod 371gpt-db-test --name db-test -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:15-alpine
    
    Write-Host "Database should be accessible at: localhost:${Port}" -ForegroundColor Cyan
    Write-Host "Username: test" -ForegroundColor Cyan
    Write-Host "Password: test" -ForegroundColor Cyan
    Write-Host "Database: testdb" -ForegroundColor Cyan
}

function Test-Orchestrator {
    Write-Host "Testing Orchestrator component..." -ForegroundColor Green
    
    # Clean up existing resources
    podman pod rm -f 371gpt-orch-test 2>$null
    
    # Create pod
    podman pod create --name 371gpt-orch-test -p ${Port}:8080
    
    # Build and run
    Write-Host "Building Orchestrator component..." -ForegroundColor Yellow
    podman build -t 371gpt-orch-test ./services/orchestrator
    
    Write-Host "Running Orchestrator component..." -ForegroundColor Yellow
    podman run -d --pod 371gpt-orch-test --name orch-test -e JWT_SECRET=test-secret 371gpt-orch-test
    
    Write-Host "Orchestrator API should be accessible at: http://localhost:${Port}" -ForegroundColor Cyan
}

function Clean-All {
    Write-Host "Cleaning up all test resources..." -ForegroundColor Yellow
    
    podman pod rm -f 371gpt-ui-test 2>$null
    podman pod rm -f 371gpt-db-test 2>$null
    podman pod rm -f 371gpt-orch-test 2>$null
    
    Write-Host "All test pods removed." -ForegroundColor Green
}

# Execute based on component parameter
if ($CleanUp) {
    Clean-All
    exit 0
}

switch ($Component.ToLower()) {
    "ui" { Test-UI }
    "database" { Test-Database }
    "db" { Test-Database }
    "orchestrator" { Test-Orchestrator }
    "orch" { Test-Orchestrator }
    default {
        Write-Host "Unknown component: $Component" -ForegroundColor Red
        Write-Host "Valid options: ui, database (db), orchestrator (orch)" -ForegroundColor Yellow
    }
}

# Display help
Write-Host ""
Write-Host "To test a different component:" -ForegroundColor Yellow
Write-Host "  .\simple-test.ps1 -Component ui|db|orchestrator -Port 8000" -ForegroundColor White
Write-Host ""
Write-Host "To clean up all test resources:" -ForegroundColor Yellow  
Write-Host "  .\simple-test.ps1 -CleanUp" -ForegroundColor White