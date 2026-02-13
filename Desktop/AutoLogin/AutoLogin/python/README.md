# AutoLogin Automation Testing Framework

A production-ready test automation framework built with Python, Selenium WebDriver, and PyTest, following the Page Object Model (POM) design pattern with OOP principles.

## 📋 Table of Contents

- [Framework Architecture](#framework-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [TestNG Integration](#testng-integration)
- [Maven Integration](#maven-integration)
- [CI/CD Integration](#cicd-integration)
- [Reporting & Logging](#reporting--logging)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🏗️ Framework Architecture

### Key Design Principles

1. **Page Object Model (POM)**: Encapsulates page elements and interactions
2. **OOP Principles**: Uses inheritance, abstraction, and encapsulation
3. **Separation of Concerns**: Tests, pages, utilities, and configuration are separated
4. **Reusability**: Common functionality in base classes
5. **Maintainability**: Easy to add new tests and modify existing ones

### Architecture Layers

```
┌─────────────────────────────────────────────────┐
│            Test Cases (PyTest)                  │
│        (test_login.py, test_dashboard.py)       │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────┐
│         Page Objects (POM)                      │
│  (BasePage, LoginPage, DashboardPage)           │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────┐
│    Base Classes & Utilities                     │
│  (BaseTest, WaitHelper, ScreenshotHandler)      │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────┐
│    Selenium WebDriver & Configuration           │
│  (DriverFactory, ConfigReader)                  │
└─────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
python/
├── src/
│   └── test/
│       └── python/
│           ├── __init__.py
│           ├── base/
│           │   ├── __init__.py
│           │   └── base_test.py                    # Base test class with fixtures
│           │
│           ├── pages/
│           │   ├── __init__.py
│           │   ├── base_page.py                    # Base page object class
│           │   └── login_page.py                   # Login page implementation
│           │
│           ├── tests/
│           │   ├── __init__.py
│           │   └── test_login.py                   # Login test cases
│           │
│           ├── utilities/
│           │   ├── __init__.py
│           │   ├── driver_factory.py               # WebDriver creation
│           │   ├── logger_config.py                # Logging configuration
│           │   ├── wait_helper.py                  # Explicit waits
│           │   └── screenshot_handler.py           # Screenshot management
│           │
│           ├── config/
│           │   ├── __init__.py
│           │   ├── config.properties               # Configuration file
│           │   └── config_reader.py                # Config reader utility
│           │
│           ├── test_data/
│           │   ├── login_data.json                 # Test data
│           │   └── test_data.csv
│           │
│           ├── conftest.py                         # PyTest fixtures & plugins
│           └── pytest.ini                          # PyTest configuration
│
├── reports/                                        # Test execution reports
├── logs/                                           # Test execution logs
├── screenshots/                                    # Screenshots on failure
├── .github/
│   └── workflows/
│       └── automation-tests.yml                    # GitHub Actions CI/CD
├── pom.xml                                         # Maven configuration
├── Jenkinsfile                                     # Jenkins pipeline
├── requirements.txt                                # Python dependencies
└── README.md                                       # This file
```

---

## 📦 Prerequisites

### System Requirements

- **OS**: Windows, Linux, or macOS
- **Java**: JDK 11 or higher (for Maven)
- **Python**: 3.9 or higher
- **Maven**: 3.6 or higher
- **Browsers**: Chrome/Firefox (with stable versions)

### Installation Verification

```bash
# Verify Java
java -version

# Verify Maven
mvn --version

# Verify Python
python --version

# Verify pip
pip --version
```

---

## 🔧 Installation & Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd python
```

### Step 2: Install Java & Maven

**Windows**:
```powershell
# If using Chocolatey
choco install javaruntime maven
```

**Linux/macOS**:
```bash
# Using Homebrew (macOS)
brew install java maven

# Using apt (Ubuntu/Debian)
sudo apt-get install openjdk-11-jdk maven
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Test PyTest installation
pytest --version

# Test Selenium installation
python -c "from selenium import webdriver; print('Selenium OK')"

# Test configuration
python -c "from config.config_reader import ConfigReader; print('Config OK')"
```

---

## ⚙️ Configuration

### Configuration File

Edit `src/test/python/config/config.properties`:

```properties
# Browser: chrome or firefox
[browser]
name = chrome
headless = false

# Application URL
[application]
base_url = http://localhost:8080/login

# Wait times in seconds
[wait]
implicit_wait = 10
explicit_wait = 15

# Screenshots
[screenshot]
on_failure = true
path = ./screenshots

# Reports
[reporting]
report_path = ./reports

# Logging
[logging]
level = INFO
log_path = ./logs
```

### Environment Variables (Optional)

Override config via environment variables:

```bash
# Windows
set BASE_URL=http://your-app.com
set BROWSER=firefox
set HEADLESS=true

# Linux/macOS
export BASE_URL=http://your-app.com
export BROWSER=firefox
export HEADLESS=true
```

---

## 🚀 Running Tests

### Using PyTest Directly

```bash
# Run all tests
pytest src/test/python/tests -v

# Run specific test file
pytest src/test/python/tests/test_login.py -v

# Run specific test
pytest src/test/python/tests/test_login.py::TestLogin::test_successful_login -v

# Run with markers
pytest src/test/python/tests -m login -v

# Run with specific browser
# (Modify config.properties or environment variable)
pytest src/test/python/tests -v

# Generate HTML report
pytest src/test/python/tests --html=reports/report.html --self-contained-html

# Generate with coverage
pytest src/test/python/tests --cov=src/test/python --cov-report=html:reports/coverage

# Run in parallel (requires pytest-xdist)
pytest src/test/python/tests -n auto -v

# Run with specific log level
pytest src/test/python/tests -v -o log_cli_level=DEBUG
```

### Using Maven

```bash
# Run all tests
mvn clean test

# Run specific browser
mvn clean test -Dbrowser=firefox

# Run with specific profile
mvn clean test -P dev          # Development
mvn clean test -P ci           # CI/CD environment
mvn clean test -P parallel     # Parallel execution
mvn clean test -P headless     # Headless mode

# Run smoke tests only
mvn clean test -Dgroups=smoke

# Run and skip
mvn clean test -DskipTests     # Skip tests
```

### Test Execution Examples

```bash
# Example 1: Run with Chrome in headless mode
cd python
pytest src/test/python/tests/test_login.py -v

# Example 2: Run with coverage report
cd python
pytest src/test/python/tests --cov=src/test/python --cov-report=html

# Example 3: Run with HTML report
cd python
pytest src/test/python/tests --html=reports/report.html --self-contained-html

# Example 4: Run in parallel (4 workers)
cd python
pytest src/test/python/tests -n 4 -v

# Example 5: Run with detailed logging
cd python
pytest src/test/python/tests -v -s --log-cli-level=DEBUG
```

---

## 🧪 TestNG Integration

The framework includes **TestNG-style decorators and XML configuration** to provide familiar test organization patterns, even though we use PyTest as the primary test runner.

### Why TestNG Integration?

- **Familiar Patterns**: QA teams already know TestNG from Java testing
- **XML Organization**: Organize tests in structured `testng.xml` file
- **Test Grouping**: Group tests by feature, priority, or type
- **Metadata**: Attach rich metadata to tests (priority, dependencies, timeout)
- **Test Registry**: Access test information programmatically at runtime

### Quick Start

#### 1. Use TestNG Decorators

```python
from utilities.testng_decorators import test_method, before_method, after_method
import pytest

class TestLogin(BaseTest):
    
    @before_method()
    def setup_test(self):
        self.login_page = LoginPage(self.driver)
    
    @test_method(
        name="successful_login",
        description="Test successful login",
        priority=1,
        groups=["smoke", "login"]
    )
    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login(self):
        self.login_page.login("user@example.com", "password")
        self.assert_url_contains("dashboard")
    
    @after_method(alwaysRun=True)
    def cleanup_test(self):
        # Cleanup code
        pass
```

#### 2. Use TestNG XML Configuration

The `testng.xml` file organizes tests into logical suites:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "http://testng.org/testng-current.dtd">

<suite name="AutoLogin Test Suite" parallel="methods" thread-count="4">
    
    <test name="Smoke Tests">
        <groups>
            <run><include name="smoke"/></run>
        </groups>
        <classes>
            <class name="tests.test_login.TestLogin"/>
        </classes>
    </test>
    
</suite>
```

#### 3. Run via TestNG Suite Runner

```bash
# List available suites
python -m utilities.testng_suite_runner list

# Run specific suite
python -m utilities.testng_suite_runner run "Smoke Tests"

# Run by group
python -m utilities.testng_suite_runner group smoke

# Run in parallel (4 workers)
python -m utilities.testng_suite_runner parallel 4
```

### TestNG Decorators Available

| Decorator | Purpose | Example |
|-----------|---------|---------|
| `@test_method()` | Mark test with metadata | `@test_method(priority=1, groups=["smoke"])` |
| `@before_method()` | Setup before each test | `@before_method()` |
| `@after_method()` | Cleanup after each test | `@after_method(alwaysRun=True)` |
| `@before_class()` | Setup for test class | `@before_class()` |
| `@after_class()` | Cleanup for test class | `@after_class()` |
| `@skip()` | Skip test | `@skip("Not ready yet")` |
| `@data_provider()` | Parameterized test data | `@data_provider([[1,2], [3,4]])` |

### Test Groups (PyTest Markers)

```python
@pytest.mark.smoke        # Quick sanity tests
@pytest.mark.login        # Login feature tests
@pytest.mark.regression   # Regression test suite
@pytest.mark.ui           # UI component tests
@pytest.mark.integration  # Integration tests
@pytest.mark.functional   # Functional tests
@pytest.mark.performance  # Performance tests
@pytest.mark.critical     # Must-pass tests
@pytest.mark.priority1    # High priority
@pytest.mark.priority2    # Medium priority
@pytest.mark.priority3    # Low priority
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
```

### Test Registry

Access test metadata programmatically:

```python
from utilities.testng_decorators import get_test_registry, get_tests_by_group

# Get all tests
all_tests = get_test_registry()

# Get tests by group
smoke_tests = get_tests_by_group('smoke')

# Access test info
for test_name, test_info in smoke_tests.items():
    print(f"{test_name}: {test_info['description']}")
```

### Files Added

| File | Purpose |
|------|---------|
| `testng.xml` | TestNG suite configuration |
| `utilities/testng_decorators.py` | TestNG-style decorators |
| `utilities/testng_suite_runner.py` | Suite runner CLI |
| `tests/test_example_testng.py` | Example demonstrating decorators |
| `TESTNG_INTEGRATION.md` | Comprehensive integration guide |

### More Information

For complete TestNG integration details:

- **Full Guide**: See [TESTNG_INTEGRATION.md](TESTNG_INTEGRATION.md)
- **Examples**: See [tests/test_example_testng.py](tests/test_example_testng.py)
- **Current Tests**: See [tests/test_login.py](tests/test_login.py) for real examples

### TestNG + PyTest Integration

Both can coexist in the same project:

```bash
# Run as PyTest (primary)
pytest tests -v

# Run specific TestNG suite
python -m utilities.testng_suite_runner run "Smoke Tests"

# Run with both markers and decorators
pytest tests -m smoke -v  # Uses PyTest markers
python -m utilities.testng_suite_runner run "Smoke Tests"  # Uses XML config
```

---

## 🛠️ Maven Integration

### Maven Architecture

While Maven is primarily a Java build tool, this framework uses Maven as an orchestrator for Python test execution through the **Maven Exec Plugin**.

### Key Maven Features

1. **Dependency Management**: Python dependencies via `requirements.txt`
2. **Build Phases**: Clean, test, package, deploy
3. **Profiles**: Dev, CI, Parallel, Headless
4. **Plugins**: Exec, Clean, Assembly

### Maven Lifecycle

```
mvn clean          # Clean build artifacts
mvn test           # Run tests
mvn package        # Package framework
mvn install        # Install locally
mvn deploy         # Deploy to repository
```

### Maven Commands for This Framework

```bash
# Initialize and install dependencies
mvn initialize

# Run tests
mvn clean test

# Run tests with specific profile
mvn clean test -P ci

# Run specific test class
mvn clean test -Dtest=TestLogin

# Run with custom properties
mvn clean test -Dpython.executable=python3 -Dbrowser=firefox

# Generate reports
mvn clean test -Dreport.format=html

# Package framework
mvn clean package

# Skip tests during package
mvn clean package -DskipTests
```

### Important Note on Maven-Python Integration

Maven integrates with Python through:
- **Exec Maven Plugin**: Executes Python commands
- **requirements.txt**: Manages Python dependencies
- **conftest.py**: PyTest configuration

Python packages are NOT declared in `pom.xml` but in `requirements.txt`.

---

## 🔄 CI/CD Integration

### GitHub Actions

The framework includes a complete GitHub Actions workflow (`.github/workflows/automation-tests.yml`):

#### Features

- **Multi-OS Testing**: Runs on Ubuntu and Windows
- **Multi-Python Version**: Tests Python 3.9, 3.10, 3.11
- **Multi-Browser**: Runs on Chrome and Firefox
- **Parallel Execution**: Separate parallel test job
- **Reports**: Automatic uploading of reports and artifacts
- **Coverage**: Integration with Codecov
- **Notifications**: Slack notifications on completion

#### Setup GitHub Actions

1. Push repository to GitHub
2. No additional setup required (workflow file is included)
3. Customize Slack webhook in repository secrets if needed

#### View Results

- Go to "Actions" tab in GitHub
- Click on workflow run
- View logs and download artifacts

### Jenkins Pipeline

The framework includes Jenkins Declarative Pipeline (`Jenkinsfile`):

#### Features

- **Parallel Browser Testing**: Chrome and Firefox in parallel
- **Code Quality**: Pylint, flake8, black checks
- **HTML Reports**: Published test and coverage reports
- **JUnit Results**: Integration with Jenkins test results
- **Artifact Archiving**: Screenshots, logs, reports
- **Webhooks**: SCM polling and webhook triggers

#### Setup Jenkins

1. **Create Job**:
   - New Item → Pipeline
   - Pipeline script from SCM → Git
   - Repository URL: `<your-repo>`
   - Script path: `python/Jenkinsfile`

2. **Configure Credentials**:
   - GitHub credentials (if private repo)

3. **Build Triggers** (optional):
   - GitHub hook trigger
   - Poll SCM schedule

4. **Run Builds**:
   - Manual trigger or SCM webhook

---

## 📊 Reporting & Logging

### Test Reports

Reports are generated in `./reports/` directory:

```
reports/
├── report.html                      # HTML test report (pytest-html)
├── junit.xml                        # JUnit format (for Jenkins/CI)
├── coverage/                        # Code coverage report
│   └── index.html
└── allure-results/ (if using allure)
    └── *.json
```

### View Reports

```bash
# After test execution
cd python

# Open HTML report
# Windows
start reports\report.html

# Linux/macOS
open reports/report.html
```

### Logging

Logs are generated in `./logs/` directory:

```
logs/
├── automation_test_20240101_080000.log
├── pytest.log
└── ...
```

### Log Configuration

Configure in `config.properties`:

```properties
[logging]
level = INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
log_path = ./logs
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General status messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

---

## 🎯 Best Practices

### Writing Tests

```python
# ✓ Good: Follows convention and clear intent
def test_successful_login(self):
    """Test successful login with valid credentials"""
    # Arrange
    username = "user@example.com"
    password = "SecurePass123!"
    
    # Act
    self.login_page.login(username, password)
    
    # Assert
    self.assert_url_contains("dashboard")

# ✗ Bad: Unclear test name, no documentation
def test1(self):
    self.driver.get("http://app.com")
    # ...
```

### Creating Page Objects

```python
# ✓ Good: Encapsulated locators, clear methods
class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    
    def login(self, username, password):
        """Complete login flow"""
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

# ✗ Bad: Locators in test methods, repeated code
def test_login(self):
    self.driver.find_element(By.ID, "username").send_keys("user")
    self.driver.find_element(By.ID, "password").send_keys("pass")
    self.driver.find_element(By.XPATH, "//button[...]").click()
```

### Wait Strategies

```python
# ✓ Good: Explicit waits (recommended)
element = self.wait_helper.wait_for_element_clickable(LoginPage.LOGIN_BUTTON)
element.click()

# ✗ Bad: Implicit waits or sleep
import time
time.sleep(5)  # Hard waits - unreliable
self.driver.find_element(By.ID, "username")
```

### Error Handling

```python
# ✓ Good: Proper exception handling and logging
try:
    self.login_page.login(username, password)
except TimeoutException:
    self.logger.error("Login button not found")
    self.take_screenshot("login_timeout")
    raise

# ✗ Bad: Bare except, no logging
try:
    self.login_page.login(username, password)
except:
    pass  # Swallows exceptions
```

### Test Data

```python
# Use test data files
with open('src/test/python/test_data/login_data.json') as f:
    test_data = json.load(f)

username = test_data['valid_user']
password = test_data['valid_password']
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Issue 1: "Selenium not found"

```bash
# Solution:
pip install selenium
# or
python -m pip install selenium
```

#### Issue 2: "WebDriver manager error"

```bash
# Solution: Reinstall webdriver-manager
pip install --upgrade webdriver-manager

# Clear cache
rm -rf ~/.wdm  # Linux/macOS
rmdir /s %USERPROFILE%\.wdm  # Windows
```

#### Issue 3: "Config file not found"

```bash
# Ensure you're in python directory
cd python

# Verify config file exists
# Windows
dir src\test\python\config\config.properties

# Linux/macOS
ls src/test/python/config/config.properties
```

#### Issue 4: "Port already in use"

```bash
# If application server is running on same port
# Change port in config.properties or stop existing server
```

#### Issue 5: "Import errors in tests"

```bash
# Ensure python directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%CD%  # Windows
```

#### Issue 6: "Maven not found"

```bash
# Install Maven or check PATH
mvn --version

# Or use maven wrapper if available
./mvnw clean test  # Linux/macOS
mvnw.cmd clean test  # Windows
```

#### Issue 7: "Tests fail sporadically"

Solutions:
- Increase explicit waits in `config.properties`
- Check application stability
- Look for race conditions in tests
- Review logs: `cat logs/automation_test_*.log`

#### Issue 8: "Screenshot not captured"

```bash
# Verify screenshot directory exists and has write permissions
ls -la screenshots/  # Linux/macOS
dir screenshots\    # Windows

# Check config setting
# config.properties: on_failure = true
```

### Debug Mode

```bash
# Run with maximum logging
pytest src/test/python/tests -v -s --log-cli-level=DEBUG

# Add breakpoints in Python code
import pdb; pdb.set_trace()

# Or use IDE debugger (VSCode, PyCharm)
```

### Performance Issues

```bash
# Run tests in parallel
pytest src/test/python/tests -n auto

# Profile test execution
pytest src/test/python/tests --durations=10
```

---

## 📚 Additional Resources

### Framework Components

- [BasePage Class](src/test/python/pages/base_page.py) - Common page methods
- [BaseTest Class](src/test/python/base/base_test.py) - Common test methods
- [DriverFactory](src/test/python/utilities/driver_factory.py) - WebDriver creation
- [WaitHelper](src/test/python/utilities/wait_helper.py) - Explicit waits
- [ConfigReader](src/test/python/config/config_reader.py) - Configuration management

### External Documentation

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [PyTest Documentation](https://docs.pytest.org/)
- [Maven Documentation](https://maven.apache.org/guides/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Jenkins Documentation](https://www.jenkins.io/doc/)

---

## 📝 License

This framework is provided as-is for automation testing purposes.

---

## 👥 Support & Contributing

For issues, questions, or contributions:

1. Check existing issues in repository
2. Create detailed bug reports
3. Submit pull requests with improvements
4. Follow existing code style and conventions

---

## 🔄 Framework Updates

Regular updates to the framework:
- Security patches
- Dependency updates
- New features
- Performance improvements

Check the [Changelog](CHANGELOG.md) for details.

---

**Happy Testing! 🚀**

For questions or support, contact the Automation Team.
