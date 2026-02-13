"""
BasePage Module
Base class for all page objects following Page Object Model (POM) pattern
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utilities.wait_helper import WaitHelper
from utilities.logger_config import LoggerConfig


class BasePage:
    """
    Base class for all page objects.
    Encapsulates common functionality and WebDriver interactions.
    
    This class provides:
    - Centralized WebDriver management
    - Wait utilities
    - Common element interactions
    - Logging
    """
    
    def __init__(self, driver):
        """
        Initialize BasePage with WebDriver instance
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait_helper = WaitHelper(driver)
        self.logger = LoggerConfig.get_logger(self.__class__.__name__)
        self.logger.debug(f"Initializing {self.__class__.__name__}")
    
    # ==================== Element Interaction Methods ====================
    
    def click_element(self, locator):
        """
        Click on element using Actions or direct click
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
        """
        try:
            element = self.wait_helper.wait_for_element_clickable(locator)
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Error clicking element {locator}: {str(e)}")
            raise
    
    def send_keys(self, locator, text):
        """
        Send text input to element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            text (str): Text to send
        """
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent keys to element {locator}: {text[:20]}...")
        except Exception as e:
            self.logger.error(f"Error sending keys to {locator}: {str(e)}")
            raise
    
    def get_element_text(self, locator):
        """
        Get text content from element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            
        Returns:
            str: Element text content
        """
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            text = element.text
            self.logger.debug(f"Got text from element {locator}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Error getting text from {locator}: {str(e)}")
            raise
    
    def get_element_attribute(self, locator, attribute):
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            attribute (str): Attribute name
            
        Returns:
            str: Attribute value
        """
        try:
            element = self.wait_helper.wait_for_element_present(locator)
            attr_value = element.get_attribute(attribute)
            self.logger.debug(f"Got attribute '{attribute}' from element {locator}: {attr_value}")
            return attr_value
        except Exception as e:
            self.logger.error(f"Error getting attribute '{attribute}' from {locator}: {str(e)}")
            raise
    
    def is_element_displayed(self, locator):
        """
        Check if element is displayed on page
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            
        Returns:
            bool: True if element is displayed
        """
        try:
            element = self.wait_helper.wait_for_element_present(locator)
            is_displayed = element.is_displayed()
            self.logger.debug(f"Element {locator} displayed: {is_displayed}")
            return is_displayed
        except Exception as e:
            self.logger.debug(f"Element {locator} not displayed: {str(e)}")
            return False
    
    def is_element_enabled(self, locator):
        """
        Check if element is enabled
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            
        Returns:
            bool: True if element is enabled
        """
        try:
            element = self.wait_helper.wait_for_element_present(locator)
            is_enabled = element.is_enabled()
            self.logger.debug(f"Element {locator} enabled: {is_enabled}")
            return is_enabled
        except Exception as e:
            self.logger.debug(f"Error checking if element enabled {locator}: {str(e)}")
            return False
    
    def is_element_selected(self, locator):
        """
        Check if element is selected (for checkboxes/radio buttons)
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            
        Returns:
            bool: True if element is selected
        """
        try:
            element = self.wait_helper.wait_for_element_present(locator)
            is_selected = element.is_selected()
            self.logger.debug(f"Element {locator} selected: {is_selected}")
            return is_selected
        except Exception as e:
            self.logger.debug(f"Error checking if element selected {locator}: {str(e)}")
            return False
    
    # ==================== Advanced Interaction Methods ====================
    
    def hover_over_element(self, locator):
        """
        Hover mouse over element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
        """
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            self.logger.error(f"Error hovering over element {locator}: {str(e)}")
            raise
    
    def double_click_element(self, locator):
        """
        Double click on element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
        """
        try:
            element = self.wait_helper.wait_for_element_clickable(locator)
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
            self.logger.info(f"Double clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Error double clicking element {locator}: {str(e)}")
            raise
    
    def right_click_element(self, locator):
        """
        Right click on element
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
        """
        try:
            element = self.wait_helper.wait_for_element_visible(locator)
            actions = ActionChains(self.driver)
            actions.context_click(element).perform()
            self.logger.info(f"Right clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Error right clicking element {locator}: {str(e)}")
            raise
    
    def select_dropdown_by_text(self, locator, text):
        """
        Select dropdown option by visible text
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            text (str): Visible text of option
        """
        try:
            from selenium.webdriver.support.select import Select
            element = self.wait_helper.wait_for_element_visible(locator)
            select = Select(element)
            select.select_by_visible_text(text)
            self.logger.info(f"Selected dropdown option '{text}' in element: {locator}")
        except Exception as e:
            self.logger.error(f"Error selecting dropdown option '{text}' in {locator}: {str(e)}")
            raise
    
    def select_dropdown_by_value(self, locator, value):
        """
        Select dropdown option by value attribute
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            value (str): Value attribute of option
        """
        try:
            from selenium.webdriver.support.select import Select
            element = self.wait_helper.wait_for_element_visible(locator)
            select = Select(element)
            select.select_by_value(value)
            self.logger.info(f"Selected dropdown option with value '{value}' in element: {locator}")
        except Exception as e:
            self.logger.error(f"Error selecting dropdown option '{value}' in {locator}: {str(e)}")
            raise
    
    # ==================== Navigation Methods ====================
    
    def navigate_to(self, url):
        """
        Navigate to URL
        
        Args:
            url (str): URL to navigate to
        """
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Error navigating to {url}: {str(e)}")
            raise
    
    def refresh_page(self):
        """Refresh current page"""
        try:
            self.driver.refresh()
            self.logger.info("Page refreshed")
        except Exception as e:
            self.logger.error(f"Error refreshing page: {str(e)}")
            raise
    
    def go_back(self):
        """Go back to previous page"""
        try:
            self.driver.back()
            self.logger.info("Navigated back")
        except Exception as e:
            self.logger.error(f"Error navigating back: {str(e)}")
            raise
    
    def go_forward(self):
        """Go forward to next page"""
        try:
            self.driver.forward()
            self.logger.info("Navigated forward")
        except Exception as e:
            self.logger.error(f"Error navigating forward: {str(e)}")
            raise
    
    # ==================== Page State Methods ====================
    
    def get_page_title(self):
        """
        Get current page title
        
        Returns:
            str: Page title
        """
        try:
            title = self.driver.title
            self.logger.debug(f"Got page title: {title}")
            return title
        except Exception as e:
            self.logger.error(f"Error getting page title: {str(e)}")
            raise
    
    def get_current_url(self):
        """
        Get current page URL
        
        Returns:
            str: Current URL
        """
        try:
            url = self.driver.current_url
            self.logger.debug(f"Got current URL: {url}")
            return url
        except Exception as e:
            self.logger.error(f"Error getting current URL: {str(e)}")
            raise
    
    def wait_for_page_title(self, title_text):
        """
        Wait for page title to contain text
        
        Args:
            title_text (str): Text that should be in title
            
        Returns:
            bool: True when title contains text
        """
        return self.wait_helper.wait_for_title_contains(title_text)
    
    def wait_for_url(self, url_text):
        """
        Wait for URL to contain text
        
        Args:
            url_text (str): Text that should be in URL
            
        Returns:
            bool: True when URL contains text
        """
        return self.wait_helper.wait_for_url_contains(url_text)
