import pytest

from utils.config import SORT_OPTIONS


@pytest.mark.sorting
@pytest.mark.parametrize("option", list(SORT_OPTIONS))
def test_sort_option_orders_products(logged_in, option):
    """Task 3: for each sort option, the displayed list must match the expected order.

    The page's list is read into a Python list, sorted locally, and compared.
    """
    key, reverse = SORT_OPTIONS[option]
    logged_in.sort_by(option)

    if key == "name":
        actual = logged_in.product_names()
    else:
        actual = logged_in.product_prices()

    assert actual == sorted(actual, reverse=reverse), f"List not ordered for '{option}': {actual}"


@pytest.mark.sorting
@pytest.mark.parametrize("option", list(SORT_OPTIONS))
def test_sort_keeps_same_products(logged_in, option):
    """Sorting must reorder the list, never add or drop products."""
    before = sorted(logged_in.product_names())
    logged_in.sort_by(option)
    assert sorted(logged_in.product_names()) == before
