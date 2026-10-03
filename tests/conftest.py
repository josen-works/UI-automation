import base64
from pathlib import Path

import pytest
from playwright.sync_api import Page

try:
    import pytest_html
except ImportError:  # report plugin is optional
    pytest_html = None

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import PASSWORD, STANDARD_USER

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"


def pytest_configure(config):
    """Keep the HTML report inside the project, wherever pytest is launched from."""
    html = getattr(config.option, "htmlpath", None)
    if html and not Path(html).is_absolute():
        config.option.htmlpath = str(PROJECT_ROOT / html)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def logged_in(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """Open the site, log in as the standard user and land on the Products page."""
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.expect_loaded()
    return inventory_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, save a screenshot and embed it in the HTML report."""
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page")
    if report.when == "call" and report.failed and page is not None:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        safe = item.nodeid.replace("/", "_").replace("::", "__").replace("[", "_").replace("]", "")
        png = page.screenshot(path=str(SCREENSHOT_DIR / f"{safe}.png"))
        if pytest_html is not None:
            report.extras = getattr(report, "extras", []) + [
                pytest_html.extras.png(base64.b64encode(png).decode(), name="screenshot")]
