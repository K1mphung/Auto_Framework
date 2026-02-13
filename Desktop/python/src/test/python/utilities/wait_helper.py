"""
Wait Helper Module
Provides explicit wait utilities using Selenium WebDriverWait
"""

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.logger_config import LoggerConfig
from config.config_reader import ConfigReader


class WaitHelper:
    """
    Utility class for explicit waits in Selenium.
    Uses WebDriverWait with custom timeout from configuration.
    """
    
    logger = LoggerConfig.get_logger(__name__)
    config = ConfigReader()
    
    def __init__(self, driver, wait_time=None):
        """
        Initialize WaitHelper with WebDriver instance
        
        Args:
            driver: Selenium WebDriver instance
            wait_time (int): Timeout in seconds. Uses config value if None.
        """
        self.driver = driver
        self.wait_time = wait_time or self.config.get_explicit_wait()
        self.wait = WebDriverWait(driver, self.wait_time)
        self.logger.debug(f"WaitHelper initialized with timeout: {self.wait_time}s")
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            timeout (int): Custom timeout in seconds
            
        Returns:
            WebElement: The element when it becomes visible
            
        Raises:
            TimeoutException: If element not visible within timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            element = wait_obj.until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"Element {locator} is visible")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element visibility: {locator}")
            raise
    
    def wait_for_element_present(self, locator, timeout=None):
        """
        Wait for element to be present in DOM
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            timeout (int): Custom timeout in seconds
            
        Returns:
            WebElement: The element when it's present in DOM
            
        Raises:
            TimeoutException: If element not present within timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            element = wait_obj.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element {locator} is present in DOM")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element presence: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            timeout (int): Custom timeout in seconds
            
        Returns:
            WebElement: The element when it becomes clickable
            
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            element = wait_obj.until(EC.element_to_be_clickable(locator))
            self.logger.debug(f"Element {locator} is clickable")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element to be clickable: {locator}")
            raise
    
    def wait_for_element_invisible(self, locator, timeout=None):
        """
        Wait for element to be invisible or removed from DOM
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            timeout (int): Custom timeout in seconds
            
        Returns:
            bool: True if element became invisible
            
        Raises:
            TimeoutException: If element still visible after timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            result = wait_obj.until(EC.invisibility_of_element_located(locator))
            self.logger.debug(f"Element {locator} is invisible")
            return result
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element invisibility: {locator}")
            raise
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """
        Wait for specific text to appear in element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            text (str): Text to wait for
            timeout (int): Custom timeout in seconds
            
        Returns:
            bool: True when text appears
            
        Raises:
            TimeoutException: If text not found within timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            result = wait_obj.until(EC.text_to_be_present_in_element(locator, text))
            self.logger.debug(f"Text '{text}' found in element {locator}")
            return result
        except TimeoutException:
            self.logger.error(f"Timeout waiting for text '{text}' in element {locator}")
            raise
    
    def wait_for_url_contains(self, url_text, timeout=None):
        """
        Wait for URL to contain specific text
        
        Args:
            url_text (str): Text that should be in URL
            timeout (int): Custom timeout in seconds
            
        Returns:
            bool: True when URL contains text
            
        Raises:
            TimeoutException: If URL doesn't contain text within timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            result = wait_obj.until(EC.url_contains(url_text))
            self.logger.debug(f"URL contains '{url_text}'")
            return result
        except TimeoutException:
            self.logger.error(f"Timeout waiting for URL to contain: {url_text}")
            raise
    
    def wait_for_title_contains(self, title_text, timeout=None):
        """
        Wait for page title to contain specific text
        
        Args:
            title_text (str): Text that should be in title
            timeout (int): Custom timeout in seconds
            
        Returns:
            bool: True when title contains text
            
        Raises:
            TimeoutException: If title doesn't contain text within timeout
        """
        try:
            wait_obj = WebDriverWait(self.driver, timeout or self.wait_time)
            result = wait_obj.until(EC.title_contains(title_text))
            self.logger.debug(f"Page title contains '{title_text}'")
            return result
        except TimeoutException:
            self.logger.error(f"Timeout waiting for title to contain: {title_text}")
            raise
