"""
Base Actions Module
Abstract base class for page actions
Provides structure for creating action classes for other pages
"""

from pages.base_page import BasePage


class BaseActions(BasePage):
    """
    Abstract base class for page-specific actions.
    All page action classes should inherit from this.
    
    This class extends BasePage with additional page-specific functionality.
    
    Benefits:
    - Unified action interface across all page objects
    - Separation of concerns (locators, actions, tests)
    - Easy to maintain and extend
    - Reusable action patterns
    
    Usage:
        class YourPageActions(BaseActions):
            def __init__(self, driver):
                super().__init__(driver)
                self.locators = YourPageLocators()
            
            def your_action(self):
                # Use self.locators to access page elements
                self.click_element(self.locators.BUTTON)
    """
    
    def __init__(self, driver):
        """Initialize BaseActions with WebDriver instance"""
        super().__init__(driver)
        self.locators = None  # Will be set by subclasses
    
    def set_locators(self, locators):
        """
        Set locators for this page
        
        Args:
            locators: Locators class instance
        """
        self.locators = locators
        self.logger.debug(f"Locators set: {locators.__class__.__name__}")
    
    def get_page_name(self):
        """
        Get the name of this page
        
        Returns:
            str: Page name (class name)
        """
        return self.__class__.__name__
