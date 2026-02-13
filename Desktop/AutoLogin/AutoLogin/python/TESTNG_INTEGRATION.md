# TestNG Integration Guide

## Overview

The AutoLogin framework now includes **TestNG integration** with:
- TestNG-style annotations/decorators for Python
- TestNG XML configuration file for test organization
- TestNG Suite Runner to execute tests based on XML configuration
- Test grouping and prioritization support

Even though we use PyTest, the TestNG patterns provide familiar structure for QA teams.

## Why TestNG for Python Tests?

| Benefit | Usage |
|---------|-------|
| **Familiar Structure** | QA teams already know TestNG patterns from Java |
| **XML Configuration** | Organize tests in structured XML file |
| **Test Grouping** | Group tests by feature, priority, or purpose |
| **Suite Management** | Run specific suites without command line complexity |
| **Parallel Execution** | Configure parallel execution in XML |
| **Reporting** | Use TestNG-style reporting concepts |

## TestNG Decorators

### 1. @test_method

Marks a method as a test with metadata.

```python
from utilities.testng_decorators import test_method

@test_method(
    name="test_login",
    description="Test successful login",
    groups=["login", "smoke"],
    priority=1,
    enabled=True,
    timeout=5000
)
def test_successful_login(self):
    pass
```

**Parameters:**
- `name`: Test name (defaults to method name)
- `description`: Test description
- `priority`: Priority level 0-10 (0 = highest)
- `groups`: List of test groups/categories
- `enabled`: Whether test is enabled
- `timeout`: Timeout in milliseconds
- `depends_on_methods`: List of dependent test methods

### 2. @before_method

Runs before each test method.

```python
from utilities.testng_decorators import before_method

@before_method(alwaysRun=False)
def setup_test(self):
    """Setup before each test"""
    self.login_page = LoginPage(self.driver)
```

### 3. @after_method

Runs after each test method.

```python
from utilities.testng_decorators import after_method

@after_method(alwaysRun=True)
def cleanup_test(self):
    """Cleanup after each test - runs even if test fails"""
    self.driver.quit()
```

### 4. @before_class

Runs once before all tests in class.

```python
from utilities.testng_decorators import before_class

@before_class()
def setup_class(self):
    """Setup for entire test class"""
    self.browser = 'chrome'
```

### 5. @after_class

Runs once after all tests in class complete.

```python
from utilities.testng_decorators import after_class

@after_class()
def cleanup_class(self):
    """Cleanup for entire test class"""
    print("All tests completed")
```

### 6. @skip

Skips test with reason.

```python
from utilities.testng_decorators import skip

@skip("Not ready yet")
def test_future_feature(self):
    pass
```

### 7. @data_provider

Provides test data for parameterized tests.

```python
from utilities.testng_decorators import data_provider

@data_provider([
    ["user1@example.com", "password1"],
    ["user2@example.com", "password2"],
    ["user3@example.com", "password3"]
])
def test_login_with_data(self, username, password):
    self.login_page.login(username, password)
```

## TestNG XML Configuration

### File: `testng.xml`

Located at project root, defines test suites and groups.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "http://testng.org/testng-current.dtd">

<suite name="AutoLogin Test Suite" verbose="3" parallel="methods" thread-count="4">
    
    <!-- Test suite 1: Smoke tests -->
    <test name="Smoke Tests" enabled="true">
        <groups>
            <run>
                <include name="smoke"/>
            </run>
        </groups>
        <classes>
            <class name="tests.test_login.TestLogin">
                <methods>
                    <include name="test_successful_login"/>
                </methods>
            </class>
        </classes>
    </test>
    
    <!-- Test suite 2: Login tests -->
    <test name="Login Tests" enabled="true">
        <groups>
            <run>
                <include name="login"/>
            </run>
        </groups>
        <classes>
            <class name="tests.test_login.TestLogin"/>
        </classes>
    </test>
    
    <!-- Parameters -->
    <parameter name="browser" value="chrome"/>
    <parameter name="base_url" value="http://localhost:8080/login"/>
    
</suite>
```

### XML Attributes

| Attribute | Example | Description |
|-----------|---------|-------------|
| `name` | "AutoLogin Test Suite" | Suite/Test name |
| `enabled` | true/false | Enable/disable suite |
| `verbose` | 0-3 | Verbosity level |
| `parallel` | methods/classes/tests | Parallel execution level |
| `thread-count` | 4 | Number of parallel threads |

## TestNG Suite Runner

### Command Line Usage

```bash
# List all available suites
python -m utilities.testng_suite_runner list

