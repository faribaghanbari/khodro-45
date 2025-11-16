"""
Base Page Object Model class
Provides common functionality for all page objects
"""
from playwright.sync_api import Page


class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def goto(self, url: str) -> None:
        """Navigate to a specific URL"""
        self.page.goto(url, wait_until="load", timeout=60000)
    
    def wait_for_element(self, selector: str, timeout: int = 10000) -> None:
        """Wait for element to be visible"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
    
    def wait_for_navigation(self) -> None:
        """Wait for navigation to complete"""
        self.page.wait_for_load_state("load")
        # Wait a bit for dynamic content
        self.page.wait_for_timeout(2000)
    
    def take_screenshot(self, name: str) -> None:
        """Take a screenshot"""
        self.page.screenshot(path=f"test-results/{name}.png", full_page=True)

