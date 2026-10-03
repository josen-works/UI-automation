from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator("[data-test='title']")
        self.items = page.locator("[data-test='inventory-item']")
        self.names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")

    def expect_loaded(self):
        expect(self.header).to_have_text("Your Cart")

    def product_names(self) -> list[str]:
        return [t.strip() for t in self.names.all_inner_texts()]
