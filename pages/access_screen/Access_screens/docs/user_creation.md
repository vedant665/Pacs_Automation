# User Creation Screen – Automation Module

This module provides a Selenium-based automation helper for the **User Creation** screen of an Angular application. It handles:

- Opening the creation form (Add button)
- Filling user details: `username`, `email`, `first_name`, `last_name`, `password`
- Selecting **User Types** (multi‑select dropdown)
- Selecting a **Role** (searchable single‑select dropdown)
- Selecting an **Entity** (multi‑select dropdown, single value in the example)
- Submitting the form
- Validating the submission result (SweetAlert, toast, or error)
- Verifying that the newly created user appears in the data table (via a shared table helper, with date column validation)

## File Location

`pages/access_screen/user_creation.py`

## Dependencies

- Python 3.7+
- Selenium WebDriver
- `selenium.webdriver.common.by`
- `selenium.webdriver.support.ui.WebDriverWait`
- `selenium.webdriver.support.expected_conditions`
- `logging`, `time`
- `common.table_helpers` – provides `verify_in_table()` with optional date checking

## Usage Example

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.access_screen.user_creation import create_user

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Assume you are already logged in and on the User Creation page
create_user(
    driver, wait,
    username="john.doe",
    email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    password="SecurePass123",
    user_types=["Admin", "Manager"],
    role="Supervisor",
    entity="BRANCH"
)
```

## Function Reference

### `create_user(driver, wait, username, email, first_name, last_name, password, user_types, role, entity)`

The main entry point. Creates a new user, submits the form, and verifies the user appears in the table.

**Parameters:**

| Name          | Type            | Description                                                              |
|---------------|-----------------|--------------------------------------------------------------------------|
| `driver`      | WebDriver       | Active Selenium WebDriver instance                                       |
| `wait`        | WebDriverWait   | Explicit wait object for the driver                                      |
| `username`    | str             | Username for the new user                                                |
| `email`       | str             | Email address                                                            |
| `first_name`  | str             | First name                                                               |
| `last_name`   | str             | Last name                                                                |
| `password`    | str             | Password                                                                 |
| `user_types`  | list[str]       | List of user types to select (e.g., `["Admin", "Manager"]`)              |
| `role`        | str             | Role to select from the searchable dropdown                              |
| `entity`      | str             | Entity to select from the multi-select dropdown (single value in example)|

**Raises:**

- `Exception` – if the submission shows an error (alert-danger, toast-error, etc.)
- `Exception` – if the username is not found in the table after creation
- `TimeoutException` – if required UI elements are missing

**Behavior:**

1. Clicks the **ADD** button (selector: `//div[@mattooltip='ADD']//button`)
2. Fills the five text inputs using `_fill_input()`
3. Opens the **User Type** multi‑select dropdown and selects all options in `user_types`
4. Opens the **Role** searchable dropdown, types the role name, and selects the matching option
5. Opens the **Entity** multi‑select dropdown and selects the given `entity`
6. Clicks the **Submit** button
7. Checks for success/error feedback (SweetAlert, toast)
8. Calls `verify_in_table(driver, wait, username, check_date=True, date_column="joined", date_format="%d %b %Y")` to search for the new user and validate the `joined` date column format
9. Logs completion

---

## Private Helpers

### `_fill_input(driver, wait, field_name, text)`

Fills a text input identified by its `formcontrolname` attribute.

- Locates `//input[@formcontrolname='{field_name}']`
- Attempts `clear()` and `send_keys()`
- Falls back to JavaScript assignment + manual `input` event dispatch if normal interaction fails

### `_fill_multi_dropdown(driver, wait, label_text, options_list)`

Selects multiple options from a Material multi‑select dropdown identified by its `<mat-label>` text.

**Steps:**

1. Finds the dropdown trigger using XPath:  
   `//mat-label[normalize-space()='{label_text}']/ancestor::mat-form-field//mat-select//div[contains(@class,'select-trigger')]`
2. Scrolls into view and performs a native `click()` to open the panel
3. Waits for `//div[contains(@class,'cdk-overlay-pane')]//mat-option` to appear
4. Loops through `options_list`, clicking each matching option (`//span[normalize-space()='{opt_text}']`)
5. Closes the panel by clicking on `<body>`

### `_fill_search_dropdown(driver, wait, label_text, search_text)`

Selects a single option from a searchable Material dropdown.

**Steps:**

1. Finds and clicks the dropdown trigger (same XPath as above)
2. Waits for the search input inside the overlay:  
   `//div[contains(@class,'cdk-overlay-pane')]//input[contains(@placeholder,'Search')]`
3. Clears and types `search_text` into the search box
4. Waits for the filtered option and clicks it
5. Closes the panel implicitly (option click also closes the dropdown)

### `_check_result(driver, wait)`

Identical to the implementation in `entity_group.py` and `role_creation.py`. Checks for:

- `.alert-danger`, `.toast-error`, `.snack-bar-error` → raises `Exception`
- `.swal2-success` → logs success, clicks confirmation button
- `.toast-success` / `.snack-bar-success` → logs success as fallback

