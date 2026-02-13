"""
Configuration Reader Module
Handles reading configuration properties from config.properties file
"""

import os
import configparser
from pathlib import Path


class ConfigReader:
    """
    Reads and manages configuration properties for the test framework.
    Follows singleton pattern to ensure single instance.
    """
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from properties file"""
        try:
            # Get the path to config.properties
            config_path = Path(__file__).parent.parent / "config" / "config.properties"
            
            if not config_path.exists():
                raise FileNotFoundError(f"Config file not found at {config_path}")
            
            self._config = configparser.ConfigParser()
            self._config.read(config_path)
            
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            raise
    
    def get(self, section, key, default=None):
        """
        Get configuration value
        
        Args:
            section (str): Section in config file
            key (str): Key name
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            if self._config.has_option(section, key):
                return self._config.get(section, key)
            return default
        except Exception as e:
            print(f"Error reading config {section}.{key}: {str(e)}")
            return default
    
    def get_browser(self):
        """Get browser type from config"""
        return self.get('browser', 'name', 'chrome')
    
    def get_base_url(self):
        """Get base URL from config"""
        return self.get('application', 'base_url', 'http://localhost:8080')
    
    def get_implicit_wait(self):
        """Get implicit wait time from config"""
        return int(self.get('wait', 'implicit_wait', '10'))
    
    def get_explicit_wait(self):
        """Get explicit wait time from config"""
        return int(self.get('wait', 'explicit_wait', '15'))
    
    def get_headless_mode(self):
        """Get headless mode setting from config"""
        value = self.get('browser', 'headless', 'false')
        return value.lower() == 'true'
    
    def get_screenshot_enabled(self):
        """Get screenshot on failure setting from config"""
        value = self.get('screenshot', 'on_failure', 'true')
        return value.lower() == 'true'
    
    def get_screenshot_path(self):
        """Get screenshot directory path from config"""
        return self.get('screenshot', 'path', './screenshots')
    
    def get_report_path(self):
        """Get report directory path from config"""
        return self.get('reporting', 'report_path', './reports')
    
    def get_log_level(self):
        """Get logging level from config"""
        return self.get('logging', 'level', 'INFO')
    
    def get_log_path(self):
        """Get log file path from config"""
        return self.get('logging', 'log_path', './logs')
