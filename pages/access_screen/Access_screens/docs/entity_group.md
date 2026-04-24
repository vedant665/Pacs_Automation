# Entity Group Definition Screen – Automation Module

This module provides a Selenium-based automation helper for the **Entity Group Definition** screen of an Angular application. It handles:

- Opening the creation form (Add button)
- Filling in `Entity Group Name` and `Level`
- Submitting the form
- Validating the submission result (SweetAlert, toast, or error)
- Searching for the newly created group in the data table
- Verifying that the group appears in the `entity_group` column

## File Location

`pages/access_screen/entity_group.py`

## Dependencies

- Python 3.7+
- Selenium WebDriver
- `selenium.webdriver.common.by`
- `selenium.webdriver.support.ui.WebDriverWait`
- `selenium.webdriver.support.expected_conditions`
- `logging`, `time`, `re` (implicitly used)

## Usage Example

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.access_screen.entity_group import create_entity_group

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Assume you are already logged in and on the Entity Group Definition page
create_entity_group(driver, wait, "Admin Role", "2")
```

## Function Reference

### `create_entity_group(driver, wait, group_name, level)`

The main entry point. Creates a new entity group, submits it, and verifies its appearance in the table.

**Parameters:**

| Name        | Type            | Description                                      |
|-------------|-----------------|--------------------------------------------------|
| `driver`    | WebDriver       | Active Selenium WebDriver instance               |
| `wait`      | WebDriverWait   | Explicit wait object for the driver              |
| `group_name`| str             | Name of the entity group (e.g., `"Admin Role"`)  |
| `level`     | str or int      | Level value (e.g., `"2"` or `2`)                 |

**Raises:**

- `Exception` – if the submission shows an error (alert-danger, toast-error, etc.)
- `Exception` – if the group name is not found in the table after creation
- `TimeoutException` – if required UI elements are missing

**Behavior:**

1. Clicks the **ADD** button (selector: `//div[@mattooltip='ADD']//button`)
2. Fills the **Entity Group Name** and **Level** fields using label-based XPath
3. Clicks the **Submit** button
4. Checks for success/error feedback (SweetAlert, toast, or inline error)
5. Triggers a search for the new group name using the table search bar
6. Verifies that the name appears in the `mat-column-entity_group` column
7. Clears the search input to restore full table view

---

## Private Helpers

### `_fill_field(driver, wait, label_text, value)`

Fills a Material input field by its `<mat-label>` text.

- Scrolls the element into view
- Attempts `click()`, `clear()`, `send_keys()`
- Falls back to JavaScript `value` assignment if normal interaction fails

### `_check_result(driver, wait)`

Checks the server response after form submission.

- Looks for `.alert-danger`, `.toast-error`, or `.snack-bar-error` – raises exception if found
- Looks for `.swal2-success` – clicks the confirmation button if present
- Falls back to `.toast-success` / `.snack-bar-success` for logging

### `_verify_in_table(driver, wait, group_name)`

Searches the data table for the given group name and validates its presence.

**Steps:**

1. Clicks the search button (`button.search-btn` or `button[aria-label='Search']`)
2. Enters the `group_name` into the revealed search input
3. Waits for Angular filtering (1.5 seconds)
4. Checks for a “No results found” row – raises `Exception` if found
5. Searches for an XPath matching `//td[contains(@class,'mat-column-entity_group')]//span[normalize-space()='{group_name}']`
6. Clears the search input to reset the table

## Page Element Assumptions

The module assumes the target page contains:

| Element                     | Selector (CSS / XPath)                                                              |
|-----------------------------|-------------------------------------------------------------------------------------|
| Add button                  | `//div[@mattooltip='ADD']//button`                                                  |
| Input field (by label)      | `//mat-label[normalize-space()='{label}']/ancestor::mat-form-field//input`          |
| Submit button               | `//button[@type='submit']//span[normalize-space()='Submit']`                        |
| Success SweetAlert          | `.swal2-success`                                                                    |
| Error alert                 | `.alert-danger`, `.toast-error`, `.snack-bar-error`                                 |
| Search button               | `button.search-btn`, `button[aria-label='Search']`                                  |
| Search input                | `input.search-input`, `.erp-search-container input`, `input[placeholder*='Search']` |
| Table “No results” row      | `.mat-mdc-no-data-row`, text `No results found` / `No data found`                   |
| Entity group column cell    | `td.mat-column-entity_group span`                                                   |

## Logging

The module uses Python’s `logging` module with a console handler (INFO level).  
Example log output:

```
14:32:11 | INFO     | Creating Entity Group: 'Admin Role' | Level: '2'
14:32:11 | INFO     |   Clicking Add...
14:32:12 | INFO     |   Filling 'Entity Group Name' = 'Admin Role'
14:32:13 | INFO     |   Filling 'Level' = '2'
14:32:14 | INFO     |   Submitting...
14:32:16 | INFO     |   Submit succeeded (SweetAlert confirmed).
14:32:18 | INFO     |   Verifying 'Admin Role' in table...
14:32:20 | INFO     |   Verification PASSED: 'Admin Role' found in table.
14:32:21 | INFO     | Done: Entity Group 'Admin Role' created and verified.
```

## Error Handling

- If the submission fails (error toast/danger alert), an `Exception` is raised with the error text.
- If the group name is **not found** after searching, an `Exception` is raised.
- If the SweetAlert success is not detected, the module falls back to checking success toasts.
- All element interactions use JavaScript scrolling and `WebDriverWait` to avoid staleness issues.

## Notes

- The module includes hard‑coded sleep calls (`time.sleep(0.3)`, `time.sleep(1.5)`) to accommodate Angular change detection. Adjust these if the application becomes faster.
- The search input clearing step is wrapped in a `try/except` because the input may become detached after filtering.
- The `_fill_field` helper uses a `click()` before `clear()` to ensure the input is focused and ready. If that fails, a JavaScript fallback is used.
```