---

## Page Element Assumptions

The module assumes the target page contains:

| Element                     | Selector (CSS / XPath)                                                              |
|-----------------------------|-------------------------------------------------------------------------------------|
| Add button                  | `//div[@mattooltip='ADD']//button`                                                  |
| Text input fields           | `//input[@formcontrolname='username']` (similarly for `email`, `first_name`, etc.)  |
| Multi‑select dropdown trigger | `//mat-label[normalize-space()='User Type']/ancestor::mat-form-field//mat-select//div[contains(@class,'select-trigger')]` |
| Multi‑select option panel   | `//div[contains(@class,'cdk-overlay-pane')]//mat-option`                            |
| Multi‑select option text    | `//div[contains(@class,'cdk-overlay-pane')]//mat-option//span[normalize-space()='{opt_text}']` |
| Searchable dropdown trigger | `//mat-label[normalize-space()='Role']/ancestor::mat-form-field//mat-select//div[contains(@class,'select-trigger')]` |
| Search input in overlay     | `//div[contains(@class,'cdk-overlay-pane')]//input[contains(@placeholder,'Search')]` |
| Entity dropdown trigger     | Similar to User Type but label `'Entity'`                                          |
| Submit button               | `//button[@type='submit']//span[normalize-space()='Submit']`                        |
| Success SweetAlert          | `.swal2-success`                                                                    |
| Error alert                 | `.alert-danger`, `.toast-error`, `.snack-bar-error`                                 |

**Note on dropdowns:**  
The module distinguishes between three dropdown types:
- **Multi‑select** (`_fill_multi_dropdown`) – selects multiple options, closes by clicking `<body>`
- **Searchable single‑select** (`_fill_search_dropdown`) – types into a search box before selecting
- The `user_types` parameter expects a `list`, while `role` and `entity` are single strings

---

## Shared Table Verification

The module uses a common helper:

```python
from common.table_helpers import verify_in_table

verify_in_table(driver, wait, username,
                check_date=True, date_column="joined",
                date_format="%d %b %Y")
```

This helper is expected to:

- Click the search button and reveal the search input
- Type the `username` into the search field
- Assert that the user exists in the appropriate name column
- Optionally validate that a date column (here: `"joined"`) matches the expected format (e.g., `"15 Apr 2025"`)

If the helper raises an exception (user not found or date format mismatch), `create_user()` propagates it.

## Logging

The module uses Python’s `logging` module with a console handler (INFO level).  
Example log output:

```
14:32:11 | INFO     | Creating User: 'john.doe' | Email: 'john.doe@example.com'
14:32:11 | INFO     |   Clicking Add...
14:32:12 | INFO     |   Filling 'username' = 'john.doe'
14:32:12 | INFO     |   Filling 'email' = 'john.doe@example.com'
14:32:13 | INFO     |   Filling 'first_name' = 'John'
14:32:13 | INFO     |   Filling 'last_name' = 'Doe'
14:32:14 | INFO     |   Filling 'password' = 'SecurePass123'
14:32:15 | INFO     |   Multi-select 'User Type': ['Admin', 'Manager']
14:32:16 | INFO     |     Selected 'Admin'
14:32:17 | INFO     |     Selected 'Manager'
14:32:18 | INFO     |   Search-select 'Role': 'Supervisor'
14:32:19 | INFO     |     Selected 'Supervisor'
14:32:20 | INFO     |   Multi-select 'Entity': ['BRANCH']
14:32:21 | INFO     |     Selected 'BRANCH'
14:32:22 | INFO     |   Submitting...
14:32:24 | INFO     |   Submit succeeded (SweetAlert confirmed).
14:32:26 | INFO     | Table verification PASSED for 'john.doe' (date checked)
14:32:27 | INFO     | Done: User 'john.doe' created and verified.
```

## Error Handling

- If the submission fails (error toast/danger alert), an `Exception` is raised with the error text.
- If any helper (`_fill_input`, `_fill_multi_dropdown`, etc.) cannot locate an element, `TimeoutException` is raised.
- If the table verification fails (user not found or date column format mismatch), the exception is propagated.
- The `_fill_input` function includes a JavaScript fallback with manual `input` event dispatch to ensure Angular two‑way binding updates.

## Notes

- The module contains hard‑coded sleeps (`time.sleep(0.3)`, `time.sleep(0.5)`, `time.sleep(1)` after dropdown opening, `time.sleep(2)` after submission). Adjust if the application becomes faster.
- After selecting options in a multi‑select dropdown, the module explicitly clicks `<body>` to close the panel. This is necessary because the panel does not auto‑close after multiple selections.
- The `user_types` parameter is a list; the example usage shows `["Admin", "Manager"]`. The module will select **all** options in that list.
- Although the `entity` parameter is passed to `_fill_multi_dropdown` as a single‑element list `[entity]`, the function is designed to handle multiple entities if needed.
- The table verification expects a column named `joined` with dates formatted as `%d %b %Y` (e.g., `"15 Apr 2025"`). If your application uses a different format, change the `date_format` parameter in the `verify_in_table` call.
```