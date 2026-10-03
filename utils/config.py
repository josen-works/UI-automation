"""Central test data: URL and credentials for https://www.saucedemo.com (public demo site)."""

BASE_URL = "https://www.saucedemo.com"

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PASSWORD = "secret_sauce"

# Sort option (dropdown label) -> (key extracting the compared value, reverse?)
SORT_OPTIONS = {
    "Name (A to Z)": ("name", False),
    "Name (Z to A)": ("name", True),
    "Price (low to high)": ("price", False),
    "Price (high to low)": ("price", True),
}
