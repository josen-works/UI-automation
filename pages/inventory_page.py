from playwright.sync_api import Page, expect


class InventoryPage:
    """The 'Products' page shown after login."""

    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator("[data-test='title']")
        self.items = page.locator("[data-test='inventory-item']")
        self.names = page.locator("[data-test='inventory-item-name']")
        self.prices = page.locator("[data-test='inventory-item-price']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    def expect_loaded(self):
        expect(self.header).to_be_visible()
        expect(self.header).to_have_text("Products")

    def _item(self, product_name: str):
        return self.items.filter(has_text=product_name)

    def add_to_cart(self, product_name: str):
        self._item(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str):
        self._item(product_name).get_by_role("button", name="Remove").click()

    def open_product(self, product_name: str):
        self.names.filter(has_text=product_name).click()

    def sort_by(self, option_label: str):
        self.sort_dropdown.select_option(label=option_label)

    def product_names(self) -> list[str]:
        return [t.strip() for t in self.names.all_inner_texts()]

    def product_prices(self) -> list[float]:
        return [float(t.strip().lstrip("$")) for t in self.prices.all_inner_texts()]

    def open_cart(self):
        self.cart_link.click()
