"""
PyTest Configuration File (conftest.py)
Provides shared fixtures and configurations for all tests
"""

import pytest
from utilities.logger_config import LoggerConfig
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def pytest_configure(config):
    """
    PyTest configuration hook
    Called after command line options have been parsed
    """
    LoggerConfig.get_logger("pytest", log_dir="./logs")


@pytest.fixture(scope="session")
def test_session():
    """
    Session-level fixture
    Runs once per test session
    """
    logger = LoggerConfig.get_logger(__name__)
    logger.info("=" * 70)
    logger.info("TEST SESSION STARTED".center(70))
    logger.info("=" * 70)
    
    yield
    
    logger.info("=" * 70)
    logger.info("TEST SESSION COMPLETED".center(70))
    logger.info("=" * 70)


@pytest.fixture
def test_case():
    """
    Function-level fixture
    Available to all test functions
    """
    yield


def pytest_runtest_makereport(item, call):
    """
    Hook for test result collection
    Called after test execution
    """
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed
            logger = LoggerConfig.get_logger("pytest")
            logger.error(f"FAILED: {item.name}")
        else:
            # Test passed
            logger = LoggerConfig.get_logger("pytest")
            logger.info(f"PASSED: {item.name}")


def pytest_collection_modifyitems(config, items):
    """
    Hook for modifying test collection
    Add markers for test organization
    """
    for item in items:
        # Add marker based on test file
        if "test_login" in item.nodeid:
            item.add_marker(pytest.mark.login)


# ==================== Pytest Configuration Options ====================
"""
To run tests with specific configurations:

1. Run all tests:
   pytest
   
2. Run with verbose output:
   pytest -v
   
3. Run specific test file:
   pytest src/test/python/tests/test_login.py
   
4. Run specific test:
   pytest src/test/python/tests/test_login.py::TestLogin::test_successful_login
   
5. Run with markers:
   pytest -m login
   
6. Run with specific browser:
   pytest --browser=firefox
   
7. Run in parallel (requires pytest-xdist):
   pytest -n auto
   
8. Run with HTML report (requires pytest-html):
   pytest --html=reports/report.html --self-contained-html
   
9. Run with allure report (requires allure-pytest):
   pytest --alluredir=./allure-results
   
10. Run with coverage (requires pytest-cov):
    pytest --cov=src/test/python --cov-report=html
"""
