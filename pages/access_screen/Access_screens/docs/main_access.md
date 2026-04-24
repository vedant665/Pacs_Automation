# Test Runner – Access Screen Automation (Entity Group, Role, User)

This script serves as the **orchestration runner** for automating the creation of Entity Groups, Roles, and Users in the PACS Angular application. It:

- Launches a Chrome browser (maximized, with WebDriver Manager)
- Logs into the application using credentials from `config.py`
- Navigates to the required **Access** sub‑screens using a shared navigation helper
- Calls dedicated creation modules (`entity_group.py`, `role_creation.py`, `user_creation.py`)
- Feeds test data from `pages/access_screen/data/access_data.py`
- Logs progress and handles cleanup (driver quit)

## File Location

`test_runner.py` (or the file name that contains this script – adjust as needed)

## Dependencies

- Python 3.7+
- Selenium WebDriver
- `webdriver_manager` (automatic ChromeDriver management)
- `config.py` – must define:  
  `MODULE_LOGIN_URL`, `PACS_EMAIL`, `PACS_PASSWORD`, `PACS_FACILITY`
- `common.nav_section` – provides `navigate_to(driver, wait, main_menu, sub_menu)`
- `pages.access_screen.Access_screens.entity_group` – provides `create_entity_group`
- `pages.access_screen.Access_screens.role_creation` – provides `create_role`
- `pages.access_screen.Access_screens.user_creation` – provides `create_user`
- `pages.access_screen.data.access_data` – provides dictionaries:  
  `entity_group_data`, `role_creation_data`, `user_creation_data`

## Usage Example

```bash
python test_runner.py
```

Make sure `config.py` and all module dependencies are properly imported and that the file paths are correct relative to the execution directory.

## Script Structure

### 1. Path Setup

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
```

Adds the project root to `sys.path` so that imports like `config`, `common`, `pages` work regardless of the current working directory.

### 2. Imports

- Selenium components (`webdriver`, `Service`, `Options`, `By`, `WebDriverWait`, `EC`)
- `webdriver_manager.chrome.ChromeDriverManager`
- Configuration (`MODULE_LOGIN_URL`, `PACS_EMAIL`, `PACS_PASSWORD`, `PACS_FACILITY`)
- Navigation helper (`navigate_to`)
- Three creation modules
- Test data dictionaries from `access_data.py`

### 3. Logger

Standard logging with a console handler (INFO level). Log lines include timestamps and log levels.

### 4. Driver Setup – `build_driver()`

Creates and returns a Chrome WebDriver instance:

- Maximized window (`--start-maximized`)
- Suppresses Chrome logging (`excludeSwitches`, `enable-logging`)
- Uses `ChromeDriverManager` to automatically download and manage the correct ChromeDriver version

### 5. Login – `login(driver, wait)`

Performs the authentication flow:

1. Navigate to `MODULE_LOGIN_URL`
2. Enter email (from `PACS_EMAIL`)
3. Click the facility dropdown (`//mat-select`) and select the option matching `PACS_FACILITY`
4. Enter password (from `PACS_PASSWORD`)
5. Click the submit button using JavaScript (ensures click even if partially obscured)
6. Wait 3 seconds
7. Log success

### 6. Main Execution

The script:

- Builds the driver and a `WebDriverWait` with **60 seconds** timeout
- Executes `login(driver, wait)`
- Calls `navigate_to()` and the respective creation function(s)
- Currently **only `User Creation` is uncommented** (others are commented out for selective execution)
- Logs final success and waits 5 seconds before quitting the driver

**Example flow (with only user creation active):**

```python
navigate_to(driver, wait, "Access", "User Creation Screen")
create_user(driver, wait, **user_creation_data)
```

### 7. Cleanup

The `finally` block ensures `driver.quit()` is called even if an exception occurs.

---

## Configuration File (`config.py`)

The script expects a `config.py` file in the project root (or in `sys.path`) containing:

```python
MODULE_LOGIN_URL = "https://your-app.com/login"
PACS_EMAIL = "admin@example.com"
PACS_PASSWORD = "your_password"
PACS_FACILITY = "Main Facility"
```

## Test Data File (`pages/access_screen/data/access_data.py`)

The script imports three dictionaries (keys must match the parameters expected by each creation function):

```python
entity_group_data = {
    "group_name": "Admin Group",
    "level": "2"
}

role_creation_data = {
    "role_name": "Supervisor",
    "entity_group": "BRANCH"
}

user_creation_data = {
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "Test@123",
    "user_types": ["Admin", "Viewer"],
    "role": "Supervisor",
    "entity": "BRANCH"
}
```

> **Note:** The dictionaries are unpacked (`**data_dict`) when calling the creation functions. Ensure the keys match the function parameter names exactly.

## Navigation Helper (`common.nav_section`)

The script uses `navigate_to(driver, wait, main_menu, sub_menu)`.  
This helper is expected to:

- Click the main menu item (e.g., `"Access"`)
- Click the sub‑menu item (e.g., `"User Creation Screen"`)
- Wait for the target screen to load

## How to Run Selective Tests

The script currently has all creation calls commented except for **User Creation**. To run other flows:

1. Uncomment the corresponding `navigate_to` and creation function calls.
2. Ensure the required test data dictionary is defined in `access_data.py`.
3. Run the script again.

Example – running all three in sequence:

```python
navigate_to(driver, wait, "Access", "Entity Group Definition")
create_entity_group(driver, wait, **entity_group_data)

navigate_to(driver, wait, "Access", "Role Creation Screen")
create_role(driver, wait, **role_creation_data)

navigate_to(driver, wait, "Access", "Role Screen Link")
# create_role_screen_link(...)   # not yet implemented

navigate_to(driver, wait, "Access", "User Creation Screen")
create_user(driver, wait, **user_creation_data)

navigate_to(driver, wait, "Access", "Screen Api Link")
# create_screen_api_link(...)    # not yet implemented
```

## Logging Output Example

```
14:32:01 | INFO     | --- LOGIN ---
14:32:05 | INFO     | Login Done
14:32:06 | INFO     | Navigating to: Access -> User Creation Screen
14:32:08 | INFO     | Creating User: 'testuser' | Email: 'test@example.com'
14:32:08 | INFO     |   Clicking Add...
14:32:09 | INFO     |   Filling 'username' = 'testuser'
...
14:32:25 | INFO     | Table verification PASSED for 'testuser' (date checked)
14:32:26 | INFO     | Done: User 'testuser' created and verified.
14:32:26 | INFO     | SUCCESS: All forms filled!
```

## Error Handling

- If any creation step fails (e.g., submit error, element not found), an exception is raised and the script will print the traceback.
- The `finally` block still executes `driver.quit()` to close the browser.
- The driver wait timeout is set to **60 seconds**, which should be sufficient for slow Angular rendering. Adjust as needed.

## Notes

- The script uses JavaScript clicks for several interactions (`driver.execute_script("arguments[0].click();", element)`) to avoid “element not intractable” issues.
- Hard‑coded sleeps (`time.sleep(3)` after login, `time.sleep(5)` at the end) are present – adjust if the application loads faster.
- The `login` function uses a static XPath for the facility dropdown; if the application has multiple facilities, ensure `PACS_FACILITY` matches an existing option exactly.
- All creation modules rely on the same `verify_in_table` helper from `common.table_helpers`. That helper must be implemented correctly for the verification step to work.
```