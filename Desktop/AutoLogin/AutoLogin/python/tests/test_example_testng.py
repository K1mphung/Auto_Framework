"""
Example test file demonstrating TestNG decorator usage in PyTest.

This file shows:
- Using @test_method decorator with various options
- Using @before_method and @after_method decorators
- Using @data_provider for parameterized tests
- Using @skip decorator
- Organizing tests with pytest markers
- Creating test dependencies
"""

import pytest
from base.base_test import BaseTest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.testng_decorators import (
    test_method,
    before_method,
    after_method,
    before_class,
    after_class,
    skip,
    data_provider,
    get_test_registry,
    get_tests_by_group
)


class TestLogsTestNG(BaseTest):
    """
    Demonstrates TestNG decorator patterns with PyTest.
    
    This test class shows best practices for:
    - Test organization with decorators
    - Setup/teardown with decorators
    - Parameterized tests
    - Test grouping
    - Priority and dependencies
    """
    
    # ==================== CLASS SETUP/TEARDOWN ====================
    
    @before_class()
    def setup_class_testng(self):
        """
        Runs once before all tests in this class.
        
        TestNG equivalent: @BeforeClass
        PyTest equivalent: setup_class (but with decorator pattern)
        """
        print("\n" + "="*60)
        print("SETUP CLASS: TestNGExamples")
        print("="*60)
        self.test_data = {
            'valid_user': 'user@example.com',
            'valid_password': 'password123'
        }
    
    @after_class()
    def cleanup_class_testng(self):
        """
        Runs once after all tests in this class complete.
        
        TestNG equivalent: @AfterClass
        PyTest equivalent: teardown_class (but with decorator pattern)
        """
        print("\n" + "="*60)
        print("CLEANUP CLASS: TestNGExamples")
        print("="*60)
        print("All tests completed")
    
    # ==================== TEST METHOD EXAMPLES ====================
    
    @test_method(
        name="successful_login_testng",
        description="Demonstrate successful login with TestNG decorator",
        priority=1,
        groups=["smoke", "login", "priority1"],
        enabled=True,
        timeout=10000
    )
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.priority1
    @before_method()
    def test_successful_login_with_decorator(self):
        """
        Example: Basic test decorated with @test_method.
        
        Features:
        - Uses @test_method with metadata (name, description, priority)
        - Groups: smoke, login, priority1 (can run: pytest -m smoke)
        - Enabled: true (test will run)
        - Timeout: 10 seconds
        - Priority: 1 (high priority)
        
        TestNG equivalent:
        @Test(
            testName = "successful_login_testng",
            description = "...",
            priority = 1,
            groups = {"smoke", "login", "priority1"},
            enabled = true,
            timeOut = 10000
        )
        public void testSuccessfulLogin() { }
        """
        # Test implementation
        self.navigate_to_app()
        login_page = LoginPage(self.driver)
        login_page.login(self.test_data['valid_user'], 
                        self.test_data['valid_password'])
        
        # Assertion
        self.assert_url_contains("dashboard")
        assert login_page.is_login_successful()
    
    @test_method(
        name="login_with_invalid_username",
        description="Test login fails with invalid username",
        priority=2,
        groups=["regression", "login"],
        enabled=True
    )
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.priority2
    def test_login_invalid_username(self):
        """
        Example: Test with lower priority and regression group.
        
        Features:
        - Priority: 2 (medium priority)
        - Groups: regression, login
        - No timeout specified (uses default)
        
        TestNG equivalent:
        @Test(priority = 2, groups = {"regression", "login"})
        """
        self.navigate_to_app()
        login_page = LoginPage(self.driver)
        login_page.login("invalid_user@example.com", 
                        self.test_data['valid_password'])
        
        # Should see error message
        assert login_page.is_error_message_displayed()
    
    @test_method(
        name="login_with_invalid_password",
        description="Test login fails with invalid password",
        priority=2,
        groups=["regression", "login"]
    )
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.priority2
    def test_login_invalid_password(self):
        """
        Example: Another regression test.
        """
        self.navigate_to_app()
        login_page = LoginPage(self.driver)
        login_page.login(self.test_data['valid_user'], 
                        "wrong_password")
        
        assert login_page.is_error_message_displayed()
    
    # ==================== PARAMETERIZED TEST EXAMPLE ====================
    
    @test_method(
        name="login_with_multiple_users",
        description="Test login with multiple user data sets",
        priority=3,
        groups=["functional", "login"]
    )
    @pytest.mark.functional
    @pytest.mark.login
    @pytest.mark.priority3
    @data_provider([
        ["admin@example.com", "admin123"],
        ["user1@example.com", "pass123"],
        ["user2@example.com", "pass456"],
        ["manager@example.com", "mgr789"]
    ])
    def test_login_multiple_users(self, username, password):
        """
        Example: Parameterized test using @data_provider.
        
        Features:
        - @data_provider passes multiple data sets
        - Test runs once per data set
        - Each iteration tests different username/password
        
        TestNG equivalent:
        @DataProvider(name = "loginData")
        public Object[][] getLoginData() {
            return new Object[][] {
                {"admin@example.com", "admin123"},
                {"user1@example.com", "pass123"}
            };
        }
        
        @Test(dataProvider = "loginData")
        public void testLoginMultipleUsers(String username, String password) { }
        """
        self.navigate_to_app()
        login_page = LoginPage(self.driver)
        login_page.login(username, password)
        
        # After successful login, user should be on dashboard
        self.assert_url_contains("dashboard")
    
    # ==================== SKIPPED TEST EXAMPLE ====================
    
    @skip(reason="Feature not yet implemented - waiting for backend API")
    @test_method(
        name="biometric_login",
        description="Test biometric login functionality",
        priority=1,
        groups=["smoke"]
    )
    @pytest.mark.skip(reason="Feature not yet implemented")
    def test_biometric_login(self):
        """
        Example: Skipped test with @skip decorator.
        
        Features:
        - @skip marks test to be skipped
        - reason parameter explains why
        - Test won't execute or count as failure
        
        TestNG equivalent:
        @Test(skip = true)
        public void testBiometricLogin() { }
        """
        # This won't run
        pass
    
    # ==================== UI COMPONENT TEST ====================
    
    @test_method(
        name="verify_login_page_elements",
        description="Verify all login page elements are visible",
        priority=2,
        groups=["ui", "smoke"]
    )
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.priority2
    def test_login_page_elements_visible(self):
        """
        Example: UI test checking element visibility.
        """
        self.navigate_to_app()
        login_page = LoginPage(self.driver)
        
        # Verify all UI elements are displayed
        assert login_page.is_username_field_visible()
        assert login_page.is_password_field_visible()
        assert login_page.is_login_button_visible()
        assert login_page.is_remember_me_checkbox_visible()
    
    # ==================== INTEGRATION TEST ====================
    
    @test_method(
        name="full_login_and_logout_flow",
        description="Test complete login and logout flow",
        priority=1,
        groups=["integration", "critical"]
    )
    @pytest.mark.integration
    @pytest.mark.critical
    @pytest.mark.priority1
    def test_full_login_logout_flow(self):
        """
        Example: Integration test with multiple steps.
        """
        # Login
        self.navigate_to_app()
        login_page = LoginPage(self.driver)
        login_page.login(self.test_data['valid_user'], 
                        self.test_data['valid_password'])
        
        # Verify dashboard
        dashboard = DashboardPage(self.driver)
        assert dashboard.is_dashboard_loaded()
        
        # Logout
        dashboard.logout()
        
        # Verify back at login page
        assert login_page.is_login_page_displayed()


