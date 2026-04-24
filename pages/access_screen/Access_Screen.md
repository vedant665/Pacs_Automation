# Access Screen Module – Complete Documentation

This document covers the **Access Screen** module of the PACS Automation framework. The module provides page objects, test data generators, and a pytest‑based test suite for the **Entity Group Definition**, **Role Creation**, and **User Creation** screens.

---

## 1. Overview

The `access_screen` folder is a self‑contained test module that:

- Automates creation of Entity Groups, Roles, and Users via Selenium.
- Generates random test data for positive scenarios.
- Provides negative (validation) and dropdown tests.
- Produces an Excel report with test results and failure screenshots.

All code resides under `pages/access_screen/`.

---

## 2. Directory Structure

```
pages/access_screen/
├── Access_screens/                 # Page Object Modules
│   ├── entity_group.py             → create_entity_group()
│   ├── role_creation.py            → create_role()
│   ├── user_creation.py            → create_user()
│   ├── main_access.py              → standalone runner (manual execution)
│   └── docs/                       → Markdown docs for each module
├── access_screens_test_cases/      # pytest test suite
│   ├── conftest.py                 → fixtures, hooks, Excel report
│   ├── access_screen_test_runner.py→ CLI test runner (supports filtering)
│   ├── user_creation_test.py       → test cases for User Creation
│   └── docs/                       → test‑related docs
├── data/                           # Test data generators
│   ├── access_data.py              → core random data + pre‑gen data
│   ├── access_test_data.py         → pytest‑specific data (duplicates, weak passwords)
│   └── __init__.py                 → empty
├── reports/                        → Generated Excel reports
├── screenshots/                    → Failure screenshots (PNG)
└── report_config.py                → Report title, descriptions, categories
```

---

## 3. Page Object Modules (`Access_screens/`)

These modules contain the low‑level automation functions for each screen.

### 3.1 `entity_group.py`

**Function:** `create_entity_group(driver, wait, group_name, level)`

- Clicks ADD, fills “Entity Group Name” and “Level”, submits.
- Checks SweetAlert/toast success.
- Searches for the group in the table and verifies it exists.

**Key helpers:** `_fill_field()`, `_check_result()`, `_verify_in_table()` (internal).

### 3.2 `role_creation.py`

**Function:** `create_role(driver, wait, role_name, entity_group)`

- Clicks ADD, fills Role Name (by `formcontrolname`), selects Entity Type from dropdown.
- Submits and checks result.
- Verifies role in table using `common.table_helpers.verify_in_table()`.

**Key helper:** `_fill_dropdown()` for single‑select Material dropdowns.

### 3.3 `user_creation.py`

**Function:** `create_user(driver, wait, username, email, first_name, last_name, password, user_types, role, entity)`

- Fills five text inputs (`_fill_input`).
- Handles multi‑select (**User Type**, **Entity**) with `_fill_multi_dropdown`.
- Handles searchable single‑select (**Role**) with `_fill_search_dropdown`.
- Submits, checks result, and verifies in table with date column validation.

### 3.4 `main_access.py`

Standalone script that:

- Builds a Chrome driver (maximized, with WebDriver Manager).
- Logs in using credentials from `config.py`.
- Navigates to **User Creation Screen** (by default – other screens are commented).
- Calls `create_user()` with pre‑generated data from `access_data.py`.
- Closes the driver.

**Purpose:** Quick manual testing or demonstration; not used by pytest.

---

## 4. Pytest Test Suite (`access_screens_test_cases/`)

### 4.1 `conftest.py` – Fixtures and Hooks

**Overrides** `SCREENSHOT_DIR` and `REPORT_DIR` to point inside `access_screen/`.

**Fixtures:**

- `driver` (session‑scoped) – launches browser once.
- `logged_in_driver` (session‑scoped) – performs login once and shares the authenticated driver.
- `on_user_creation` (function‑scoped) – navigates to User Creation screen before each test, cleans up leftover modals/toasts.
- `user_creation_screen` (class‑scoped) – navigates once per test class (used by positive tests).

