# Role Creation Screen – Automation Module

This module provides a Selenium-based automation helper for the **Role Creation** screen of an Angular application. It handles:

- Opening the creation form (Add button)
- Filling the **Role Name** text field
- Selecting an **Entity Type** from a dropdown (`BRANCH`, `DCB`, or `PACS`)
- Submitting the form
- Validating the submission result (SweetAlert, toast, or error)
- Verifying that the newly created role appears in the data table (via a shared table helper)

## File Location

`pages/access_screen/role_creation.py`

## Dependencies

- Python 3.7+
- Selenium WebDriver
- `selenium.webdriver.common.by`
- `selenium.webdriver.support.ui.WebDriverWait`
- `selenium.webdriver.support.expected_conditions`
- `logging`, `time`
- `common.table_helpers` – provides `verify_in_table()` helper

## Usage Example

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.access_screen.role_creation import create_role

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Assume you are already logged in and on the Role Creation page
create_role(driver, wait, "Admin Role", "BRANCH")
```

## Function Reference

### `create_role(driver, wait, role_name, entity_group)`

The main entry point. Creates a new role, submits it, and verifies its appearance in the table.

**Parameters:**

| Name           | Type            | Description                                      |
|----------------|-----------------|--------------------------------------------------|
| `driver`       | WebDriver       | Active Selenium WebDriver instance               |
| `wait`         | WebDriverWait   | Explicit wait object for the driver              |
| `role_name`    | str             | Name of the role (e.g., `"Admin Role"`)          |
| `entity_group` | str             | Entity type to select – `"BRANCH"`, `"DCB"`, or `"PACS"` |

**Raises:**

- `Exception` – if the submission shows an error (alert-danger, toast-error, etc.)
- `Exception` – if the role name is not found in the table after creation
- `TimeoutException` – if required UI elements are missing

**Behavior:**

1. Clicks the **ADD** button (selector: `//div[@mattooltip='ADD']//button`)
2. Fills the **Role Name** input (`formcontrolname="role_name"`)
3. Selects the **Entity Type** from a dropdown using `_fill_dropdown()`
4. Clicks the **Submit** button
5. Checks for success/error feedback (SweetAlert, toast, or inline error)
6. Calls `verify_in_table(driver, wait, role_name, "name")` to search and validate the new role in the table
7. Logs completion

---

## Private Helpers

### `_fill_dropdown(driver, wait, formcontrol_name, option_text)`

Selects an option from a Material dropdown (`mat-select`) identified by its `formcontrolname`.

**Steps:**

1. Locates the trigger div inside the `mat-select` using XPath:  
   `//mat-select[@formcontrolname='{formcontrol_name}']//div[contains(@class,'select-trigger')]`
2. Scrolls into view and performs a **native** `click()` (JavaScript click would not fire Angular events)
3. Waits for the dropdown panel (`//div[@role='listbox']//mat-option`)
4. Clicks the matching option by its visible text

**Note:** The function uses a short `time.sleep(0.5)` after opening the dropdown to ensure the options are rendered.

### `_check_result(driver, wait)`

Checks the server response after form submission.

- Looks for `.alert-danger`, `.toast-error`, or `.snack-bar-error` – raises exception if found
- Looks for `.swal2-success` – clicks the confirmation button if present
- Falls back to `.toast-success` / `.snack-bar-success` for logging

---

## Page Element Assumptions

The module assumes the target page contains:

| Element                     | Selector (CSS / XPath)                                                              |
|-----------------------------|-------------------------------------------------------------------------------------|
| Add button                  | `//div[@mattooltip='ADD']//button`                                                  |
| Role Name input             | `//input[@formcontrolname='role_name']`                                             |
| Entity Type dropdown        | `//mat-select[@formcontrolname='entity_type']` (trigger and options as described)   |
| Submit button               | `//button[@type='submit']//span[normalize-space()='Submit']`                        |
| Success SweetAlert          | `.swal2-success`                                                                    |
| Error alert                 | `.alert-danger`, `.toast-error`, `.snack-bar-error`                                 |
| Dropdown panel (role)       | `//div[@role='listbox']//mat-option`                                                |
| Dropdown option text        | `//div[@role='listbox']//mat-option//span[normalize-space()='{option_text}']`       |

**Note on dropdown selection:**  
The module does **not** rely on `mat-select`’s default `click()` because Angular Material often requires a native click on the trigger element. The `_fill_dropdown` function handles this correctly.

---

## Shared Table Verification

The module delegates table search and verification to a common helper:

```python
from common.table_helpers import verify_in_table
```

This helper is assumed to:

- Click the search button and reveal the search input
- Type the `role_name` into the search field
- Wait for filtering
- Assert that the role exists in the appropriate column (`name` column in this case)

If the helper raises an exception (e.g., role not found), `create_role()` propagates it.

---

## Logging

The module uses Python’s `logging` module with a console handler (INFO level).  
Example log output:

```
14:32:11 | INFO     | Creating Role: 'Admin Role' | Entity: 'BRANCH'
14:32:11 | INFO     |   Clicking Add...
14:32:12 | INFO     |   Filling Role Name = 'Admin Role'
14:32:13 | INFO     |   Selecting 'BRANCH' from dropdown (formcontrol: entity_type)
14:32:14 | INFO     |   Selected 'BRANCH'.
14:32:15 | INFO     |   Submitting...
14:32:17 | INFO     |   Submit succeeded (SweetAlert confirmed).
14:32:19 | INFO     |   Verifying in table...
14:32:20 | INFO     | Table verification PASSED for 'Admin Role'
14:32:21 | INFO     | Done: Role 'Admin Role' created and verified.
```

## Error Handling

- If the submission fails (error toast/danger alert), an `Exception` is raised with the error text.
- If the `verify_in_table()` helper fails (role not found), the exception is propagated.
- Native clicks are used for the dropdown trigger; JavaScript fallback is **not** attempted for the trigger because Angular events rely on native DOM events.
- All element interactions use explicit waits (`WebDriverWait`) and scrolling via JavaScript to avoid visibility issues.

## Notes

- The module contains hard‑coded sleeps (`time.sleep(0.3)`, `time.sleep(0.5)`, `time.sleep(2)` after submission). Adjust if the application becomes faster.
- The dropdown selection function specifically uses a **native** `trigger.click()` because `driver.execute_script("arguments[0].click();", trigger)` would not properly open the Material dropdown.
- The shared `verify_in_table` helper is expected to handle the search button, input, and column verification. If your application does not have a dedicated table search, you may need to adapt or replace that call.
```