# Run specific suite
python -m utilities.testng_suite_runner run "Smoke Tests"

# Run tests by group
python -m utilities.testng_suite_runner group smoke

# Run tests in parallel
python -m utilities.testng_suite_runner parallel 4
```

### Python Usage

```python
from utilities.testng_suite_runner import TestNGSuiteRunner

# Create runner
runner = TestNGSuiteRunner('testng.xml')

# List suites
runner.list_suites()

# Run specific suite
runner.run_suite('Smoke Tests')

# Run by group
runner.run_group('smoke')

# Run in parallel
runner.run_parallel(num_workers=4)
```

## Test Groups (PyTest Markers)

Groups organize tests for selective execution.

### Defined Groups

| Group | Purpose |
|-------|---------|
| `smoke` | Quick sanity checks (must pass) |
| `login` | Login-related tests |
| `regression` | Comprehensive regression tests |
| `ui` | UI component tests |
| `integration` | Integration tests |
| `functional` | Functional tests |
| `performance` | Performance tests |
| `critical` | Must-pass tests |
| `priority1` | High priority |
| `priority2` | Medium priority |
| `priority3` | Low priority |

### Using Groups in Tests

```python
import pytest

class TestLogin(BaseTest):
    
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.priority1
    def test_successful_login(self):
        pass
    
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_password(self):
        pass
```

### Running Tests by Group

```bash
# Run all smoke tests
pytest tests -m smoke -v

# Run login tests
pytest tests -m login -v

# Run smoke AND login tests
pytest tests -m "smoke or login" -v

# Run regression AND NOT slow tests
pytest tests -m "regression and not slow" -v

# Run high priority tests
pytest tests -m priority1 -v
```

## Example Test Suite

### Using TestNG Decorators

```python
import pytest
from base.base_test import BaseTest
from pages.login_page import LoginPage
from utilities.testng_decorators import (
    test_method,
    before_method,
    after_method,
    skip,
    data_provider
)

class TestLoginSuite(BaseTest):
    
    @before_method()
    def setup_test(self):
        """Setup before each test"""
        self.login_page = LoginPage(self.driver)
    
    @test_method(
        name="successful_login",
        description="Test successful login with valid credentials",
        groups=["smoke", "login"],
        priority=1
    )
    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.priority1
    def test_successful_login(self):
        """Test successful login"""
        self.navigate_to_app()
        self.login_page.login("user@example.com", "password")
        self.assert_url_contains("dashboard")
    
    @test_method(
        name="invalid_credentials",
        description="Test login with invalid credentials",
        groups=["regression", "login"]
    )
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_credentials(self):
        """Test invalid credentials handling"""
        self.navigate_to_app()
        self.login_page.login("invalid@example.com", "wrong")
        assert self.login_page.is_error_message_displayed()
    
    @test_method(
        name="login_with_data",
        description="Parameterized login test",
        groups=["login"]
    )
    @pytest.mark.login
    @data_provider([
        ["user1@example.com", "pass1"],
        ["user2@example.com", "pass2"]
    ])
    def test_login_with_data(self, username, password):
        """Test login with multiple data sets"""
        self.navigate_to_app()
        self.login_page.login(username, password)
    
    @skip("Feature not yet implemented")
    def test_biometric_login(self):
        """Test biometric login"""
        pass
    
    @after_method(alwaysRun=True)
    def cleanup_test(self):
        """Cleanup after each test"""
        # Take screenshot on failure
        pass
```

## Test Organization Patterns

### Pattern 1: By Feature

```xml
<test name="Login Feature Tests">
    <groups>
        <run><include name="login"/></run>
    </groups>
</test>

<test name="Dashboard Feature Tests">
    <groups>
        <run><include name="dashboard"/></run>
    </groups>
</test>
```

### Pattern 2: By Priority

```xml
<test name="High Priority Tests">
    <groups>
        <run><include name="priority1"/></run>
    </groups>
</test>

<test name="Medium Priority Tests">
    <groups>
        <run><include name="priority2"/></run>
    </groups>
</test>
```

### Pattern 3: By Execution Type

```xml
<test name="Smoke Tests - Quick">
    <groups>
        <run><include name="smoke"/></run>
    </groups>
</test>

