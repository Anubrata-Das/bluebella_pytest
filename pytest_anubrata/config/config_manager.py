"""
Configuration Manager for Test Automation Framework.
Handles reading configuration from config.ini file.
"""
import os
import configparser
from pathlib import Path


class ConfigManager:
    """Manages configuration settings for the test automation framework."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """Singleton pattern to ensure single configuration instance."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from config.ini file."""
        config = configparser.ConfigParser()
        # Get the root directory (project root)
        root_dir = Path(__file__).parent.parent.parent
        config_file = root_dir / "pytest_anubrata" / "config" / "config.ini"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        config.read(config_file)
        self._config = config
    
    def get(self, section, option, fallback=None):
        """Get configuration value from specified section and option."""
        return self._config.get(section, option, fallback=fallback)
    
    def getint(self, section, option, fallback=None):
        """Get integer configuration value."""
        return self._config.getint(section, option, fallback=fallback)
    
    def getboolean(self, section, option, fallback=None):
        """Get boolean configuration value."""
        return self._config.getboolean(section, option, fallback=fallback)
    
    # Convenience methods for common configurations
    @property
    def base_url(self):
        """Get base URL for the application."""
        return self.get("DEFAULT", "base_url")
    
    @property
    def default_timeout(self):
        """Get default timeout for waits."""
        return self.getint("Test", "default_timeout", 10)
    
    @property
    def short_timeout(self):
        """Get short timeout for quick waits."""
        return self.getint("Test", "short_timeout", 5)
    
    @property
    def long_timeout(self):
        """Get long timeout for extended waits."""
        return self.getint("Test", "long_timeout", 20)
    
    @property
    def default_browser(self):
        """Get default browser name."""
        return self.get("Browser", "default_browser", "chrome")
    
    @property
    def implicit_wait(self):
        """Get implicit wait time for WebDriver."""
        return self.getint("DEFAULT", "implicit_wait", 5)
    
    @property
    def test_data_path(self):
        """Get test data file path."""
        path = self.get("Paths", "test_data_path")
        root_dir = Path(__file__).parent.parent.parent
        return root_dir / path
    
    @property
    def screenshots_path(self):
        """Get screenshots directory path."""
        path = self.get("Paths", "screenshots_path")
        root_dir = Path(__file__).parent.parent.parent
        full_path = root_dir / path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path
    
    @property
    def reports_path(self):
        """Get reports directory path."""
        path = self.get("Paths", "reports_path")
        root_dir = Path(__file__).parent.parent.parent
        full_path = root_dir / path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path
    
    @property
    def logs_path(self):
        """Get logs directory path."""
        path = self.get("Paths", "logs_path")
        root_dir = Path(__file__).parent.parent.parent
        full_path = root_dir / path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path


# Global configuration instance
config = ConfigManager()

