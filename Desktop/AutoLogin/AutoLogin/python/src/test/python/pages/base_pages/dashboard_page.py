"""
DashboardPage Module
Page Object for dashboard functionality - Facade combining locators and actions
Example page showing complete structure
"""

from pages.actions.dashboard_actions import DashboardActions
from pages.locators.dashboard_locators import DashboardLocators


class DashboardPage(DashboardActions):
    """
    Dashboard page object combining DashboardActions and DashboardLocators.
    Provides unified interface for dashboard interactions.
    
    This is an example page showing how to structure new page objects
    using the Locators + Actions pattern.
    
    Inherits from DashboardActions which inherits from BaseActions.
    Follows Page Object Model pattern with separated locators and actions.
    """
    
    def __init__(self, driver):
        """Initialize DashboardPage with WebDriver instance"""
        super().__init__(driver)
        # Make locators accessible as class attributes for backward compatibility
        self.locators = DashboardLocators()