**Hooks:**

- `pytest_runtest_makereport` – captures test result (PASS/FAIL), saves screenshot on failure.
- `pytest_sessionfinish` – generates an Excel report via `common.report_generator.generate_report()`.

**Report configuration** is imported from `report_config.py`.

### 4.2 `access_screen_test_runner.py`

CLI wrapper for `pytest`. Supports:

- Run all tests: `python runner.py`
- Filter by keyword: `--positive`, `--validation`, `--dropdown`, `--user-creation`
- Pass custom pytest arguments (e.g., `--html=report.html`)

Internally calls `pytest.main()` with the test folder path and flags `-v`, `--tb=short`, `-s`.

### 4.3 `user_creation_test.py`

Contains **8 test methods** in three classes:

| Class                         | Tests                                                                 |
|-------------------------------|-----------------------------------------------------------------------|
| `TestUserCreationPositive`    | Happy path, single user type, DCB role (3 tests).                     |
| `TestUserCreationValidation`  | Blank submit, duplicate username, duplicate email, weak password (4). |
| `TestUserCreationDropdown`    | Multi‑select User Type – verifies chip count (1 test).                |

All tests reuse helpers from `user_creation.py` and `common.table_helpers`.

### 4.4 `report_config.py`

Defines:

- `REPORT_TITLE = "Access Screen – User Creation"`
- `FILENAME_PREFIX = "UserCreation"`
- `UC_DESCRIPTIONS` – mapping of test function names to human‑readable questions (used in the “Test Guide” sheet of the Excel report).
- `UC_CATEGORIES` – maps test class names to category labels (“Positive Tests”, “Validation Tests”, “Dropdown Tests”).

---

## 5. Test Data (`data/`)

### 5.1 `access_data.py`

**Core random generators** used by both the standalone runner and pytest:

- `random_entity_group_data()` – returns `{"group_name": ..., "level": ...}`
- `random_role_creation_data()` – returns `{"role_name": ..., "entity_group": ...}`
- `random_user_creation_data()` – returns a complete user dictionary, respecting role‑entity pairing (DCB → `dcb1`, PACS → random from large list).

**Pre‑generated variables** (computed once at import):
- `entity_group_data`
- `role_creation_data`
- `user_creation_data`

These are used by `main_access.py`.

### 5.2 `access_test_data.py`

**Pytest‑specific constants**:

- `DUPLICATE_USERNAME`, `DUPLICATE_EMAIL` – existing records for negative tests.
- `VALID_PASSWORD` – meets complexity rules.
- `WEAK_PASSWORDS` – dict of five weak password examples.
- `BLANK_VALUES` – empty strings for each field.

**Random generators for positive tests** (wrappers around `access_data.random_user_creation_data()`):

- `random_user_data(**overrides)` – full random user.
- `random_user_data_single_type(**overrides)` – only one user type.
- `random_user_data_dcb(**overrides)` – forces role=DCB, entity=dcb1.

These ensure that test cases get fresh unique data each run.

### 5.3 `__init__.py`

Empty – marks `data` as a Python package.

---

## 6. Common Helpers (`common/table_helpers.py`)

**`verify_in_table(driver, wait, search_value, column_class=None, check_date=False, date_column="created_date_time", date_format="%d-%b-%Y")`**

- Clicks search button, types `search_value` into `#erpSearchInput` (or similar).
- Checks for “No results” row – raises exception if found.
- Searches for value in a specific column (if `column_class` given) or any cell.
- Optionally verifies a date column matches today’s date.
- Clears search.

This helper is reused by `user_creation.py` and `role_creation.py`.

---

## 7. Execution Flow

### 7.1 Standalone Runner (`main_access.py`)

```
build_driver() → login() → navigate_to("Access", "User Creation Screen") → create_user()
```

### 7.2 Pytest Test Suite

