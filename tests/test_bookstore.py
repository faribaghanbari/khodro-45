"""
Book Store - Login Authentication Tests
"""
import pytest
from pages.bookstore_page import BookStorePage
from helpers.test_data import VALID_CREDENTIALS, INVALID_CREDENTIALS
from helpers.auth import login_to_bookstore


# Skip all login tests if credentials are not configured
skip_if_no_credentials = (
    VALID_CREDENTIALS["username"] == "your_username_here" or
    VALID_CREDENTIALS["password"] == "your_password_here"
)


@pytest.mark.bookstore
@pytest.mark.skipif(skip_if_no_credentials, reason="⚠️  SKIPPED: Please configure TEST_USERNAME and TEST_PASSWORD environment variables or update helpers/test_data.py with your demoqa.com credentials. Visit https://demoqa.com/login and click 'New User' to create an account.")
class TestBookStoreLogin:
    """Test suite for Book Store Login"""
    
    def test_successfully_login_with_valid_credentials(self, bookstore_page: BookStorePage):
        """Test successful login with valid credentials"""
        bookstore_page.login(VALID_CREDENTIALS["username"], VALID_CREDENTIALS["password"])
        
        # Verify successful login
        assert bookstore_page.is_logged_in() is True
        
        # Verify username is displayed
        username = bookstore_page.get_logged_in_username()
        assert username == VALID_CREDENTIALS["username"]
        
        # Verify books table is visible
        assert bookstore_page.books_table.is_visible()
    
    def test_fail_login_with_invalid_credentials(self, bookstore_page: BookStorePage):
        """Test failed login with invalid credentials"""
        bookstore_page.login(INVALID_CREDENTIALS["username"], INVALID_CREDENTIALS["password"])
        
        # Verify login failed - error message should appear
        assert bookstore_page.has_error_message() is True
        
        # Verify user is not logged in
        assert bookstore_page.is_logged_in() is False
    
    def test_fail_login_with_empty_username(self, bookstore_page: BookStorePage):
        """Test failed login with empty username"""
        bookstore_page.login("", VALID_CREDENTIALS["password"])
        
        # Verify login failed
        assert bookstore_page.is_logged_in() is False
    
    def test_fail_login_with_empty_password(self, bookstore_page: BookStorePage):
        """Test failed login with empty password"""
        bookstore_page.login(VALID_CREDENTIALS["username"], "")
        
        # Verify login failed
        assert bookstore_page.is_logged_in() is False
    
    def test_fail_login_with_wrong_password(self, bookstore_page: BookStorePage):
        """Test failed login with wrong password"""
        bookstore_page.login(VALID_CREDENTIALS["username"], "WrongPassword123")
        
        # Verify login failed
        assert bookstore_page.has_error_message() is True
        assert bookstore_page.is_logged_in() is False
    
    def test_fail_login_with_wrong_username(self, bookstore_page: BookStorePage):
        """Test failed login with wrong username"""
        bookstore_page.login("nonexistentuser", VALID_CREDENTIALS["password"])
        
        # Verify login failed
        assert bookstore_page.has_error_message() is True
        assert bookstore_page.is_logged_in() is False
    
    def test_display_error_message_on_failed_login(self, bookstore_page: BookStorePage):
        """Test error message display on failed login"""
        bookstore_page.login(INVALID_CREDENTIALS["username"], INVALID_CREDENTIALS["password"])
        
        error_message = bookstore_page.get_error_message()
        assert error_message is not None
        assert len(error_message) > 0
    
    def test_logout_successfully_after_login(self, bookstore_page: BookStorePage):
        """Test logout successfully after login"""
        # Login first
        bookstore_page.login(VALID_CREDENTIALS["username"], VALID_CREDENTIALS["password"])
        
        # Verify logged in
        assert bookstore_page.is_logged_in() is True
        
        # Logout
        bookstore_page.logout()
        
        # Verify logged out - should be back on login page
        assert bookstore_page.username_input.is_visible()
        assert bookstore_page.password_input.is_visible()
        assert bookstore_page.login_button.is_visible()
    
    def test_navigate_to_new_user_registration_page(self, bookstore_page: BookStorePage, page):
        """Test navigation to new user registration page"""
        bookstore_page.click_new_user()
        
        # Verify navigation to registration page
        assert "register" in page.url.lower()
    
    def test_use_auth_helper_function_for_login(self, page):
        """Test using auth helper function for login"""
        logged_in_page = login_to_bookstore(page)
        
        assert logged_in_page.is_logged_in() is True

