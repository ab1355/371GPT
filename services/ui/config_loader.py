import os
import json
from typing import Dict, Any, Optional
from loguru import logger

class UIConfigLoader:
    """
    Loads and manages UI configuration from JSON files.
    This allows non-technical users to modify the UI appearance and behavior
    without changing code.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the UI configuration JSON file
        """
        self.config_path = config_path or os.environ.get(
            "UI_CONFIG_PATH", 
            "/app/config/ui/ui-config.json"
        )
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the JSON file.
        
        Returns:
            Dict containing UI configuration
        """
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                logger.info(f"Loaded UI configuration from {self.config_path}")
                return config
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to load UI configuration: {str(e)}. Using defaults.")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Provide default configuration if the config file is not available.
        
        Returns:
            Dict containing default UI configuration
        """
        return {
            "theme": {
                "primary_color": "#1E3A8A",
                "secondary_color": "#4F46E5",
                "dark_mode": False
            },
            "layout": {
                "sidebar_width": "250px",
                "content_max_width": "1200px"
            },
            "dashboard": {
                "auto_refresh_interval": 5,
                "show_system_stats": True
            },
            "logs": {
                "auto_refresh_interval": 3,
                "max_visible_logs": 100
            }
        }
    
    def get_config(self, section: Optional[str] = None) -> Dict[str, Any]:
        """
        Get configuration, optionally for a specific section.
        
        Args:
            section: Optional section name to retrieve
            
        Returns:
            Dict containing requested configuration
        """
        if section:
            return self.config.get(section, {})
        return self.config
    
    def reload_config(self) -> bool:
        """
        Reload configuration from the file.
        
        Returns:
            bool: Success status
        """
        try:
            self.config = self._load_config()
            logger.info("UI configuration reloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to reload UI configuration: {str(e)}")
            return False
    
    def get_theme(self) -> Dict[str, Any]:
        """
        Get theme configuration.
        
        Returns:
            Dict containing theme configuration
        """
        return self.get_config("theme")
    
    def get_layout(self) -> Dict[str, Any]:
        """
        Get layout configuration.
        
        Returns:
            Dict containing layout configuration
        """
        return self.get_config("layout")
    
    def get_dashboard_config(self) -> Dict[str, Any]:
        """
        Get dashboard configuration.
        
        Returns:
            Dict containing dashboard configuration
        """
        return self.get_config("dashboard")
    
    def get_logs_config(self) -> Dict[str, Any]:
        """
        Get logs configuration.
        
        Returns:
            Dict containing logs configuration
        """
        return self.get_config("logs")

# Singleton pattern for config loader
_config_loader = None

def get_config_loader() -> UIConfigLoader:
    """
    Get or create the singleton config loader instance.
    
    Returns:
        UIConfigLoader instance
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = UIConfigLoader()
    return _config_loader