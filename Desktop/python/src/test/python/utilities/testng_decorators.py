"""
TestNG-Style Decorators and Annotations for Python
Provides TestNG-like decorators for PyTest tests
"""

import functools
from typing import List, Optional
from utilities.logger_config import LoggerConfig


# Global registry for test metadata
test_registry = {}


def test_method(
    name: Optional[str] = None,
    description: Optional[str] = None,
    priority: int = 5,
    groups: Optional[List[str]] = None,
    enabled: bool = True,
    timeout: int = 0,
    depends_on_methods: Optional[List[str]] = None
):
    """
    TestNG-style @Test decorator for Python
    
    Args:
        name: Test name (defaults to function name)
        description: Test description
        priority: Priority (0-10, where 0 is highest)
        groups: List of test groups/categories
        enabled: Whether test is enabled
        timeout: Timeout in milliseconds (0 = no timeout)
        depends_on_methods: List of methods this test depends on
        
    Example:
        @test_method(
            name="test_login",
            description="Test successful login",
            groups=["login", "smoke"],
            priority=1
        )
        def test_successful_login(self):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerConfig.get_logger(__name__)
            
            if not enabled:
                logger.warning(f"Test {func.__name__} is disabled")
                return None
            
            logger.info(f"Running: {description or func.__name__}")
            return func(*args, **kwargs)
        
        # Store metadata
        wrapper.test_name = name or func.__name__
        wrapper.description = description or func.__doc__
        wrapper.priority = priority
        wrapper.groups = groups or []
        wrapper.enabled = enabled
        wrapper.timeout = timeout
        wrapper.depends_on_methods = depends_on_methods or []
        wrapper.is_test = True
        
        test_registry[func.__name__] = {
            'name': wrapper.test_name,
            'description': wrapper.description,
            'priority': priority,
            'groups': wrapper.groups,
            'enabled': enabled,
            'timeout': timeout,
            'depends_on_methods': depends_on_methods
        }
        
        return wrapper
    
    return decorator


def before_method(alwaysRun: bool = False):
    """
    TestNG-style @BeforeMethod decorator
    Runs before each test method
    
    Args:
        alwaysRun: Run even if test is skipped
        
    Example:
        @before_method()
        def setup_test(self):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerConfig.get_logger(__name__)
            logger.debug(f"Before method: {func.__name__}")
            return func(*args, **kwargs)
        
        wrapper.is_before_method = True
        wrapper.always_run = alwaysRun
        return wrapper
    
    return decorator


def after_method(alwaysRun: bool = False):
    """
    TestNG-style @AfterMethod decorator
    Runs after each test method
    
    Args:
        alwaysRun: Run even if test fails
        
    Example:
        @after_method(alwaysRun=True)
        def cleanup_test(self):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerConfig.get_logger(__name__)
            logger.debug(f"After method: {func.__name__}")
            return func(*args, **kwargs)
        
        wrapper.is_after_method = True
        wrapper.always_run = alwaysRun
        return wrapper
    
    return decorator


def before_class(alwaysRun: bool = False):
    """
    TestNG-style @BeforeClass decorator
    Runs once before all tests in class
    
    Args:
        alwaysRun: Run even if first test is skipped
        
    Example:
        @before_class()
        def setup_class(self):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerConfig.get_logger(__name__)
            logger.debug(f"Before class: {func.__name__}")
            return func(*args, **kwargs)
        
        wrapper.is_before_class = True
        wrapper.always_run = alwaysRun
        return wrapper
    
    return decorator


def after_class(alwaysRun: bool = False):
    """
    TestNG-style @AfterClass decorator
    Runs once after all tests in class complete
    
    Args:
        alwaysRun: Run even if tests fail
        
    Example:
        @after_class()
        def cleanup_class(self):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerConfig.get_logger(__name__)
            logger.debug(f"After class: {func.__name__}")
            return func(*args, **kwargs)
        
        wrapper.is_after_class = True
        wrapper.always_run = alwaysRun
        return wrapper
    
    return decorator


def skip(reason: str = "Skipped"):
    """
    TestNG-style @Skip decorator
    Skips test with reason
    
    Args:
        reason: Reason for skipping
        
    Example:
        @skip("Not ready yet")
        def test_future_feature(self):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerConfig.get_logger(__name__)
            logger.warning(f"Test skipped: {reason}")
            return None
        
        wrapper.skip_reason = reason
        wrapper.is_skipped = True
        return wrapper
    
    return decorator


def data_provider(data_list: List):
    """
    TestNG-style @DataProvider decorator
    Provides test data for parameterized tests
    
    Args:
        data_list: List of test data
        
    Example:
        @data_provider([
            ["user1@example.com", "password1"],
            ["user2@example.com", "password2"]
        ])
        def test_login_with_data(self, username, password):
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper.test_data = data_list
        wrapper.is_data_provider = True
        return wrapper
    
    return decorator


def get_test_registry():
    """Get all registered tests"""
    return test_registry


def get_tests_by_group(group_name: str) -> List[dict]:
    """
    Get all tests in a specific group
    
    Args:
        group_name: Group name
        
    Returns:
        List of tests in group
    """
    return [
        test for test in test_registry.values()
        if group_name in test['groups']
    ]


def get_tests_by_priority(priority: int) -> List[dict]:
    """
    Get tests with specific priority
    
    Args:
        priority: Priority level
        
    Returns:
        List of tests with that priority
    """
    return [
        test for test in test_registry.values()
        if test['priority'] == priority
    ]
