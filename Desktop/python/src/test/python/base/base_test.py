"""
BaseTest Module
Base test class providing common setup, teardown, and utilities for all test cases
"""

import pytest
from utilities.driver_factory import DriverFactory
from utilities.logger_config import LoggerConfig
from utilities.screenshot_handler import ScreenshotHandler
from config.config_reader import ConfigReader


class BaseTest:
    """
    Base class for all test cases.
    Provides:
    - WebDriver setup and teardown
    - Logging configuration
    - Screenshot handling
    - Common test utilities
    
    All test classes should inherit from this class.
    """
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Automatic setup and teardown fixture for each test
        """
        # Setup
        self.logger = LoggerConfig.get_logger(self.__class__.__name__)
        self.config = ConfigReader()
        self.driver = DriverFactory.create_driver()
        self.screenshot_handler = ScreenshotHandler()
        
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Starting test: {self._get_test_name()}")
        self.logger.info(f"{'='*60}")
        
        yield
        
        # Teardown
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Finishing test: {self._get_test_name()}")
        self.logger.info(f"{'='*60}")
        
        try:
            DriverFactory.quit_driver(self.driver)
        except Exception as e:
            self.logger.error(f"Error during teardown: {str(e)}")
    
    def _get_test_name(self):
        """
        Get current test method name
        
        Returns:
            str: Test method name
        """
        # Extract test method name from the current test context
        return self.__class__.__name__
    
    # ==================== Common Test Utilities ====================
    
    def navigate_to_app(self):
        """
        Navigate to application base URL from config
        """
        try:
            base_url = self.config.get_base_url()
            self.driver.get(base_url)
            self.logger.info(f"Navigated to base URL: {base_url}")
        except Exception as e:
            self.logger.error(f"Error navigating to application: {str(e)}")
            self.take_screenshot("navigation_error")
            raise
    
    def take_screenshot(self, filename_prefix=None):
        """
        Capture screenshot with optional filename prefix
        
        Args:
            filename_prefix (str): Prefix for screenshot filename
            
        Returns:
            str: Path to screenshot file
        """
        try:
            test_name = self._get_test_name()
            if filename_prefix:
                filename = f"{test_name}_{filename_prefix}.png"
            else:
                filename = f"{test_name}.png"
            
            screenshot_path = self.screenshot_handler.capture_screenshot(
                self.driver, 
                filename
            )
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return None
    
    # ==================== Assertion Methods ====================
    
    def assert_text_in_page(self, text, locator=None):
        """
        Assert that text is present in page or element
        
        Args:
            text (str): Text to verify
            locator (tuple): Optional element locator. If None, checks full page.
            
        Raises:
            AssertionError: If text not found
        """
        try:
            if locator:
                element_text = self.driver.find_element(*locator).text
                assert text in element_text, f"Text '{text}' not found in element"
            else:
                page_text = self.driver.page_source
                assert text in page_text, f"Text '{text}' not found in page"
            
            self.logger.info(f"Assertion passed: Text '{text}' found")
        except AssertionError as e:
            self.logger.error(f"Assertion failed: {str(e)}")
            self.take_screenshot("assertion_failed")
            raise
    
    def assert_element_visible(self, locator):
        """
        Assert that element is visible
        
        Args:
            locator (tuple): Selenium locator tuple (By.XPATH, locator_string)
            
        Raises:
            AssertionError: If element not visible
        """
        try:
            element = self.driver.find_element(*locator)
            assert element.is_displayed(), f"Element {locator} is not visible"
            self.logger.info(f"Assertion passed: Element {locator} is visible")
        except AssertionError as e:
            self.logger.error(f"Assertion failed: {str(e)}")
            self.take_screenshot("element_not_visible")
            raise
    
    def assert_url_contains(self, url_text):
        """
        Assert that URL contains specific text
        
        Args:
            url_text (str): Text expected in URL
            
        Raises:
            AssertionError: If URL doesn't contain text
        """
        try:
            current_url = self.driver.current_url
            assert url_text in current_url, f"URL does not contain '{url_text}'. Current URL: {current_url}"
            self.logger.info(f"Assertion passed: URL contains '{url_text}'")
        except AssertionError as e:
            self.logger.error(f"Assertion failed: {str(e)}")
            self.take_screenshot("url_assertion_failed")
            raise
    
    def assert_page_title_contains(self, title_text):
        """
        Assert that page title contains specific text
        
        Args:
            title_text (str): Text expected in title
            
        Raises:
            AssertionError: If title doesn't contain text
        """
        try:
            page_title = self.driver.title
            assert title_text in page_title, f"Title does not contain '{title_text}'. Current title: {page_title}"
            self.logger.info(f"Assertion passed: Title contains '{title_text}'")
        except AssertionError as e:
            self.logger.error(f"Assertion failed: {str(e)}")
            self.take_screenshot("title_assertion_failed")
            raise
    
    # ==================== Helper Methods ====================
    
    def wait_for_loading_to_complete(self, timeout=10):
        """
        Wait for page loading spinners to disappear
        
        Args:
            timeout (int): Timeout in seconds
        """
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        try:
            # Wait for common loading spinners to disappear
            spinner_locators = [
                (By.CLASS_NAME, "spinner"),
                (By.CLASS_NAME, "loader"),
                (By.CLASS_NAME, "loading"),
                (By.ID, "loading"),
            ]
            
            wait = WebDriverWait(self.driver, timeout)
            for locator in spinner_locators:
                try:
                    wait.until(EC.invisibility_of_element_located(locator))
                except:
                    pass
            
            self.logger.info("Loading complete")
        except Exception as e:
            self.logger.warning(f"Error waiting for loading: {str(e)}")
    
    def switch_to_frame(self, locator):
        """
        Switch WebDriver focus to iframe
        
        Args:
            locator (tuple): Selenium locator tuple for iframe
        """
        try:
            frame_element = self.driver.find_element(*locator)
            self.driver.switch_to.frame(frame_element)
            self.logger.info(f"Switched to frame: {locator}")
        except Exception as e:
            self.logger.error(f"Error switching to frame: {str(e)}")
            raise
    
    def switch_to_default_content(self):
        """
        Switch WebDriver focus back to main content
        """
        try:
            self.driver.switch_to.default_content()
            self.logger.info("Switched to default content")
        except Exception as e:
            self.logger.error(f"Error switching to default content: {str(e)}")
            raise
    
    def close_browser_alert(self, action="accept"):
        """
        Handle JavaScript alert dialog
        
        Args:
            action (str): 'accept' to click OK, 'dismiss' to click Cancel
        """
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            
            if action.lower() == "accept":
                alert.accept()
                self.logger.info(f"Alert accepted: {alert_text}")
            elif action.lower() == "dismiss":
                alert.dismiss()
                self.logger.info(f"Alert dismissed: {alert_text}")
            else:
                raise ValueError(f"Invalid action: {action}")
                
        except Exception as e:
            self.logger.error(f"Error handling alert: {str(e)}")
            raise
