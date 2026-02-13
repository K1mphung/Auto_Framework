"""
LoginPage Locators Module
Centralized locators for login page elements
"""

from selenium.webdriver.common.by import By
from pages.locators.base_locators import BaseLocators


class LoginLocators(BaseLocators):
    """
    Centralized locators for login page.
    All element locators are defined here for easy maintenance.
    Uses Page Object Model best practice pattern.
    """
    
    # ==================== Input Fields ====================
    # Username/Email input field
    USERNAME_INPUT = (By.ID, "username")
    
    # Password input field
    PASSWORD_INPUT = (By.ID, "password")
    
    # ==================== Buttons ====================
    # Login button
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    
    # ==================== Checkboxes ====================
    # Remember me checkbox
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberMe")
    
    # ==================== Links ====================
    # Forgot password link
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    
    # Sign up link
    SIGNUP_LINK = (By.LINK_TEXT, "Sign Up")
    
    # ==================== Messages & Display Elements ====================
    # Error message display
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    # Success message display
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    
    # Page title/heading
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(), 'Login')]")
