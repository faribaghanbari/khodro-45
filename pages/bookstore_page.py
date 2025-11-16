"""
Page Object Model for Book Store Login
https://demoqa.com/login
"""
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage
from typing import Optional


class BookStorePage(BasePage):
    """Page Object for Book Store Login"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        # Login form elements
        self.username_input: Locator = page.locator("#userName")
        self.password_input: Locator = page.locator("#password")
        self.login_button: Locator = page.locator("#login")
        self.new_user_button: Locator = page.locator("#newUser")
        
        # After login elements
        self.user_name_label: Locator = page.locator("#userName-value")
        self.logout_button: Locator = page.locator('button:has-text("Log out")')
        self.books_table: Locator = page.locator(".rt-table")
        
        # Error messages
        self.error_message: Locator = page.locator("#name")
    
    def navigate(self) -> None:
        """Navigate to Login page"""
        self.goto("/login")
        self.wait_for_navigation()
        # Wait for login form to be ready
        self.username_input.wait_for(state="visible", timeout=10000)
    
    def login(self, username: str, password: str) -> None:
        """Perform login with username and password"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.wait_for_navigation()
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        try:
            self.user_name_label.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False
    
    def get_logged_in_username(self) -> Optional[str]:
        """Get logged in username"""
        try:
            return self.user_name_label.text_content()
        except Exception:
            return None
    
    def logout(self) -> None:
        """Logout from the application"""
        self.logout_button.click()
        self.wait_for_navigation()
    
    def get_error_message(self) -> Optional[str]:
        """Get error message if login fails"""
        try:
            self.error_message.wait_for(state="visible", timeout=3000)
            return self.error_message.text_content()
        except Exception:
            return None
    
    def has_error_message(self) -> bool:
        """Check if error message is displayed"""
        try:
            error_text = self.get_error_message()
            return error_text is not None and len(error_text) > 0
        except Exception:
            return False
    
    def click_new_user(self) -> None:
        """Click on New User button"""
        self.new_user_button.click()
        self.wait_for_navigation()

