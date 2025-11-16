"""
Authentication helper functions
"""
from playwright.sync_api import Page
from pages.bookstore_page import BookStorePage
from helpers.test_data import VALID_CREDENTIALS


def login_to_bookstore(page: Page) -> BookStorePage:
    """Login to Book Store application"""
    bookstore_page = BookStorePage(page)
    bookstore_page.navigate()
    bookstore_page.login(VALID_CREDENTIALS["username"], VALID_CREDENTIALS["password"])
    return bookstore_page


def is_authenticated(page: Page) -> bool:
    """Check if user is authenticated"""
    bookstore_page = BookStorePage(page)
    return bookstore_page.is_logged_in()


def logout_from_bookstore(page: Page) -> None:
    """Logout from Book Store application"""
    bookstore_page = BookStorePage(page)
    bookstore_page.logout()

