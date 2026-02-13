"""
Base Pages Module
Contains base page objects following Page Object Model (POM) pattern
"""

from pages.base_pages.base_page import BasePage
from pages.base_pages.dashboard_page import DashboardPage
from pages.base_pages.login_page import LoginPage

__all__ = ['BasePage', 'DashboardPage', 'LoginPage']
