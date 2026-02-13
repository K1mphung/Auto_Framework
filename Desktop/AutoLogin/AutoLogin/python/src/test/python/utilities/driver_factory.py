"""
WebDriver Factory Module
Creates and manages WebDriver instances for Chrome and Firefox browsers
Supports headless mode and configuration via properties
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utilities.logger_config import LoggerConfig
from config.config_reader import ConfigReader


class DriverFactory:
    """
    Factory class for WebDriver creation.
    Supports Chrome and Firefox browsers with configuration options.
    Uses webdriver-manager for automatic driver management.
    """
    
    logger = LoggerConfig.get_logger(__name__)
    config = ConfigReader()
    
    @staticmethod
    def create_driver(browser_name=None, headless=None):
        """
        Create WebDriver instance based on browser name and configuration
        
        Args:
            browser_name (str): Browser type ('chrome' or 'firefox'). 
                               If None, reads from config.
            headless (bool): Run browser in headless mode. 
                            If None, reads from config.
                            
        Returns:
            WebDriver: Configured WebDriver instance
            
        Raises:
            ValueError: If browser type is not supported
        """
        browser = (browser_name or DriverFactory.config.get_browser()).lower()
        is_headless = headless if headless is not None else DriverFactory.config.get_headless_mode()
        
        DriverFactory.logger.info(f"Creating {browser} WebDriver (headless={is_headless})")
        
        if browser == 'chrome':
            return DriverFactory._create_chrome_driver(is_headless)
        elif browser == 'firefox':
            return DriverFactory._create_firefox_driver(is_headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """
        Create Chrome WebDriver with option settings
        
        Args:
            headless (bool): Run in headless mode
            
        Returns:
            WebDriver: Chrome WebDriver instance
        """
        try:
            chrome_options = ChromeOptions()
            
            # Common arguments
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            if headless:
                chrome_options.add_argument('--headless=new')
            
            # Create service with webdriver-manager
            service = ChromeService(ChromeDriverManager().install())
            
            # Create driver
            driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            # Set implicit wait
            implicit_wait = DriverFactory.config.get_implicit_wait()
            driver.implicitly_wait(implicit_wait)
            
            # Maximize window
            driver.maximize_window()
            
            DriverFactory.logger.info("Chrome WebDriver created successfully")
            return driver
            
        except Exception as e:
            DriverFactory.logger.error(f"Error creating Chrome WebDriver: {str(e)}")
            raise
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """
        Create Firefox WebDriver with option settings
        
        Args:
            headless (bool): Run in headless mode
            
        Returns:
            WebDriver: Firefox WebDriver instance
        """
        try:
            firefox_options = FirefoxOptions()
            
            if headless:
                firefox_options.add_argument('--headless')
            
            # Additional preferences
            firefox_options.set_preference('dom.webdriver.enabled', False)
            
            # Create service with webdriver-manager
            service = FirefoxService(GeckoDriverManager().install())
            
            # Create driver
            driver = webdriver.Firefox(
                service=service,
                options=firefox_options
            )
            
            # Set implicit wait
            implicit_wait = DriverFactory.config.get_implicit_wait()
            driver.implicitly_wait(implicit_wait)
            
            # Maximize window
            driver.maximize_window()
            
            DriverFactory.logger.info("Firefox WebDriver created successfully")
            return driver
            
        except Exception as e:
            DriverFactory.logger.error(f"Error creating Firefox WebDriver: {str(e)}")
            raise
    
    @staticmethod
    def quit_driver(driver):
        """
        Safely quit WebDriver
        
        Args:
            driver: WebDriver instance to quit
        """
        try:
            if driver:
                driver.quit()
                DriverFactory.logger.info("WebDriver closed successfully")
        except Exception as e:
            DriverFactory.logger.error(f"Error closing WebDriver: {str(e)}")
