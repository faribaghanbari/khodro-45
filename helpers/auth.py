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
import time as _time
from typing import Any


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


def login_user_via_api(username: str, password: str) -> Dict[str, Any]:
    """
    Login via DemoQA Account API. Returns response json which may include userId and username.
    """
    payload = {"userName": username, "password": password}
    resp = requests.post("https://demoqa.com/Account/v1/Login", json=payload, timeout=30)
    if resp.status_code != 200:
        raise AssertionError(f"Login via API failed: {resp.status_code} {resp.text}")
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


def generate_token_and_expiry_via_api(username: str, password: str) -> Tuple[str, str]:
    """
    Generate an auth token and expiry for the created user.
    Returns (token, expires) tuple as provided by the DemoQA API.
    """
    payload = {"userName": username, "password": password}
    resp = requests.post("https://demoqa.com/Account/v1/GenerateToken", json=payload, timeout=30)
    if resp.status_code != 200:
        raise AssertionError(f"Token generation failed: {resp.status_code} {resp.text}")
    data = resp.json()
    if data.get("status") != "Success":
        raise AssertionError(f"Token generation not successful: {data}")
    token = data.get("token")
    expires = data.get("expires")
    if not token or not expires:
        raise AssertionError(f"Token or expires missing in response: {data}")
    return token, expires


def generate_token_and_expiry_with_retry(username: str, password: str, attempts: int = 3, backoff_seconds: float = 1.0) -> Tuple[str, str]:
    """
    Same as generate_token_and_expiry_via_api but with simple retries to tolerate transient failures.
    """
    last_error: Optional[Exception] = None
    for i in range(attempts):
        try:
            return generate_token_and_expiry_via_api(username, password)
        except Exception as e:
            last_error = e
            _time.sleep(backoff_seconds)
    raise last_error if last_error else AssertionError("Token generation failed after retries")

