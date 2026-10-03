import pytest
from playwright.sync_api import expect

from utils.config import LOCKED_OUT_USER, PASSWORD, STANDARD_USER


@pytest.mark.smoke
def test_login_shows_products_header(login_page, inventory_page):
    """Task 1: log in and assert the 'Products' header is visible."""
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.expect_loaded()


@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, message",
    [
        (STANDARD_USER, "wrong_password", "Username and password do not match"),
        ("not_a_user", PASSWORD, "Username and password do not match"),
        ("", "", "Username is required"),
        (STANDARD_USER, "", "Password is required"),
        (LOCKED_OUT_USER, PASSWORD, "this user has been locked out"),
    ],
)
def test_invalid_login_shows_error(login_page, username, password, message):
    login_page.login(username, password)
    expect(login_page.error).to_contain_text(message)