1. `conftest.py` sets up session‑scoped driver, logs in once.
2. For each test class:
   - Positive tests: `user_creation_screen` fixture navigates once to the screen.
   - Validation / Dropdown tests: `on_user_creation` fixture navigates before each test.
3. Test methods fill forms (using random data from `access_test_data.py`), submit, and assert success.
4. On failure: screenshot saved to `screenshots/`.
5. After all tests: Excel report generated in `reports/` via `common.report_generator`.

---

## 8. How to Run Tests

### 8.1 Run all tests

```bash
cd pages/access_screen/access_screens_test_cases
python access_screen_test_runner.py
```

### 8.2 Run only positive tests

```bash
python access_screen_test_runner.py --positive
```

### 8.3 Run only validation tests

```bash
python access_screen_test_runner.py --validation
```

### 8.4 Run only dropdown tests

```bash
python access_screen_test_runner.py --dropdown
```

### 8.5 Run only user creation tests

```bash
python access_screen_test_runner.py --user-creation
```

### 8.6 Run a single test by name

```bash
pytest user_creation_test.py -k "test_uc_p01_happy_path_create_and_verify" -v
```

### 8.7 Run with custom pytest arguments

```bash
python access_screen_test_runner.py -v --tb=line --html=myreport.html
```

---

## 9. Reports and Screenshots

- **Excel report** – saved in `reports/UserCreation_TestReport_YYYYMMDD_HHMMSS.xlsx`.  
  Contains a summary sheet, test results, and a “Test Guide” sheet with descriptions from `report_config.py`.
- **Failure screenshots** – saved in `screenshots/FAILED_<testname>_<timestamp>.png`.  
  Automatically captured by `conftest.py` hook.

---

## 10. Configuration Dependencies

The module relies on the project‑level `config.py` which must define:

```python
MODULE_LOGIN_URL = "https://..."
PACS_EMAIL = "your_email"
PACS_PASSWORD = "your_password"
PACS_FACILITY = "facility_name"
```

Also uses `common.nav_section.navigate_to()` and `common.auth_helper.AuthSection` for login.

---

## 11. Notes and Tips

- All dropdown interactions use **native clicks** on the trigger element (JavaScript click does not open Angular Material selects).
- The `_fill_multi_dropdown` closes the panel by clicking `<body>` after selecting all options.
- The search input in `table_helpers` uses `#erpSearchInput` as primary selector – adjust if your app uses a different ID.
- The DCB role only works with entity `dcb1`; PACS works with a long list – the random generator respects this.
- Weak password test (`test_uc_v04_weak_password_rejected`) does not expect a specific error message; it only checks that a duplicate‑user error (which would indicate the weak password was accepted) does **not** appear. This makes the test robust across different backend implementations.

---

## 12. Extending the Module

To add a new screen (e.g., “Screen Api Link”):

1. Create a page object in `Access_screens/` (e.g., `screen_api_link.py`) with a `create_screen_api_link()` function.
2. Add test data generators in `data/access_data.py` and `access_test_data.py`.
3. Write test cases in `access_screens_test_cases/` (e.g., `screen_api_link_test.py`).
4. Update `report_config.py` with descriptions and categories.
5. Add navigation calls in `main_access.py` (uncomment) or in test fixtures.

---

## 13. Troubleshooting

| Issue | Possible solution |
|-------|-------------------|
| Element not found / timeout | Increase `WebDriverWait` timeout (set in `conftest.py`). |
| Dropdown does not open | Use native `click()` instead of JS – already done. |
| SweetAlert success not detected | The toast/popup may have a different CSS class; update `_check_result()` or `_wait_for_swal_success()`. |
| Table verification fails | Check the column class (`cdk-column-<name>`). In `user_creation` we use `name`; adjust if needed. |
| Excel report not generated | Ensure `common.report_generator` exists and `REPORT_DIR` is writable. |

---

*Documentation generated for `pages/access_screen` – covers all files as of April 2026.*
```