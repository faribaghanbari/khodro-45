"""
Base Page Object Model class
Provides common functionality for all page objects
"""
from playwright.sync_api import Page
from playwright._impl._errors import TimeoutError as PlaywrightTimeoutError


class BasePage:
    """Base page class with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def goto(self, url: str, retries: int = 2) -> None:
        """Navigate to a specific URL with small retry and faster readiness threshold."""
        last_error = None
        for attempt in range(retries + 1):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=90000)
                return
            except PlaywrightTimeoutError as e:
                last_error = e
                # brief pause before retry
                self.page.wait_for_timeout(1000)
        # re-raise last error if all retries failed
        raise last_error
    
    def wait_for_element(self, selector: str, timeout: int = 10000) -> None:
        """Wait for element to be visible"""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
    
    def wait_for_navigation(self) -> None:
        """Wait for navigation to complete with lighter readiness."""
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(300)
    
    def take_screenshot(self, name: str) -> None:
        """Take a screenshot"""
        self.page.screenshot(path=f"test-results/{name}.png", full_page=True)

