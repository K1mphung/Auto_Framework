"""
Login Test Cases
Test suite for login functionality using Page Object Model
Uses TestNG-style annotations for test organization
"""

import pytest
from base.base_test import BaseTest
from pages.base_pages.login_page import LoginPage
from pages.locators.login_locators import LoginLocators
from utilities.testng_decorators import (
    test_method,
    before_method,
    after_method,
    skip
)


class TestLogin(BaseTest):
    """
    Test class for login functionality
    Inherits from BaseTest for automatic setup/teardown and utilities
    """
    
    @pytest.fixture(autouse=True)
    def setup_login_tests(self):
        """
        Setup specific to login tests
        Initialize page objects required for tests
        """
        self.login_page = LoginPage(self.driver)
        self.locators = LoginLocators()
        yield
    
    # ==================== Test Cases ====================
    
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.priority1
    def test_successful_login(self):
        """
        Test Case: TC_LOGIN_001 - Successful Login
        
        Preconditions:
            - User is on login page
            - Valid credentials are available
            
        Test Steps:
            1. Navigate to login page
            2. Enter valid username
            3. Enter valid password
            4. Click login button
            
        Expected Result:
            - Login should be successful
            - User should be redirected to dashboard
        """
        try:
            # Arrange
            username = "testuser@example.com"
            password = "TestPassword123!"
            
            # Act
            self.navigate_to_app()
            assert self.login_page.is_login_page_displayed(), \
                "Login page is not displayed"
            
            self.login_page.login(username, password)
            
            # Assert
            self.wait_for_loading_to_complete()
            self.assert_url_contains("dashboard")
            
            self.logger.info("✓ Test passed: Successful login")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_successful_login_failed")
            raise
        except Exception as e:
            self.logger.error(f"✗ Test error: {str(e)}")
            self.take_screenshot("test_successful_login_error")
            raise
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_invalid_username(self):
        """
        Test Case: TC_LOGIN_002 - Login with Invalid Username
        
        Preconditions:
            - User is on login page
            
        Test Steps:
            1. Navigate to login page
            2. Enter invalid username
            3. Enter valid password
            4. Click login button
            
        Expected Result:
            - Login should fail
            - Error message should be displayed
        """
        try:
            # Arrange
            invalid_username = "invaliduser@example.com"
            password = "TestPassword123!"
            
            # Act
            self.navigate_to_app()
            assert self.login_page.is_login_page_displayed(), \
                "Login page is not displayed"
            
            self.login_page.login(invalid_username, password)
            
            # Assert
            self.wait_for_loading_to_complete()
            assert self.login_page.is_error_message_displayed(), \
                "Error message is not displayed"
            
            error_msg = self.login_page.get_error_message()
            assert "invalid" in error_msg.lower() or "failed" in error_msg.lower(), \
                f"Unexpected error message: {error_msg}"
            
            self.logger.info("✓ Test passed: Invalid username handled correctly")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_invalid_username_failed")
            raise
        except Exception as e:
            self.logger.error(f"✗ Test error: {str(e)}")
            self.take_screenshot("test_invalid_username_error")
            raise
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_invalid_password(self):
        """
        Test Case: TC_LOGIN_003 - Login with Invalid Password
        
        Preconditions:
            - User is on login page
            
        Test Steps:
            1. Navigate to login page
            2. Enter valid username
            3. Enter invalid password
            4. Click login button
            
        Expected Result:
            - Login should fail
            - Error message should be displayed
        """
        try:
            # Arrange
            username = "testuser@example.com"
            invalid_password = "WrongPassword123!"
            
            # Act
            self.navigate_to_app()
            assert self.login_page.is_login_page_displayed(), \
                "Login page is not displayed"
            
            self.login_page.login(username, invalid_password)
            
            # Assert
            self.wait_for_loading_to_complete()
            assert self.login_page.is_error_message_displayed(), \
                "Error message is not displayed"
            
            error_msg = self.login_page.get_error_message()
            assert "invalid" in error_msg.lower() or "failed" in error_msg.lower(), \
                f"Unexpected error message: {error_msg}"
            
            self.logger.info("✓ Test passed: Invalid password handled correctly")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_invalid_password_failed")
            raise
        except Exception as e:
            self.logger.error(f"✗ Test error: {str(e)}")
            self.take_screenshot("test_invalid_password_error")
            raise
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_empty_credentials(self):
        """
        Test Case: TC_LOGIN_004 - Login with Empty Credentials
        
        Preconditions:
            - User is on login page
            
        Test Steps:
            1. Navigate to login page
            2. Leave username empty
            3. Leave password empty
            4. Click login button
            
        Expected Result:
            - Login should fail
            - Validation message should be displayed
        """
        try:
            # Arrange
            username = ""
            password = ""
            
            # Act
            self.navigate_to_app()
            assert self.login_page.is_login_page_displayed(), \
                "Login page is not displayed"
            
            self.login_page.login(username, password)
            
            # Assert
            self.wait_for_loading_to_complete()
            # Check for validation or error message
            assert self.login_page.is_error_message_displayed() or \
                   self.login_page.is_login_page_displayed(), \
                "Expected error or validation message"
            
            self.logger.info("✓ Test passed: Empty credentials handled correctly")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_empty_credentials_failed")
            raise
        except Exception as e:
            self.logger.error(f"✗ Test error: {str(e)}")
            self.take_screenshot("test_empty_credentials_error")
            raise
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_login_page_elements(self):
        """
        Test Case: TC_LOGIN_005 - Verify Login Page Elements
        
        Preconditions:
            - User is on login page
            
        Test Steps:
            1. Navigate to login page
            2. Verify all required elements are present and visible
            
        Expected Result:
            - All login page elements should be visible and functional
        """
        try:
            # Act
            self.navigate_to_app()
            
            # Assert
            assert self.login_page.is_login_page_displayed(), \
                "Login page is not displayed"
            
            assert self.login_page.is_element_displayed(self.locators.USERNAME_INPUT), \
                "Username input field is not visible"
            
            assert self.login_page.is_element_displayed(self.locators.PASSWORD_INPUT), \
                "Password input field is not visible"
            
            assert self.login_page.is_element_displayed(self.locators.LOGIN_BUTTON), \
                "Login button is not visible"
            
            assert self.login_page.is_element_displayed(self.locators.FORGOT_PASSWORD_LINK), \
                "Forgot Password link is not visible"
            
            assert self.login_page.is_element_displayed(self.locators.SIGNUP_LINK), \
                "Sign Up link is not visible"
            
            self.logger.info("✓ Test passed: All login page elements are visible")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_login_elements_failed")
            raise
        except Exception as e:
            self.logger.error(f"✗ Test error: {str(e)}")
            self.take_screenshot("test_login_elements_error")
            raise
    
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_remember_me(self):
        """
        Test Case: TC_LOGIN_006 - Login with Remember Me Checked
        
        Preconditions:
            - User is on login page
            
        Test Steps:
            1. Navigate to login page
            2. Enter valid username and password
            3. Check 'Remember Me' checkbox
            4. Click login button
            
        Expected Result:
            - Login should be successful
            - Remember Me preference should be saved
        """
        try:
            # Arrange
            username = "testuser@example.com"
            password = "TestPassword123!"
            
            # Act
            self.navigate_to_app()
            assert self.login_page.is_login_page_displayed(), \
                "Login page is not displayed"
            
            self.login_page.login(username, password, remember_me=True)
            
            # Assert
            self.wait_for_loading_to_complete()
            assert self.login_page.is_remember_me_checked(), \
                "Remember Me checkbox is not checked"
            
            self.assert_url_contains("dashboard")
            
            self.logger.info("✓ Test passed: Login with Remember Me successful")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_remember_me_failed")
            raise
        except Exception as e:
            self.logger.error(f"✗ Test error: {str(e)}")
            self.take_screenshot("test_remember_me_error")
            raise


class TestLoginPageValidation(BaseTest):
    """
    Test class for login page validation and UI tests
    """
    
    @pytest.fixture(autouse=True)
    def setup_validation_tests(self):
        """Setup for validation tests"""
        self.login_page = LoginPage(self.driver)
        yield
    
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_username_field_placeholder(self):
        """
        Test Case: TC_LOGIN_007 - Verify Username Field Placeholder
        
        Expected Result:
            - Username field should have proper placeholder text
        """
        try:
            self.navigate_to_app()
            
            placeholder = self.login_page.get_username_placeholder()
            assert placeholder is not None, "Username placeholder is missing"
            assert len(placeholder) > 0, "Username placeholder is empty"
            
            self.logger.info(f"✓ Test passed: Username placeholder: {placeholder}")
            
        except AssertionError as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            self.take_screenshot("test_username_placeholder_failed")
            raise
