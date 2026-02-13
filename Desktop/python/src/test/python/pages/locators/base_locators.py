"""
Base Locators Module
Abstract base class for page locators
Provides structure for creating locator classes for other pages
"""

from abc import ABC


class BaseLocators(ABC):
    """
    Abstract base class for page locators.
    All page-specific locator classes should inherit from this.
    
    Benefits:
    - Centralized locator management
    - Easy to maintain and update selectors
    - Separate from action logic
    - Easy to switch between locator strategies
    """
    
    @classmethod
    def get_all_locators(cls):
        """
        Get all locators for this page as dictionary
        
        Returns:
            dict: Dictionary of all locator attributes
        """
        locators = {}
        for attr_name in dir(cls):
            attr_value = getattr(cls, attr_name)
            # Include only tuples (locators) and not private attributes
            if isinstance(attr_value, tuple) and len(attr_value) == 2 and \
               not attr_name.startswith('_'):
                locators[attr_name] = attr_value
        return locators
    
    @classmethod
    def get_locator_count(cls):
        """
        Get count of locators defined in this class
        
        Returns:
            int: Number of locators
        """
        return len(cls.get_all_locators())
