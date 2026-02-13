"""
LoginPage Module
Page Object for login functionality - Facade combining locators and actions
"""

from pages.actions.login_actions import LoginActions
from pages.locators.login_locators import LoginLocators


class LoginPage(LoginActions):
    """
    Login page object combining LoginActions and LoginLocators.
    Provides unified interface for login page interactions.
    
    Inherits from LoginActions which inherits from BasePage.
    Follows Page Object Model pattern with separated locators and actions.
    """
    
    def __init__(self, driver):
        """Initialize LoginPage with WebDriver instance"""
        super().__init__(driver)
        # Make locators accessible as class attributes for backward compatibility
        self.locators = LoginLocators()
