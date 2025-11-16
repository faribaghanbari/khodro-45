"""
End-to-end: Register a new user via API, then login via UI with same credentials.
Page: https://demoqa.com/register
API:  https://demoqa.com/swagger/#/Account
"""
import pytest
from playwright.sync_api import Page
from helpers.auth import generate_unique_credentials, create_user_via_api
from pages.bookstore_page import BookStorePage


@pytest.mark.bookstore
def test_register_user_via_api_then_login_via_ui(page: Page) -> None:
    # Arrange: create new user with API to bypass captcha on UI register page
    username, password = generate_unique_credentials(prefix="e2e")
    create_user_via_api(username, password)

    # Act: login via UI with the created credentials
    bookstore = BookStorePage(page)
    bookstore.navigate()
    bookstore.login(username, password)

    # Assert: logged in username is visible and matches
    assert bookstore.is_logged_in(), "User should be logged in after valid credentials"
    assert bookstore.get_logged_in_username() == username

