"""
DashboardPage Locators Module
Centralized locators for dashboard page elements
Example page demonstrating the locators structure
"""

from selenium.webdriver.common.by import By
from pages.locators.base_locators import BaseLocators


class DashboardLocators(BaseLocators):
    """
    Locators for dashboard page.
    This is an example showing how to structure locators for other pages.
    """
    
    # ==================== Header Elements ====================
    # User profile button
    USER_PROFILE_BUTTON = (By.ID, "user-profile")
    
    # Logout button
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Logout')]")
    
    # Welcome message
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome-text")
    
    # ==================== Navigation ====================
    # Sidebar menu
    SIDEBAR_MENU = (By.ID, "sidebar-menu")
    
    # Dashboard link
    DASHBOARD_LINK = (By.LINK_TEXT, "Dashboard")
    
    # Settings link
    SETTINGS_LINK = (By.LINK_TEXT, "Settings")
    
    # ==================== Content Area ====================
    # Main content area
    MAIN_CONTENT = (By.ID, "main-content")
    
    # Data table
    DATA_TABLE = (By.ID, "data-table")
    
    # ==================== Notifications ====================
    # Notification bell
    NOTIFICATION_BELL = (By.CLASS_NAME, "notification-bell")
    
    # Notification badge
    NOTIFICATION_BADGE = (By.CLASS_NAME, "notification-badge")
