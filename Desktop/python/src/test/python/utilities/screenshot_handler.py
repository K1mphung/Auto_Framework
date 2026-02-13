"""
Screenshot Handler Module
Handles screenshot capture on test failures and general diagnostics
"""

from pathlib import Path
from datetime import datetime
from utilities.logger_config import LoggerConfig
from config.config_reader import ConfigReader


class ScreenshotHandler:
    """
    Utility class for capturing and managing screenshots.
    Supports capturing on failures with automatic naming and organization.
    """
    
    logger = LoggerConfig.get_logger(__name__)
    config = ConfigReader()
    
    def __init__(self, screenshot_dir=None):
        """
        Initialize ScreenshotHandler
        
        Args:
            screenshot_dir (str): Directory to save screenshots. 
                                 Uses config value if None.
        """
        self.screenshot_dir = Path(screenshot_dir or self.config.get_screenshot_path())
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"Screenshot directory: {self.screenshot_dir}")
    
    def capture_screenshot(self, driver, filename=None, test_name=None):
        """
        Capture screenshot from WebDriver
        
        Args:
            driver: Selenium WebDriver instance
            filename (str): Custom filename for screenshot.
                           If None, generates automatic name with timestamp.
            test_name (str): Test name to include in filename
            
        Returns:
            str: Full path to saved screenshot
            
        Raises:
            Exception: If screenshot capture fails
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
                if test_name:
                    filename = f"{test_name}_{timestamp}.png"
                else:
                    filename = f"screenshot_{timestamp}.png"
            
            screenshot_path = self.screenshot_dir / filename
            driver.save_screenshot(str(screenshot_path))
            
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            self.logger.error(f"Error capturing screenshot: {str(e)}")
            raise
    
    def capture_screenshot_on_failure(self, driver, test_name):
        """
        Capture screenshot with failure naming convention
        
        Args:
            driver: Selenium WebDriver instance
            test_name (str): Test name that failed
            
        Returns:
            str: Full path to failure screenshot
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"FAILURE_{test_name}_{timestamp}.png"
        
        self.logger.warning(f"Test failed, capturing screenshot: {test_name}")
        return self.capture_screenshot(driver, filename)
    
    def get_latest_screenshot(self):
        """
        Get path to latest screenshot
        
        Returns:
            str: Path to latest screenshot file or None if no screenshots
        """
        try:
            screenshots = sorted(
                self.screenshot_dir.glob('*.png'),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            if screenshots:
                return str(screenshots[0])
            return None
        except Exception as e:
            self.logger.error(f"Error getting latest screenshot: {str(e)}")
            return None
    
    def cleanup_old_screenshots(self, keep_count=50):
        """
        Remove old screenshots, keeping only the most recent ones
        
        Args:
            keep_count (int): Number of recent screenshots to keep
        """
        try:
            screenshots = sorted(
                self.screenshot_dir.glob('*.png'),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            
            if len(screenshots) > keep_count:
                for screenshot in screenshots[keep_count:]:
                    screenshot.unlink()
                    self.logger.debug(f"Deleted old screenshot: {screenshot}")
                    
        except Exception as e:
            self.logger.error(f"Error cleaning up screenshots: {str(e)}")
