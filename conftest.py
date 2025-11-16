"""
Pytest configuration and fixtures for Playwright E2E tests
"""
import pytest
from playwright.sync_api import Page
from pages.forms_page import FormsPage
from pages.bookstore_page import BookStorePage
from pages.webtables_page import WebTablesPage
from typing import Generator
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments"""
    return {
        **browser_context_args,
        "base_url": "https://demoqa.com",
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


@pytest.fixture
def forms_page(page: Page) -> FormsPage:
    """Fixture providing FormsPage instance"""
    forms_page = FormsPage(page)
    # Navigate to the form page
    forms_page.navigate()
    return forms_page


@pytest.fixture
def bookstore_page(page: Page) -> BookStorePage:
    """Fixture providing BookStorePage instance"""
    bookstore_page = BookStorePage(page)
    # Navigate to the login page
    bookstore_page.navigate()
    return bookstore_page


@pytest.fixture
def webtables_page(page: Page) -> WebTablesPage:
    """Fixture providing WebTablesPage instance"""
    webtables_page = WebTablesPage(page)
    # Navigate to the web tables page
    webtables_page.navigate()
    return webtables_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Convert any skipped tests into failures so that nothing is silently skipped at runtime.
    """
    outcome = yield
    report = outcome.get_result()
    if getattr(report, "skipped", False):
        report.outcome = "failed"
        # Ensure it's not treated as xfail by any plugin
        if hasattr(report, "wasxfail"):
            report.wasxfail = False