<test name="Regression Tests - Full">
    <groups>
        <run><include name="regression"/></run>
    </groups>
</test>

<test name="Parallel Execution">
    <groups>
        <run><include name="parallel"/></run>
    </groups>
</test>
```

## Running Tests

### Via Maven

```bash
# Run tests using Maven
cd python
mvn clean test

# Run specific suite (via properties)
mvn clean test -Dsuite=Smoke
```

### Via PyTest

```bash
cd python/src/test/python

# Run all tests
pytest tests -v

# Run by group marker
pytest tests -m smoke -v

# Run specific test
pytest tests/test_login.py::TestLogin::test_successful_login -v
```

### Via TestNG Suite Runner

```bash
# List suites
python -m utilities.testng_suite_runner list

# Run Smoke Tests suite
python -m utilities.testng_suite_runner run "Smoke Tests"

# Run in parallel (4 workers)
python -m utilities.testng_suite_runner parallel 4
```

## TestNG Concepts Mapping

### From Java TestNG to Python

| Java TestNG | Python Equivalent | File |
|-------------|------------------|------|
| @Test | @test_method | testng_decorators.py |
| @BeforeMethod | @before_method | testng_decorators.py |
| @AfterMethod | @after_method | testng_decorators.py |
| @BeforeClass | @before_class | testng_decorators.py |
| @AfterClass | @after_class | testng_decorators.py |
| @Skip | @skip | testng_decorators.py |
| @DataProvider | @data_provider | testng_decorators.py |
| groups | pytest.mark | pytest.ini |
| priority | @test_method priority | testng_decorators.py |
| testng.xml | testng.xml | testng.xml |

## Test Registry

Access test metadata at runtime:

```python
from utilities.testng_decorators import get_test_registry, get_tests_by_group

# Get all tests
all_tests = get_test_registry()

# Get tests in group
smoke_tests = get_tests_by_group('smoke')

# Get test info
for test_name, test_info in all_tests.items():
    print(f"{test_name}: {test_info['description']}")
```

## Best Practices

1. **Use Groups Consistently**
   ```python
   @pytest.mark.smoke
   @pytest.mark.login
   @pytest.mark.priority1
   def test_something(self):
       pass
   ```

2. **Set Priorities**
   - Priority 1-2: Critical tests (smoke tests)
   - Priority 3-5: Important tests (regression)
   - Priority 6-10: Nice-to-have tests

3. **Use Dependencies**
   ```python
   @test_method(depends_on_methods=['test_login'])
   def test_logout(self):
       pass
   ```

4. **Organize in XML**
   - One test per functional area
   - Include related test methods
   - Use parallel execution for independent tests

5. **Clear Descriptions**
   ```python
   @test_method(
       description="Verify user can login with valid credentials",
       # ...
   )
   ```

## Troubleshooting

### Issue: Tests not recognized by runner
**Solution**: Ensure pytest markers are defined in pytest.ini

### Issue: Decorator not applied
**Solution**: Import decorator before using it

### Issue: TestNG XML not parsed
**Solution**: Check XML syntax and file path

### Issue: Tests not running in parallel
**Solution**: Use `pytest -n auto` from command line

## Integration with CI/CD

### GitHub Actions

```yaml
- name: Run TestNG Suites
  run: |
    cd python
    python -m utilities.testng_suite_runner parallel 4
```

### Jenkins

```groovy
stage('Run Tests') {
    steps {
        sh 'cd python && python -m utilities.testng_suite_runner run "Regression Tests"'
    }
}
```

## Migration from Old Tests

Convert existing tests:

### Before
```python
def test_login(self):
    pass
```

### After
```python
@pytest.mark.smoke
@pytest.mark.login
@test_method(
    description="Test login functionality",
    groups=["smoke", "login"],
    priority=1
)
def test_login(self):
    pass
```

## Files Added

| File | Purpose |
|------|---------|
| `testng.xml` | TestNG configuration |
| `utilities/testng_decorators.py` | TestNG-style decorators |
| `utilities/testng_suite_runner.py` | Test suite runner |
| `pytest.ini` | Updated with TestNG-style markers |

## References

- [TestNG Documentation](https://testng.org/)
- [PyTest Markers](https://docs.pytest.org/en/stable/how-to/mark.html)
- [Framework Documentation](README.md)

---

**TestNG integration provides familiar patterns while leveraging PyTest's power!**
