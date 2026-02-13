"""
LoginPage Actions Module
Page-specific actions for login functionality
"""

from pages.actions.base_actions import BaseActions
from pages.locators.login_locators import LoginLocators


class LoginActions(BaseActions):
    """
    Login page actions encapsulating all login-related interactions.
    Uses locators from LoginLocators class.
    Follows Page Object Model pattern for maintainability.
    """
    
    def __init__(self, driver):
        """Initialize LoginActions with WebDriver instance"""
        super().__init__(driver)
        self.locators = LoginLocators()
    
    # ==================== Verification Methods ====================
    
    def is_login_page_displayed(self):
        """
        Verify that login page is properly loaded
        
        Returns:
            bool: True if login page elements are visible
        """
        try:
            is_displayed = self.is_element_displayed(self.locators.PAGE_TITLE) and \
                          self.is_element_displayed(self.locators.USERNAME_INPUT) and \
                          self.is_element_displayed(self.locators.PASSWORD_INPUT)
            
            if is_displayed:
                self.logger.info("Login page is displayed")
            else:
                self.logger.warning("Login page components not displayed")
            
            return is_displayed
        except Exception as e:
            self.logger.error(f"Error checking login page: {str(e)}")
            return False
    
    # ==================== Input Actions ====================
    
    def enter_username(self, username):
        """
        Enter username/email in the username field
        
        Args:
            username (str): Username or email address
        """
        try:
            self.send_keys(self.locators.USERNAME_INPUT, username)
            self.logger.info(f"Entered username: {username}")
        except Exception as e:
            self.logger.error(f"Error entering username: {str(e)}")
            raise
    
    def enter_password(self, password):
        """
        Enter password in the password field
        
        Args:
            password (str): User password
        """
        try:
            self.send_keys(self.locators.PASSWORD_INPUT, password)
            self.logger.info("Password entered")  # Don't log actual password
        except Exception as e:
            self.logger.error(f"Error entering password: {str(e)}")
            raise
    
    def clear_username(self):
        """Clear username field"""
        try:
            element = self.wait_helper.wait_for_element_visible(self.locators.USERNAME_INPUT)
            element.clear()
            self.logger.info("Username field cleared")
        except Exception as e:
            self.logger.error(f"Error clearing username: {str(e)}")
            raise
    
    def clear_password(self):
        """Clear password field"""
        try:
            element = self.wait_helper.wait_for_element_visible(self.locators.PASSWORD_INPUT)
            element.clear()
            self.logger.info("Password field cleared")
        except Exception as e:
            self.logger.error(f"Error clearing password: {str(e)}")
            raise
    
    # ==================== Button & Link Click Actions ====================
    
    def click_login_button(self):
        """
        Click the login button to submit credentials
        """
        try:
            self.click_element(self.locators.LOGIN_BUTTON)
            self.logger.info("Login button clicked")
        except Exception as e:
            self.logger.error(f"Error clicking login button: {str(e)}")
            raise
    
    def click_forgot_password(self):
        """
        Click on 'Forgot Password' link
        """
        try:
            self.click_element(self.locators.FORGOT_PASSWORD_LINK)
            self.logger.info("Clicked 'Forgot Password' link")
        except Exception as e:
            self.logger.error(f"Error clicking 'Forgot Password': {str(e)}")
            raise
    
    def click_signup_link(self):
        """
        Click on 'Sign Up' link
        """
        try:
            self.click_element(self.locators.SIGNUP_LINK)
            self.logger.info("Clicked 'Sign Up' link")
        except Exception as e:
            self.logger.error(f"Error clicking 'Sign Up': {str(e)}")
            raise
    
    # ==================== Checkbox Actions ====================
    
    def check_remember_me(self):
        """
        Check the 'Remember Me' checkbox
        """
        try:
            if not self.is_remember_me_checked():
                self.click_element(self.locators.REMEMBER_ME_CHECKBOX)
                self.logger.info("'Remember Me' checkbox checked")
        except Exception as e:
            self.logger.error(f"Error checking 'Remember Me': {str(e)}")
            raise
    
    def uncheck_remember_me(self):
        """
        Uncheck the 'Remember Me' checkbox
        """
        try:
            if self.is_remember_me_checked():
                self.click_element(self.locators.REMEMBER_ME_CHECKBOX)
                self.logger.info("'Remember Me' checkbox unchecked")
        except Exception as e:
            self.logger.error(f"Error unchecking 'Remember Me': {str(e)}")
            raise
    
    # ==================== Composite Actions ====================
    
    def login(self, username, password, remember_me=False):
        """
        Complete login process with username and password
        
        Args:
            username (str): Username or email
            password (str): User password
            remember_me (bool): Whether to check 'Remember Me' checkbox
        """
        try:
            self.logger.info("Starting login process")
            
            # Verify page is loaded
            if not self.is_login_page_displayed():
                raise Exception("Login page not properly loaded")
            
            # Enter credentials
            self.enter_username(username)
            self.enter_password(password)
            
            # Check remember me if required
            if remember_me:
                self.check_remember_me()
            
            # Click login button
            self.click_login_button()
            
            self.logger.info("Login process completed")
            
        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            raise
    
    def login_and_verify_error(self, username, password):
        """
        Login and expect error message
        
        Args:
            username (str): Username or email
            password (str): User password
            
        Returns:
            str: Error message text
        """
        try:
            self.login(username, password)
            self.wait_for_loading_to_complete()
            
            if self.is_error_message_displayed():
                error_msg = self.get_error_message()
                self.logger.info(f"Error message received: {error_msg}")
                return error_msg
            else:
                raise Exception("Expected error message not displayed")
                
        except Exception as e:
            self.logger.error(f"Error in login_and_verify_error: {str(e)}")
            raise
    
    # ==================== Message Retrieval ====================
    
    def get_error_message(self):
        """
        Get error message text displayed on login page
        
        Returns:
            str: Error message text
        """
        try:
            error_text = self.get_element_text(self.locators.ERROR_MESSAGE)
            self.logger.warning(f"Error message displayed: {error_text}")
            return error_text
        except Exception as e:
            self.logger.debug(f"No error message found: {str(e)}")
            return None
    
    def get_success_message(self):
        """
        Get success message text displayed on login page
        
        Returns:
            str: Success message text
        """
        try:
            success_text = self.get_element_text(self.locators.SUCCESS_MESSAGE)
            self.logger.info(f"Success message displayed: {success_text}")
            return success_text
        except Exception as e:
            self.logger.debug(f"No success message found: {str(e)}")
            return None
    
    # ==================== State Check Methods ====================
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error message is visible
        """
        try:
            is_displayed = self.is_element_displayed(self.locators.ERROR_MESSAGE)
            return is_displayed
        except Exception as e:
            self.logger.debug(f"Error checking error message: {str(e)}")
            return False
    
    def is_success_message_displayed(self):
        """
        Check if success message is displayed
        
        Returns:
            bool: True if success message is visible
        """
        try:
            is_displayed = self.is_element_displayed(self.locators.SUCCESS_MESSAGE)
            return is_displayed
        except Exception as e:
            self.logger.debug(f"Error checking success message: {str(e)}")
            return False
    
    def is_remember_me_checked(self):
        """
        Check if 'Remember Me' checkbox is selected
        
        Returns:
            bool: True if checkbox is checked
        """
        try:
            is_checked = self.is_element_selected(self.locators.REMEMBER_ME_CHECKBOX)
            return is_checked
        except Exception as e:
            self.logger.debug(f"Error checking 'Remember Me': {str(e)}")
            return False
    
    # ==================== Attribute Retrieval ====================
    
    def get_username_placeholder(self):
        """
        Get placeholder text from username field
        
        Returns:
            str: Placeholder text
        """
        try:
            placeholder = self.get_element_attribute(self.locators.USERNAME_INPUT, "placeholder")
            return placeholder
        except Exception as e:
            self.logger.debug(f"Error getting username placeholder: {str(e)}")
            return None
    
    def get_password_placeholder(self):
        """
        Get placeholder text from password field
        
        Returns:
            str: Placeholder text
        """
        try:
            placeholder = self.get_element_attribute(self.locators.PASSWORD_INPUT, "placeholder")
            return placeholder
        except Exception as e:
            self.logger.debug(f"Error getting password placeholder: {str(e)}")
            return None
    
    def is_login_button_enabled(self):
        """
        Check if login button is enabled
        
        Returns:
            bool: True if button is enabled
        """
        try:
            is_enabled = self.is_element_enabled(self.locators.LOGIN_BUTTON)
            return is_enabled
        except Exception as e:
            self.logger.debug(f"Error checking login button enabled state: {str(e)}")
            return False