# ==================== HELPER TEST CLASS ====================

class TestNGDecoratorShowcase(BaseTest):
    """
    Additional examples showing decorator combinations.
    """
    
    @before_method()
    def setup_each_test(self):
        """
        Runs before each test method.
        
        TestNG equivalent: @BeforeMethod
        """
        print("\n" + "-"*40)
        print("SETUP TEST METHOD")
        print("-"*40)
        self.login_page = LoginPage(self.driver)
    
    @after_method(alwaysRun=True)
    def cleanup_each_test(self):
        """
        Runs after each test method, even if test fails.
        
        Features:
        - alwaysRun=True: Runs regardless of test result
        - Good for cleanup that must happen (e.g., logout, close resources)
        
        TestNG equivalent:
        @AfterMethod(alwaysRun = true)
        """
        print("\n" + "-"*40)
        print("CLEANUP TEST METHOD")
        print("-"*40)
        # Could take screenshot here on failure
        # Could logout here
        # Could close resources
    
    @test_method(
        name="dependent_test",
        description="Test that depends on another test",
        depends_on_methods=["test_successful_login_testng"],
        priority=2,
        groups=["integration"]
    )
    @pytest.mark.integration
    def test_depends_on_login(self):
        """
        Example: Test with dependency on another test.
        
        Features:
        - depends_on_methods: Only runs if dependent tests pass
        - In PyTest, this is noted but not enforced (by design)
        - Useful as metadata for reporting
        
        TestNG equivalent:
        @Test(dependsOnMethods = {"testSuccessfulLogin"})
        """
        # This conceptually depends on successful login
        dashboard = DashboardPage(self.driver)
        assert dashboard.is_dashboard_loaded()
    
    @test_method(
        name="performance_test",
        description="Performance test for login",
        priority=3,
        groups=["performance"],
        timeout=5000
    )
    @pytest.mark.performance
    def test_login_performance(self):
        """
        Example: Performance test with timeout.
        """
        import time
        start = time.time()
        
        login_page = LoginPage(self.driver)
        login_page.login("user@example.com", "password")
        
        elapsed = time.time() - start
        
        # Assert login completes within 5 seconds
        assert elapsed < 5, f"Login took {elapsed}s, expected < 5s"


