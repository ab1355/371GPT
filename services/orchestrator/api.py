from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
import logging

from orchestrator_agent import OrchestratorAgent

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator-api")

# Initialize FastAPI app
app = FastAPI(
    title="371GPT Orchestrator API",
    description="API for the CEO Orchestrator Agent",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator agent
orchestrator = OrchestratorAgent()

# Pydantic models for request/response validation
class AgentInfo(BaseModel):
    name: str
    endpoint: str
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None

class TaskCreate(BaseModel):
    description: str
    priority: str = Field(default="medium", regex="^(low|medium|high|highest)$")
    metadata: Optional[Dict[str, Any]] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    created_at: str

class AgentResponse(BaseModel):
    id: str
    name: str
    endpoint: str
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# Health check endpoint
@app.get("/health", status_code=200)
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Register a new agent
@app.post("/agents", response_model=AgentResponse, status_code=201)
def register_agent(agent_info: AgentInfo):
    try:
        agent_id = f"{agent_info.name.lower().replace(' ', '_')}_agent"
        success = orchestrator.register_agent(agent_id, agent_info.dict())
        
        if not success:
            raise HTTPException(
                status_code=400, 
                detail="Failed to register agent"
            )
        
        return {"id": agent_id, **agent_info.dict()}
    except Exception as e:
        logger.error(f"Error registering agent: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# List all registered agents
@app.get("/agents", response_model=List[AgentResponse])
def list_agents():
    try:
        agents = orchestrator.list_agents()
        return agents
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Unregister an agent
@app.delete("/agents/{agent_id}", status_code=204)
def unregister_agent(agent_id: str):
    try:
        success = orchestrator.unregister_agent(agent_id)
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail=f"Agent {agent_id} not found"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unregistering agent: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Create a new task
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    try:
        task_id = orchestrator.create_task(
            task_description=task.description,
            priority=task.priority
        )
        
        return {
            "task_id": task_id,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Get task status
@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    try:
        status = orchestrator.get_task_status(task_id)
        
        if "error" in status:
            raise HTTPException(
                status_code=404, 
                detail=f"Task {task_id} not found"
            )
        
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Execute a task
@app.post("/tasks/{task_id}/execute", status_code=200)
def execute_task(task_id: str):
    try:
        success = orchestrator.execute_task(task_id)
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail=f"Task {task_id} not found or cannot be executed"
            )
        
        return {"status": "executing", "task_id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Exception handler for custom error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)