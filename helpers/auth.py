"""
Authentication and user lifecycle helper functions
"""
from playwright.sync_api import Page
from helpers.test_data import VALID_CREDENTIALS
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pages.bookstore_page import BookStorePage
import requests
import time
from typing import Dict, Tuple, Optional


def login_to_bookstore(page: Page) -> "BookStorePage":
    """Login to Book Store application"""
    from pages.bookstore_page import BookStorePage
    bookstore_page = BookStorePage(page)
    bookstore_page.navigate()
    bookstore_page.login(VALID_CREDENTIALS["username"], VALID_CREDENTIALS["password"])
    return bookstore_page


def is_authenticated(page: Page) -> bool:
    """Check if user is authenticated"""
    from pages.bookstore_page import BookStorePage
    bookstore_page = BookStorePage(page)
    return bookstore_page.is_logged_in()


def logout_from_bookstore(page: Page) -> None:
    """Logout from Book Store application"""
    from pages.bookstore_page import BookStorePage
    bookstore_page = BookStorePage(page)
    bookstore_page.logout()


def generate_unique_credentials(prefix: str = "auto") -> Tuple[str, str]:
    """
    Generate a unique username/password pair suitable for demoqa Book Store API.
    Password must meet policy (at least 8 chars, uppercase, lowercase, number, special).
    """
    ts = str(int(time.time() * 1000))
    username = f"{prefix}_{ts}"
    password = f"Aa!{ts}"
    return username, password


def create_user_via_api(username: str, password: str) -> Dict:
    """
    Create a new user via DemoQA Account API (bypasses UI captcha on /register).
    Docs: https://demoqa.com/swagger/#/Account
    """
    payload = {"userName": username, "password": password}
    resp = requests.post("https://demoqa.com/Account/v1/User", json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        raise AssertionError(f"User creation failed: {resp.status_code} {resp.text}")
    return resp.json()


def generate_token_via_api(username: str, password: str) -> str:
    """
    Generate an auth token for the created user (useful for debugging or future API calls).
    """
    payload = {"userName": username, "password": password}
    resp = requests.post("https://demoqa.com/Account/v1/GenerateToken", json=payload, timeout=30)
    if resp.status_code != 200:
        raise AssertionError(f"Token generation failed: {resp.status_code} {resp.text}")
    data = resp.json()
    if data.get("status") != "Success":
        raise AssertionError(f"Token generation not successful: {data}")
    return data["token"]