# ==================== UTILITY EXAMPLES ====================

class TestNGUtilityExamples(BaseTest):
    """
    Examples of using TestNG utility functions.
    """
    
    def test_get_test_registry(self):
        """
        Example: Accessing test registry to view test metadata.
        """
        # Get all registered tests
        all_tests = get_test_registry()
        
        print("\n" + "="*60)
        print("ALL REGISTERED TESTS:")
        print("="*60)
        for test_name, test_info in all_tests.items():
            print(f"\nTest: {test_name}")
            print(f"  Description: {test_info.get('description', 'N/A')}")
            print(f"  Priority: {test_info.get('priority', 'N/A')}")
            print(f"  Groups: {test_info.get('groups', [])}")
    
    def test_get_tests_by_group(self):
        """
        Example: Getting tests by group.
        """
        # Get all smoke tests
        smoke_tests = get_tests_by_group('smoke')
        
        print("\n" + "="*60)
        print(f"SMOKE TESTS ({len(smoke_tests)}):")
        print("="*60)
        for test_name, test_info in smoke_tests.items():
            print(f"  - {test_name}: {test_info.get('description', 'N/A')}")


# ==================== RUNNING THESE TESTS ====================

"""
COMMAND EXAMPLES:

1. Run all tests in this file:
   pytest tests/test_example_testng.py -v

2. Run only smoke tests:
   pytest tests/test_example_testng.py -m smoke -v

3. Run only login tests:
   pytest tests/test_example_testng.py -m login -v

4. Run parameterized test (test_login_multiple_users):
   pytest tests/test_example_testng.py::TestLogsTestNG::test_login_multiple_users -v

5. Run tests by priority:
   pytest tests/test_example_testng.py -m priority1 -v

6. Run integration tests:
   pytest tests/test_example_testng.py -m integration -v

7. Run high-priority integration tests:
   pytest tests/test_example_testng.py -m "integration and priority1" -v

8. Run all except skipped:
   pytest tests/test_example_testng.py -v

9. Using TestNG Suite Runner:
   python -m utilities.testng_suite_runner run "Smoke Tests"

10. Run in parallel:
    pytest tests/test_example_testng.py -n auto -v
"""
