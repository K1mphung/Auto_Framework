"""
Logger Configuration Module
Configures logging for the test framework with file and console handlers
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


class LoggerConfig:
    """
    Configures and manages logging for the framework.
    Provides centralized logging to console and file.
    """
    
    _logger = None
    
    @staticmethod
    def get_logger(name=None, log_level=logging.INFO, log_dir='./logs'):
        """
        Get or create a logger instance
        
        Args:
            name (str): Logger name (typically __name__)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir (str): Directory to store log files
            
        Returns:
            logging.Logger: Configured logger instance
        """
        if LoggerConfig._logger is not None:
            return LoggerConfig._logger
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Create logger instance
        logger = logging.getLogger(name or 'AutoLogin')
        logger.setLevel(log_level)
        
        # Remove existing handlers to avoid duplicates
        logger.handlers = []
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File Handler with rotation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_path / f'automation_test_{timestamp}.log'
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(log_file),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        LoggerConfig._logger = logger
        return logger
    
    @staticmethod
    def reset_logger():
        """Reset logger instance (useful for testing)"""
        LoggerConfig._logger = None
