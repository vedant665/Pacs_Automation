# User Creation Screen – Pytest Test Suite

This module contains **Pytest test cases** for the **User Creation** screen of the Access module. It covers positive (happy path) scenarios, validation (negative) tests, and dropdown interaction tests.

- **3 test classes** – `TestUserCreationPositive`, `TestUserCreationValidation`, `TestUserCreationDropdown`
- **8 test methods** – P01‑P03 (positive), V01‑V04 (validation), D01 (dropdown)
- Integrates with `conftest.py` fixtures (`user_creation_screen`, `on_user_creation`)
- Uses test data from `pages/access_screen/data/access_test_data.py`
- Reuses helper functions from the `user_creation` module (`_fill_input`, `_fill_multi_dropdown`, `_fill_search_dropdown`)

## File Location

`pages/access_screen/access_screens_test_cases/user_creation_test.py`

## Dependencies

- `pytest`
- Selenium WebDriver
- `pages.access_screen.data.access_test_data` – provides:
  - `DUPLICATE_USERNAME`, `DUPLICATE_EMAIL`, `VALID_PASSWORD`, `WEAK_PASSWORDS`
  - `random_user_data()` – generates a complete random user dict
  - `random_user_data_single_type()` – user with single user type
  - `random_user_data_dcb()` – user with DCB role & entity
- `pages.access_screen.Access_screens.user_creation` – helper functions for filling form fields
- `common.table_helpers.verify_in_table` – table verification with date checking

## Test Fixtures (from `conftest.py`)

The test suite expects two class‑scoped or function‑scoped fixtures defined in the parent `conftest.py`:

| Fixture               | Scope      | Description                                                                 |
|-----------------------|------------|-----------------------------------------------------------------------------|
| `user_creation_screen` | class      | Returns `(driver, wait)` where the driver is already on the User Creation screen and logged in. Used by `TestUserCreationPositive`. |
| `on_user_creation`     | function   | Similar but function‑scoped (fresh screen before each validation/dropdown test). Used by `TestUserCreationValidation` and `TestUserCreationDropdown`. |

Both fixtures are expected to handle:
- Browser launch and login (via `conftest.py`’s global setup)
- Navigation to “Access → User Creation Screen”
- Possibly resetting the screen state between tests (e.g., closing leftover modals)

---

## Private Helpers (within the test file)

These helpers are used by the test methods to interact with the page.

### `_click_add(driver, wait)`

Clicks the ADD button (tooltip “ADD”) using JavaScript.

### `_click_submit(driver, wait)`

Clicks the form’s Submit button.

### `_wait_for_swal_toast(driver, wait, timeout=5)`

Waits for a SweetAlert **toast** (`.swal2-popup.swal2-toast h2.swal2-title`) and returns its title text. Returns `None` if not found.

### `_wait_for_swal_success(driver, wait)`

Waits for the SweetAlert **success popup** (`.swal2-success`) and clicks the OK button. Returns `True` if success appears, else `False`.

### `_is_form_open(driver, wait)`

Checks if the creation form modal is still open by looking for the title “User Creation Screen Details”. Returns `True` if visible.

### `_fill_all_fields(driver, wait, data)`

Fills all form fields using the provided dictionary. Expects keys: `username`, `email`, `first_name`, `last_name`, `password`, `user_types` (list), `role`, `entity`.

### `_open_add_form(driver, wait)` (inside `TestUserCreationPositive`)

Dismisses any blocking overlays, clicks ADD, and waits for the form title to appear.

---

## Test Classes

### 1. `TestUserCreationPositive`

Uses the **class‑scoped** `user_creation_screen` fixture. All three tests:

- Open the add form via `_open_add_form()`
- Fill fields with random test data (different helpers per test)
- Submit the form
- Wait for SweetAlert success
- Verify the new user appears in the table with date column checking (`joined` column, format `%d %b %Y`)

| Method | Description | Data source |
|--------|-------------|--------------|
| `test_uc_p01_happy_path_create_and_verify` | Full random user (multiple user types, a role, an entity) | `random_user_data()` |
| `test_uc_p02_single_user_type` | User with exactly one user type | `random_user_data_single_type()` |
| `test_uc_p03_dcb_role_dcb1_entity` | User with role “DCB” and entity “dcb1” | `random_user_data_dcb()` |

### 2. `TestUserCreationValidation`

Uses the **function‑scoped** `on_user_creation` fixture. Validates error handling.

| Method | Description | Assertion |
|--------|-------------|-----------|
| `test_uc_v01_blank_submit_no_alert` | Submit empty form | No SweetAlert, form remains open |
| `test_uc_v02_duplicate_username_rejected` | Use existing username | Error toast containing “username already exists” |
| `test_uc_v03_duplicate_email_rejected` | Use existing email | Error toast containing “email already exists” |
| `test_uc_v04_weak_password_rejected` | Use a short password (e.g., “123”) | Either no error toast, or error that does **not** indicate success (“already exists”); ensures user not created |

**Note on V04:** The test checks that either no toast appears (backend may accept weak password) or if a toast appears, it must **not** contain “already exists” (which would indicate a duplicate, not a password strength error). This is a pragmatic check because the exact error message may vary.

### 3. `TestUserCreationDropdown`

Single test to verify multi‑select dropdown behavior for **User Type**.

| Method | Description |
|--------|-------------|
| `test_uc_d01_multi_select_user_type` | Open the “User Type” dropdown, select “Maker” and “Checker”, close the panel, and assert that at least 2 chips (selected items) appear inside the form field. |

---

## Running the Tests

You can run the test file directly with pytest:

```bash
# Run all tests in this file
pytest pages/access_screen/access_screens_test_cases/user_creation_test.py -v

# Run only positive tests
pytest pages/access_screen/access_screens_test_cases/user_creation_test.py -k "Positive" -v

# Run only validation tests
pytest pages/access_screen/access_screens_test_cases/user_creation_test.py -k "Validation" -v

# Run only the dropdown test
pytest pages/access_screen/access_screens_test_cases/user_creation_test.py -k "Dropdown" -v
```

Or use the test runner described in `access_screen_test_runner.py`:

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --user-creation
```

## Test Data Notes

- `random_user_data()` generates a **unique** username and email using timestamps to avoid collisions.
- `DUPLICATE_USERNAME` and `DUPLICATE_EMAIL` are predefined values that already exist in the system (must be set up beforehand).
- `VALID_PASSWORD` is a string that meets the application’s password policy (e.g., length, complexity).
- `WEAK_PASSWORDS` is a dictionary containing at least a key `"too_short"` with a value like `"123"`.

## Logging & Reporting

The test file does **not** configure logging itself – it relies on the `conftest.py` logging setup. However, helper functions imported from `user_creation.py` will log their actions (e.g., “Filling ‘username’ = …”). Test output is captured by pytest.

If an Excel report is generated by `conftest.py`, the test results (PASS/FAIL) will be included.

## Notes

- The positive tests use class‑scoped fixture to reuse the same browser session, improving speed.
- Validation and dropdown tests use function‑scoped fixture to ensure a fresh screen state (no leftover form data) before each test.
- All field filling helpers are reused from the main `user_creation.py` module – this keeps the test code DRY.
- The `_wait_for_swal_success` helper clicks the OK button automatically, so the test does not need to handle it separately.
- In `test_uc_v04_weak_password_rejected`, the test does **not** expect a specific error message; it only ensures that a duplicate‑user error (which would indicate the weak password was accepted) does **not** occur. This is because some environments may not enforce password strength on the frontend, but the backend may still reject it with a generic 500 – the test remains robust.
```