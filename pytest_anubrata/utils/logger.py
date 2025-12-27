"""
Logging utility for test automation framework.
Provides centralized logging configuration and utilities.
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler


class Logger:
    """Custom logger class for test automation."""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name="test_automation", log_level=logging.INFO):
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name
            log_level: Logging level (default: INFO)
        
        Returns:
            Logger instance
        """
        if name not in Logger._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(log_level)
            logger.handlers.clear()  # Remove any existing handlers
            
            # Create logs directory if it doesn't exist
            log_dir = Path(__file__).parent.parent.parent / "pytest_anubrata" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Create formatters
            detailed_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            
            # File handler with rotation
            log_file = log_dir / f"test_execution_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(console_formatter)
            
            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            Logger._loggers[name] = logger
        
        return Logger._loggers[name]


def get_logger(name="test_automation"):
    """Convenience function to get logger instance."""
    return Logger.get_logger(name)

