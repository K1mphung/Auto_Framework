# Quick Start Guide

Fast reference for common testing tasks with the AutoLogin Framework.

## ⚡ First-Time Setup (5 minutes)

```bash
# 1. Navigate to project
cd python

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
pytest --version
python -c "from selenium import webdriver; print('OK')"
```

## 🚀 Running Tests (Most Common Commands)

### Run All Tests
```bash
cd python
pytest src/test/python/tests -v
```

### Run Specific Test File
```bash
cd python
pytest src/test/python/tests/test_login.py -v
```

### Run Specific Test
```bash
cd python
pytest src/test/python/tests/test_login.py::TestLogin::test_successful_login -v
```

### Run with HTML Report
```bash
cd python
pytest src/test/python/tests -v --html=reports/report.html --self-contained-html
```

### Run in Parallel
```bash
cd python
pytest src/test/python/tests -n auto -v
```

## 🧪 Running Tests with TestNG

The framework supports TestNG-style test organization. Run tests using TestNG XML configuration or PyTest markers.

### Run by TestNG Suite (XML Configuration)

```bash
cd python

# List available suites
python -m utilities.testng_suite_runner list

# Run specific test suite
python -m utilities.testng_suite_runner run "Smoke Tests"
python -m utilities.testng_suite_runner run "Login Tests"

# Run by test group
python -m utilities.testng_suite_runner group smoke
python -m utilities.testng_suite_runner group login
python -m utilities.testng_suite_runner group regression

# Run in parallel (4 workers)
python -m utilities.testng_suite_runner parallel 4
```

### Run by PyTest Marker Groups

```bash
cd python

# Run all smoke tests
pytest src/test/python/tests -m smoke -v

# Run all login tests
pytest src/test/python/tests -m login -v

# Run tests with multiple markers (OR)
pytest src/test/python/tests -m "smoke or login" -v

# Run high-priority tests
pytest src/test/python/tests -m priority1 -v

# Run regression tests
pytest src/test/python/tests -m regression -v

# Run integration tests
pytest src/test/python/tests -m integration -v

# Combine markers (AND/NOT)
pytest src/test/python/tests -m "regression and not slow" -v
```

### Available Test Groups/Markers

| Marker | Purpose |
|--------|---------|
| `smoke` | Quick sanity tests (must pass) |
| `login` | Login feature tests |
| `regression` | Comprehensive regression tests |
| `ui` | UI component tests |
| `integration` | Integration tests |
| `functional` | Functional tests |
| `performance` | Performance tests |
| `critical` | Critical must-pass tests |
| `priority1` | High priority tests |
| `priority2` | Medium priority tests |
| `priority3` | Low priority tests |

### Creating TestNG Tests

Use TestNG decorators in your tests:

```python
from utilities.testng_decorators import test_method, before_method, after_method
import pytest

class TestMyFeature(BaseTest):
    
    @before_method()
    def setup_test(self):
        self.my_page = MyPage(self.driver)
    
    @test_method(
        name="test_feature",
        description="Test feature description",
        priority=1,
        groups=["smoke", "priority1"]
    )
    @pytest.mark.smoke
    @pytest.mark.priority1
    def test_feature_works(self):
        self.navigate_to_app()
        self.my_page.perform_action()
        self.assert_url_contains("expected")
    
    @after_method(alwaysRun=True)
    def cleanup_test(self):
        # Cleanup code
        pass
```

See [TESTNG_INTEGRATION.md](TESTNG_INTEGRATION.md) for full TestNG guide and examples.

## 🔧 Configuration Changes

### Change Browser
Edit `src/test/python/config/config.properties`:
```properties
[browser]
name = firefox     # change from chrome to firefox
```

### Change Application URL
Edit `src/test/python/config/config.properties`:
```properties
[application]
base_url = http://your-app-url.com
```

### Enable Headless Mode
Edit `src/test/python/config/config.properties`:
```properties
[browser]
headless = true    # change from false to true
```

## 📝 Adding a New Test

### Step 1: Create Page Object
Edit or create `src/test/python/pages/your_page.py`:

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class YourPage(BasePage):
    # Define locators
    ELEMENT_NAME = (By.ID, "element_id")
    
    def your_action(self):
        """Perform action"""
        self.click_element(self.ELEMENT_NAME)
        self.logger.info("Action performed")
```

### Step 2: Create Test Case
Edit or create `src/test/python/tests/test_your_feature.py`:

```python
import pytest
from base.base_test import BaseTest
from pages.your_page import YourPage

class TestYourFeature(BaseTest):
    
    @pytest.fixture(autouse=True)
    def setup_tests(self):
        self.your_page = YourPage(self.driver)
        yield
    
    def test_your_scenario(self):
        """Test description"""
        # Arrange
        test_data = "some value"
        
        # Act
        self.navigate_to_app()
        self.your_page.your_action()
        
        # Assert
        self.assert_url_contains("expected_url")
        self.logger.info("✓ Test passed")
```

### Step 3: Run Your Test
```bash
cd python
pytest src/test/python/tests/test_your_feature.py::TestYourFeature::test_your_scenario -v
```

## 🐛 Debugging Tests

### View Logs
```bash
# Real-time logs
tail -f logs/automation_test_*.log  # Linux/macOS
Get-Content logs\automation_test_*.log -Wait  # Windows

