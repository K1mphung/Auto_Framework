# Page Object Structure Guide

## Overview

The framework now uses a **Locators + Actions Pattern** for better separation of concerns and maintainability.

## New Directory Structure

```
pages/
├── base_page.py                         # Base page with common methods
├── locators/
│   ├── __init__.py
│   ├── base_locators.py                 # Abstract base for locators
│   ├── login_locators.py                # Login page locators
│   └── dashboard_locators.py            # Dashboard page locators (example)
├── actions/
│   ├── __init__.py
│   ├── base_actions.py                  # Abstract base for actions
│   ├── login_actions.py                 # Login page actions
│   └── dashboard_actions.py             # Dashboard page actions (example)
├── login_page.py                         # Login page facade
└── dashboard_page.py                     # Dashboard page facade (example)
```

## How It Works

### 1. Locators (Element Selectors)

**File**: `pages/locators/login_locators.py`

Contains only element locators - no interaction logic.

```python
from selenium.webdriver.common.by import By
from pages.locators.base_locators import BaseLocators

class LoginLocators(BaseLocators):
    """Centralized locators for login page"""
    
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
```

### 2. Actions (User Interactions)

**File**: `pages/actions/login_actions.py`

Contains page-specific actions and interactions.

```python
from pages.actions.base_actions import BaseActions
from pages.locators.login_locators import LoginLocators

class LoginActions(BaseActions):
    """Login page user actions"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginLocators()
    
    def enter_username(self, username):
        """Enter username in the field"""
        self.send_keys(self.locators.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password in the field"""
        self.send_keys(self.locators.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click_element(self.locators.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
```

### 3. Page Facade (Unified Interface)

**File**: `pages/login_page.py`

Combines actions and locators for testing.

```python
from pages.actions.login_actions import LoginActions
from pages.locators.login_locators import LoginLocators

class LoginPage(LoginActions):
    """Login page facade combining actions and locators"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginLocators()
```

### 4. Test Cases

**File**: `tests/test_login.py`

Uses page facade for interactions and locators for assertions.

```python
from pages.login_page import LoginPage
from pages.locators.login_locators import LoginLocators

class TestLogin(BaseTest):
    
    def setup_login_tests(self):
        self.login_page = LoginPage(self.driver)
        self.locators = LoginLocators()
    
    def test_successful_login(self):
        # Use actions
        self.login_page.login("user@example.com", "password")
        
        # Use locators for assertions
        assert self.login_page.is_element_displayed(self.locators.ERROR_MESSAGE)
```

## Benefits of This Structure

| Benefit | Explanation |
|---------|-------------|
| **Separation of Concerns** | Locators, actions, and tests are separate |
| **Easy Maintenance** | Change selectors without touching action code |
| **Reusability** | Actions can be used in different test scenarios |
| **Scalability** | New pages follow the same pattern |
| **Testability** | Easy to mock and test individual components |
| **Documentation** | Clear structure shows what each file does |

## Adding a New Page

### Step 1: Create Locators

**File**: `pages/locators/your_page_locators.py`

```python
from selenium.webdriver.common.by import By
from pages.locators.base_locators import BaseLocators

class YourPageLocators(BaseLocators):
    """Locators for your page"""
    
    ELEMENT1 = (By.ID, "element1")
    ELEMENT2 = (By.CLASS_NAME, "element2")
    BUTTON = (By.XPATH, "//button[@id='submit']")
```

### Step 2: Create Actions

**File**: `pages/actions/your_page_actions.py`

```python
from pages.actions.base_actions import BaseActions
from pages.locators.your_page_locators import YourPageLocators

class YourPageActions(BaseActions):
    """Actions for your page"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = YourPageLocators()
    
    def perform_action(self):
        """Perform some action"""
        self.click_element(self.locators.BUTTON)
        self.logger.info("Action performed")
```

### Step 3: Create Page Facade

**File**: `pages/your_page.py`

```python
from pages.actions.your_page_actions import YourPageActions
from pages.locators.your_page_locators import YourPageLocators

class YourPage(YourPageActions):
    """Your page facade"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = YourPageLocators()
```

### Step 4: Create Tests

**File**: `tests/test_your_page.py`

