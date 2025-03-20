import os
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

import httpx
from loguru import logger
from nicegui import ui, app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8080")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
JWT_SECRET = os.getenv("JWT_SECRET", "371gpt-jwt-secret")

# Setup logging
logger.remove()
logger.add(
    "logs/ui.log", 
    rotation="10 MB", 
    level=LOG_LEVEL, 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(lambda msg: app.storage.user.setdefault("logs", []).append(msg), level=LOG_LEVEL)

# API client for connecting to the orchestrator
class OrchestratorClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_agents(self) -> List[Dict[str, Any]]:
        try:
            response = await self.client.get(f"{self.base_url}/agents")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching agents: {str(e)}")
            return []

    async def register_agent(self, agent_info: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self.client.post(
                f"{self.base_url}/agents", 
                json=agent_info
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error registering agent: {str(e)}")
            return {"error": str(e)}

    async def create_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = await self.client.post(
                f"{self.base_url}/tasks", 
                json=task_info
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return {"error": str(e)}

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"{self.base_url}/tasks/{task_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching task status: {str(e)}")
            return {"error": str(e)}

    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        try:
            response = await self.client.post(f"{self.base_url}/tasks/{task_id}/execute")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error executing task: {str(e)}")
            return {"error": str(e)}

    async def get_health(self) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error checking health: {str(e)}")
            return {"status": "error", "error": str(e)}

# Initialize client
orchestrator_client = OrchestratorClient(ORCHESTRATOR_URL)

# UI Elements
@ui.page('/')
def index():
    with ui.header().classes('bg-blue-900 text-white'):
        ui.label('371GPT - AI Agent Orchestration System').classes('text-2xl font-bold')
        with ui.row():
            ui.button('Dashboard', on_click=lambda: ui.navigate('/dashboard')).props('flat color=white')
            ui.button('Agents', on_click=lambda: ui.navigate('/agents')).props('flat color=white')
            ui.button('Tasks', on_click=lambda: ui.navigate('/tasks')).props('flat color=white')
            ui.button('Logs', on_click=lambda: ui.navigate('/logs')).props('flat color=white')
            ui.button('Settings', on_click=lambda: ui.navigate('/settings')).props('flat color=white')
    
    with ui.card().classes('w-full max-w-3xl mx-auto mt-8'):
        ui.label('Welcome to 371GPT').classes('text-2xl font-bold')
        ui.label('A scalable, ethical AI orchestration system based on the DSF model').classes('text-gray-700')
        
        with ui.row().classes('mt-4'):
            ui.button('Go to Dashboard', on_click=lambda: ui.navigate('/dashboard')).props('color=primary')
            ui.button('View Documentation', on_click=lambda: ui.open('https://github.com/ab1355/371GPT')).props('color=secondary')

@ui.page('/dashboard')
async def dashboard():
    ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    
    with ui.header().classes('bg-blue-900 text-white'):
        ui.label('371GPT Dashboard').classes('text-2xl font-bold')
        ui.button('Home', on_click=lambda: ui.navigate('/')).props('flat color=white')

    # System status card
    with ui.card().classes('w-full mx-auto my-4'):
        ui.label('System Status').classes('text-xl font-bold')
        
        status_label = ui.label('Loading system status...').classes('text-gray-700')
        system_stats = ui.row().classes('w-full justify-between mt-4')
        
        # Update system status periodically
        async def update_system_status():
            try:
                health = await orchestrator_client.get_health()
                if health.get('status') == 'healthy':
                    status_label.set_text('System Online').classes('text-green-600')
                else:
                    status_label.set_text(f"System Error: {health.get('error', 'Unknown error')}").classes('text-red-600')
                
                system_stats.clear()
                with system_stats:
                    ui.card().classes('w-1/4').style('max-width: 200px; min-width: 150px;').tight()
                    with ui.card_section():
                        ui.label('Agents').classes('text-lg font-bold')
                        agents = await orchestrator_client.get_agents()
                        ui.label(str(len(agents))).classes('text-3xl text-blue-600')
                    
                    ui.card().classes('w-1/4').style('max-width: 200px; min-width: 150px;').tight()
                    with ui.card_section():
                        ui.label('Tasks').classes('text-lg font-bold')
                        ui.label('0').classes('text-3xl text-blue-600')  # Placeholder, would need an API call
                    
                    ui.card().classes('w-1/4').style('max-width: 200px; min-width: 150px;').tight()
                    with ui.card_section():
                        ui.label('Uptime').classes('text-lg font-bold')
                        ui.label('0h 0m').classes('text-3xl text-blue-600')  # Placeholder, would need an API call
                    
                    ui.card().classes('w-1/4').style('max-width: 200px; min-width: 150px;').tight()
                    with ui.card_section():
                        ui.label('Errors').classes('text-lg font-bold')
                        ui.label('0').classes('text-3xl text-blue-600')  # Placeholder, would need an API call
                
            except Exception as e:
                status_label.set_text(f'Error: {str(e)}').classes('text-red-600')
        
        update_system_status()
        
        # Auto-refresh system status
        ui.timer(5.0, update_system_status)
    
    # Recent activity card
    with ui.card().classes('w-full mx-auto my-4'):
        ui.label('Recent Activity').classes('text-xl font-bold')
        
        with ui.table().classes('w-full').props('bordered dense rows-per-page=10'):
            ui.table_column('Timestamp', 'timestamp')
            ui.table_column('Agent', 'agent')
            ui.table_column('Action', 'action')
            ui.table_column('Status', 'status')
            
            # Sample data - would be replaced with real API calls
            ui.table_rows([
                {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent': 'CEO Orchestrator', 'action': 'System Startup', 'status': 'Completed'},
                {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent': 'Research Agent', 'action': 'Data Collection', 'status': 'In Progress'},
                {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'agent': 'Development Agent', 'action': 'Code Review', 'status': 'Pending'},
            ])

    # Quick actions card
    with ui.card().classes('w-full mx-auto my-4'):
        ui.label('Quick Actions').classes('text-xl font-bold')
        
        with ui.row().classes('w-full justify-between mt-4'):
            ui.button('Create Task', on_click=lambda: ui.navigate('/tasks/new')).props('color=primary')
            ui.button('Register Agent', on_click=lambda: ui.navigate('/agents/new')).props('color=primary')
            ui.button('View Logs', on_click=lambda: ui.navigate('/logs')).props('color=primary')
            ui.button('System Settings', on_click=lambda: ui.navigate('/settings')).props('color=primary')

@ui.page('/logs')
def logs():
    with ui.header().classes('bg-blue-900 text-white'):
        ui.label('System Logs').classes('text-2xl font-bold')
        ui.button('Home', on_click=lambda: ui.navigate('/')).props('flat color=white')
    
    # Log filtering controls
    with ui.card().classes('w-full mx-auto my-4'):
        with ui.row().classes('items-center'):
            ui.label('Log Filters:').classes('font-bold')
            log_level = ui.select(
                ['ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                value='ALL', 
                label='Log Level'
            )
            agent_filter = ui.select(
                ['ALL', 'CEO Orchestrator', 'Research Agent', 'Development Agent', 'Communication Agent'], 
                value='ALL', 
                label='Agent'
            )
            ui.button('Apply Filters', icon='filter_alt')
            ui.button('Clear Filters', icon='clear').props('outline')
    
    # Real-time log viewer
    with ui.card().classes('w-full mx-auto my-4'):
        ui.label('Real-Time Logs').classes('text-xl font-bold')
        
        # Create a container for logs with fixed height and scrolling
        log_container = ui.element('div').classes('w-full h-96 overflow-auto bg-gray-100 p-4 font-mono text-sm')
        
        # Function to update logs
        async def update_logs():
            # In a real implementation, you'd fetch logs from the backend
            # Here we're simulating logs for demonstration
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            log_entry = f"{time_now} | INFO | Simulated log entry for demonstration"
            
            # Add the log to the container
            with log_container:
                ui.label(log_entry).classes('text-xs py-1 border-b border-gray-200 w-full break-all')
            
            # Scroll to bottom
            ui.run_javascript('''
                document.querySelectorAll('.overflow-auto').forEach(el => {
                    el.scrollTop = el.scrollHeight;
                });
            ''')
        
        # Add some initial logs
        with log_container:
            for i in range(5):
                time_val = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                ui.label(f"{time_val} | INFO | System initialization... ({i}/5)").classes('text-xs py-1 border-b border-gray-200 w-full')
        
        # Auto-update logs
        ui.timer(3.0, update_logs)
        
        # Controls for logs
        with ui.row().classes('w-full justify-between mt-4'):
            ui.button('Pause', icon='pause').props('color=warning')
            ui.button('Resume', icon='play_arrow').props('color=positive')
            ui.button('Clear Logs', icon='delete').props('color=negative')
            ui.button('Download Logs', icon='download')

@ui.page('/healthz')
def healthcheck():
    return 'OK'

# Start the application
ui.run(title='371GPT UI', host='0.0.0.0', port=8000, reload=False)