# Or check in reports folder
ls logs/
```

### Run with Debug Output
```bash
cd python
pytest src/test/python/tests -v -s --log-cli-level=DEBUG
```

### Capture Specific Screenshots
```python
# In your test
self.take_screenshot("step1")
self.take_screenshot("step2")
# Screenshots saved in: screenshots/
```

### Add Debug Breakpoint
```python
# In test code
import pdb; pdb.set_trace()  # Execution pauses here

# In IDE: Set breakpoint and run with debugger
```

## 📊 Viewing Reports

### After Test Run
```bash
cd python

# Open HTML report (generated by default)
# Windows
start reports\report.html

# Linux/macOS
open reports/report.html
```

### Coverage Report
```bash
cd python
pytest src/test/python/tests --cov=src/test/python --cov-report=html:reports/coverage

# View report
# Windows
start reports\coverage\index.html

# Linux/macOS
open reports/coverage/index.html
```

## 🔄 Using Maven

### Run Tests via Maven
```bash
cd python
mvn clean test
```

### Run with Specific Browser
```bash
cd python
mvn clean test -Dbrowser=firefox
```

### Run Parallel Tests
```bash
cd python
mvn clean test -P parallel
```

### Package Framework
```bash
cd python
mvn clean package -DskipTests
```

## 🌐 CI/CD Pipeline Status

### Check GitHub Actions
1. Go to repository
2. Click "Actions" tab
3. View latest workflow run
4. Download artifacts

### Check Jenkins
1. Go to Jenkins dashboard
2. View job status
3. Click on build number
4. View logs and reports

## 📚 Common Page Object Operations

```python
# Click element
self.login_page.click_element(self.login_page.LOGIN_BUTTON)

# Send keys to field
self.login_page.send_keys(self.login_page.USERNAME_INPUT, "username")

# Get element text
text = self.login_page.get_element_text(self.login_page.MESSAGE)

# Check if element visible
if self.login_page.is_element_displayed(self.login_page.ERROR_MSG):
    # Handle error

# Wait for element
element = self.wait_helper.wait_for_element_visible(locator)

# Select dropdown
self.login_page.select_dropdown_by_text(locator, "Option Text")

# Hover over element
self.login_page.hover_over_element(locator)

# Right-click element
self.login_page.right_click_element(locator)
```

## ⚡ Common Assertions

```python
# Assert text in page
self.assert_text_in_page("Expected Text")

# Assert element visible
self.assert_element_visible(locator)

# Assert URL contains
self.assert_url_contains("dashboard")

# Assert title contains
self.assert_page_title_contains("Home")
```

## 🔑 Key File Locations

| Item | Location |
|------|----------|
| Configuration | `src/test/python/config/config.properties` |
| Test Cases | `src/test/python/tests/` |
| Page Objects | `src/test/python/pages/` |
| Base Classes | `src/test/python/base/` |
| Utilities | `src/test/python/utilities/` |
| Test Data | `src/test/python/test_data/` |
| Reports | `reports/` |
| Logs | `logs/` |
| Screenshots | `screenshots/` |
| Properties | `pom.xml` |

## 📞 Quick Help

### Issue: Tests not running
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run pytest with verbose output
pytest --version
pytest src/test/python/tests -v
```

### Issue: WebDriver not found
```bash
# Reinstall webdriver-manager
pip install --upgrade webdriver-manager

# Clear driver cache
rm -rf ~/.wdm  # Linux/macOS
rmdir /s %USERPROFILE%\.wdm  # Windows
```

### Issue: Element not found
1. Check locator in browser DevTools (F12)
2. Take screenshot: `self.take_screenshot()`
3. Review wait times in `config.properties`
4. Check application is loaded

### Issue: Slow tests
```bash
# Run in parallel
pytest src/test/python/tests -n auto

# Check wait times - may be too long
# Edit: src/test/python/config/config.properties
```

## 🎯 Test Naming Convention

```
test_<feature>_<scenario>.py           # File name
class Test<Feature><Scenario>          # Class name
def test_<action>_<expected_result>    # Method name

Examples:
test_login
test_login_with_invalid_credentials
TestLogin
TestLoginWithInvalidCredentials
test_successful_login
test_login_with_invalid_password
```

## 💡 Pro Tips

1. **Use Page Objects**: Don't use selectors directly in tests
2. **Keep Tests Small**: One assertion per test method when possible
3. **Use Waits**: Never use `time.sleep()` in tests
4. **Log Everything**: Use `self.logger.info()` for important steps
5. **Take Screenshots**: Capture on failures for debugging
6. **Organize Tests**: Use markers (`@pytest.mark.login`, etc.)
7. **Keep Data Separate**: Use test data files, not hardcoded values
8. **Use Fixtures**: Leverage PyTest fixtures for setup/teardown
9. **Test Independently**: Each test should not depend on others
10. **Document Tests**: Write clear docstrings explaining test purpose

## 📖 Related Documentation

- [Full README](README.md) - Comprehensive documentation
- [CHANGELOG](CHANGELOG.md) - Version history
- [Selenium Docs](https://www.selenium.dev/documentation/)
- [PyTest Docs](https://docs.pytest.org/)
- [Maven Docs](https://maven.apache.org/guides/)

---

**Need help?** Check logs, take screenshots, and review config!