```python
from base.base_test import BaseTest
from pages.your_page import YourPage
from pages.locators.your_page_locators import YourPageLocators

class TestYourPage(BaseTest):
    
    def setup_your_page_tests(self):
        self.your_page = YourPage(self.driver)
        self.locators = YourPageLocators()
    
    def test_your_scenario(self):
        self.navigate_to_app()
        self.your_page.perform_action()
        assert self.your_page.is_element_displayed(self.locators.ELEMENT1)
```

## Key Files Explained

### BaseLocators

Provides utility methods for all locator classes:
- `get_all_locators()` - Get all locators as dictionary
- `get_locator_count()` - Count total locators

### BaseActions

Extends BasePage with:
- `set_locators(locators)` - Set page locators
- `get_page_name()` - Get page class name
- All BasePage methods remain available

## Accessing Locators in Tests

### Method 1: Via page object
```python
# Locators accessible through page object
self.login_page.locators.USERNAME_INPUT
```

### Method 2: Direct locators class
```python
# Import and use locators directly
from pages.locators.login_locators import LoginLocators
locators = LoginLocators()
locators.USERNAME_INPUT
```

### Method 3: In fixture
```python
def setup_tests(self):
    self.login_page = LoginPage(self.driver)
    self.locators = LoginLocators()
    
    # Use via self.locators in tests
```

## Example: Complete Page Implementation

### Locators: `pages/locators/settings_locators.py`
```python
from selenium.webdriver.common.by import By
from pages.locators.base_locators import BaseLocators

class SettingsLocators(BaseLocators):
    # Form fields
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    
    # Buttons
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Save')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Cancel')]")
    
    # Messages
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success")
    ERROR_MESSAGE = (By.CLASS_NAME, "error")
```

### Actions: `pages/actions/settings_actions.py`
```python
from pages.actions.base_actions import BaseActions
from pages.locators.settings_locators import SettingsLocators

class SettingsActions(BaseActions):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = SettingsLocators()
    
    def update_email(self, email):
        self.send_keys(self.locators.EMAIL_INPUT, email)
    
    def update_phone(self, phone):
        self.send_keys(self.locators.PHONE_INPUT, phone)
    
    def save_settings(self):
        self.click_element(self.locators.SAVE_BUTTON)
    
    def is_success_message_displayed(self):
        return self.is_element_displayed(self.locators.SUCCESS_MESSAGE)
```

### Page: `pages/settings_page.py`
```python
from pages.actions.settings_actions import SettingsActions
from pages.locators.settings_locators import SettingsLocators

class SettingsPage(SettingsActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = SettingsLocators()
```

### Tests: `tests/test_settings.py`
```python
from base.base_test import BaseTest
from pages.settings_page import SettingsPage
from pages.locators.settings_locators import SettingsLocators

class TestSettings(BaseTest):
    
    def setup_tests(self):
        self.settings_page = SettingsPage(self.driver)
        self.locators = SettingsLocators()
    
    def test_update_email(self):
        self.navigate_to_app()
        self.settings_page.update_email("newemail@example.com")
        self.settings_page.save_settings()
        
        assert self.settings_page.is_success_message_displayed()
```

## Best Practices

1. **One locator per element** - Keep locators simple and specific
2. **Use meaningful names** - Locator names should describe the element
3. **Group related locators** - Organize by functional area
4. **Update locators, not actions** - If selector changes, only update locators file
5. **Reuse actions** - Common interactions should be in actions or BasePage
6. **Keep actions focused** - Each action method does one thing well
7. **Document locators** - Add comments for complex selectors
8. **Use locator constants** - Never hardcode selectors in test files

## Migration from Old Structure

If you have existing page objects, convert them:

### Old Pattern (All in one file)
```python
class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    
    def enter_username(self, username):
        self.send_keys(self.USERNAME, username)
```

### New Pattern (Separated)
```python
# Locators
class LoginLocators:
    USERNAME = (By.ID, "username")

# Actions
class LoginActions(BaseActions):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginLocators()
    
    def enter_username(self, username):
        self.send_keys(self.locators.USERNAME, username)

# Page
class LoginPage(LoginActions):
    pass
```

## Troubleshooting

### Issue: "ImportError: No module named 'pages.locators'"
**Solution**: Ensure `__init__.py` files exist in locators and actions folders

### Issue: "Locators not found" in tests
**Solution**: Make sure to import locators class and instantiate it in test fixture

### Issue: "AttributeError: 'LoginActions' object has no attribute 'locators'"
**Solution**: Call `super().__init__(driver)` in page action's `__init__`

---

**This new structure makes the framework more maintainable and scalable!**
