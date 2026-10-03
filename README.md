# SauceDemo UI Automation

A small UI test-automation project for <https://www.saucedemo.com>, built with
**Python, Pytest and Playwright** using the **Page Object Model**.

## What is covered

| Test file | Scenario |
|-----------|----------|
| `tests/test_login.py` | Log in with valid credentials and assert the **Products** header is visible; parametrized negative logins (wrong password, empty fields, locked-out user) |
| `tests/test_cart_flow.py` | Log in, pick **Sauce Labs Fleece Jacket**, add it to the cart and verify it appears there; plus remove-from-cart, multi-item badge count, add from detail page and a full checkout |
| `tests/test_sorting.py` | `@pytest.mark.parametrize` over the four sort options (A–Z, Z–A, price low–high, high–low). Product names/prices are read into a list, sorted in Python and compared to what the site displays |

> SauceDemo has no search box, so the parametrized test uses the sort options instead.

## Project structure

```text
saucedemo-ui-automation/
├── pages/            # Page objects (login, inventory, cart, checkout)
├── tests/            # Pytest tests + conftest.py (fixtures, failure screenshots)
├── utils/config.py   # URL, credentials, sort-option data
├── pytest.ini        # Markers and HTML report settings
└── requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium          # add firefox / webkit to run other browsers
```

## Run

```bash
pytest                              # all tests, headless
pytest --headed --slowmo 300        # watch the browser
pytest -m smoke                     # core login + cart only
pytest -m sorting                   # sort tests only
pytest -m negative                  # invalid-login tests only
pytest --browser firefox            # other browsers
```

An HTML report is written to `reports/report.html`. When a test fails, a
screenshot of the page is saved to `screenshots/` and embedded in the report.
Both folders are created inside the project, wherever you run `pytest` from.

## Test credentials

SauceDemo publishes these on its login page: `standard_user` / `secret_sauce`.
