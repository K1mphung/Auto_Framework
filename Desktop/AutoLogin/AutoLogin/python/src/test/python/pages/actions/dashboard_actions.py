"""
DashboardPage Actions Module
Page-specific actions for dashboard functionality
Example page demonstrating the actions structure
"""

from pages.actions.base_actions import BaseActions
from pages.locators.dashboard_locators import DashboardLocators


class DashboardActions(BaseActions):
    """
    Dashboard page actions encapsulating all dashboard-related interactions.
    This is an example showing how to structure actions for other pages.
    Inherits from BaseActions which inherits from BasePage.
    """
    
    def __init__(self, driver):
        """Initialize DashboardActions with WebDriver instance"""
        super().__init__(driver)
        self.locators = DashboardLocators()
    
    # ==================== Verification Methods ====================
    
    def is_dashboard_displayed(self):
        """
        Verify that dashboard is properly loaded
        
        Returns:
            bool: True if dashboard elements are visible
        """
        try:
            is_displayed = self.is_element_displayed(self.locators.MAIN_CONTENT) and \
                          self.is_element_displayed(self.locators.WELCOME_MESSAGE)
            
            if is_displayed:
                self.logger.info("Dashboard is displayed")
            else:
                self.logger.warning("Dashboard not fully loaded")
            
            return is_displayed
        except Exception as e:
            self.logger.error(f"Error checking dashboard: {str(e)}")
            return False
    
    # ==================== User Actions ====================
    
    def click_user_profile(self):
        """Click on user profile button"""
        try:
            self.click_element(self.locators.USER_PROFILE_BUTTON)
            self.logger.info("Clicked user profile button")
        except Exception as e:
            self.logger.error(f"Error clicking user profile: {str(e)}")
            raise
    
    def logout(self):
        """Logout from dashboard"""
        try:
            self.click_element(self.locators.LOGOUT_BUTTON)
            self.logger.info("Clicked logout button")
        except Exception as e:
            self.logger.error(f"Error logging out: {str(e)}")
            raise
    
    # ==================== Information Retrieval ====================
    
    def get_welcome_message(self):
        """
        Get welcome message from dashboard
        
        Returns:
            str: Welcome message text
        """
        try:
            message = self.get_element_text(self.locators.WELCOME_MESSAGE)
            self.logger.info(f"Welcome message: {message}")
            return message
        except Exception as e:
            self.logger.error(f"Error getting welcome message: {str(e)}")
            return None
    
    # ==================== Navigation ====================
    
    def click_settings(self):
        """Click on settings link"""
        try:
            self.click_element(self.locators.SETTINGS_LINK)
            self.logger.info("Clicked settings link")
        except Exception as e:
            self.logger.error(f"Error clicking settings: {str(e)}")
            raise
    
    def get_notification_count(self):
        """
        Get number of notifications from badge
        
        Returns:
            int: Number of notifications or 0 if not found
        """
        try:
            badge_text = self.get_element_text(self.locators.NOTIFICATION_BADGE)
            count = int(badge_text) if badge_text else 0
            return count
        except Exception as e:
            self.logger.debug(f"Error getting notification count: {str(e)}")
            return 0
