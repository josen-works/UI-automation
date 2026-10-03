import re

import pytest
from playwright.sync_api import expect

PRODUCT = "Sauce Labs Fleece Jacket"


@pytest.mark.smoke
def test_add_product_to_cart(logged_in, cart_page):
    """Task 2: select a product, add it to the cart and verify it is in the cart."""
    logged_in.add_to_cart(PRODUCT)
    expect(logged_in.cart_badge).to_have_text("1")

    logged_in.open_cart()
    cart_page.expect_loaded()
    assert cart_page.product_names() == [PRODUCT]


def test_add_product_from_detail_page(logged_in, cart_page, page):
    logged_in.open_product(PRODUCT)
    expect(page).to_have_url(re.compile(r"inventory-item\.html"))
    expect(page.locator(".inventory_details_name")).to_have_text(PRODUCT)
    page.get_by_role("button", name="Add to cart").click()
    logged_in.open_cart()
    assert PRODUCT in cart_page.product_names()


def test_remove_product_from_cart(logged_in, cart_page):
    logged_in.add_to_cart(PRODUCT)
    logged_in.open_cart()
    assert cart_page.product_names() == [PRODUCT]
    cart_page.items.get_by_role("button", name="Remove").click()
    expect(cart_page.items).to_have_count(0)


def test_multiple_products_badge_count(logged_in, cart_page):
    names = ["Sauce Labs Backpack", "Sauce Labs Bike Light", PRODUCT]
    for n in names:
        logged_in.add_to_cart(n)
    expect(logged_in.cart_badge).to_have_text(str(len(names)))
    logged_in.open_cart()
    assert sorted(cart_page.product_names()) == sorted(names)


def test_checkout_end_to_end(logged_in, cart_page, checkout_page):
    logged_in.add_to_cart(PRODUCT)
    logged_in.open_cart()
    cart_page.checkout_button.click()
    checkout_page.fill_details("Test", "User", "12345")
    checkout_page.finish()
