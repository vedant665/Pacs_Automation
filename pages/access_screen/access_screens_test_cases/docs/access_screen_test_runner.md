# Access Screen Test Runner – Pytest Driver with Excel Report

This script is the centralized **test runner** for the Access Screen test suite. It invokes `pytest` on the test folder, supports test filtering by markers (e.g., `Positive`, `Validation`, `Dropdown`, `user_creation`), and works with a `conftest.py` hook (assumed to exist) that generates an **Excel report** after test execution.

## File Location

`pages/access_screen/access_screens_test_cases/access_screen_test_runner.py`

## Purpose

- Provide a convenient CLI entry point for running Access Screen tests.
- Automatically add the project root to `sys.path` so that all modules and fixtures are importable.
- Pass the test directory to `pytest.main()`.
- Support **keyword‑based filtering** using `-k` (e.g., only tests containing `Positive` in their name/marker).
- Integrate with a custom `conftest.py` that is expected to generate an Excel report (e.g., via `pytest-html` or a custom exporter).

## Dependencies

- Python 3.7+
- `pytest`
- Assumed presence of `conftest.py` in the test folder (or one of its parent directories) that implements Excel reporting hooks.

**Note:** The script does **not** directly depend on Selenium or any application modules – those are imported by the test files themselves.

## Usage

Run from the **project root** or from anywhere as long as the script’s path is correct.

### 1. Run **all** Access Screen tests

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py
```

### 2. Run only **Positive** tests (tests with `Positive` in their name / marker)

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --positive
```

### 3. Run only **Validation** tests

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --validation
```

### 4. Run only **Dropdown** tests

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --dropdown
```

### 5. Run only **User Creation** tests

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --user-creation
```

### 6. Pass custom arguments directly to `pytest`

```bash
python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py -k "Positive and not Smoke" --html=report.html
```

Any unrecognized arguments are forwarded to `pytest.main()`.

---

## Script Behavior

1. **Path setup** – adds the project root (four levels up) to `sys.path` to ensure imports like `pages`, `common`, `config` work.

2. **Argument parsing** – checks the first CLI argument:
   - If **no arguments** → runs all tests in the current directory.
   - If `--positive` → runs `pytest -k "Positive"`.
   - If `--validation` → runs `pytest -k "Validation"`.
   - If `--dropdown` → runs `pytest -k "Dropdown"`.
   - If `--user-creation` → runs `pytest -k "user_creation"`.
   - Else → forwards all arguments as‑is to `pytest`.

3. **Test collection** – `pytest.main()` is called with:
   - The test folder path (the same directory where this runner resides)
   - Flags: `-v` (verbose), `--tb=short` (short traceback), `-s` (allow print statements)
   - Any extra arguments from the CLI

4. **Exit code** – the script exits with the same code returned by `pytest.main()`.

---

## Integration with Excel Reporting (`conftest.py`)

The test folder (`pages/access_screen/access_screens_test_cases/`) is expected to contain a `conftest.py` file that:

- Defines pytest hooks (e.g., `pytest_sessionfinish`) to aggregate test results.
- Writes the results to an **Excel file** (`access_screen_test_report.xlsx` or similar).
- May also include fixtures for browser setup, configuration loading, or navigation.

**Example `conftest.py` hook structure:**

```python
# pages/access_screen/access_screens_test_cases/conftest.py
import pytest
from openpyxl import Workbook

def pytest_sessionfinish(session, exitstatus):
    # Write test outcomes, durations, etc. to an Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.append(["Test Name", "Status", "Duration"])
    # ... collect from session.items
    wb.save("access_screen_report.xlsx")
```

The runner script does not require any Excel libraries – it simply calls `pytest`, and the hooks defined in `conftest.py` produce the report automatically.

---

## Test File Naming Conventions (for filtering)

The `-k` filtering works on test **names**, **class names**, **module names**, and **markers**. For the shortcuts to work, test files/functions should contain the keywords:

- **Positive** – tests that verify correct behavior with valid inputs.
- **Validation** – negative tests that validate error messages for invalid inputs.
- **Dropdown** – tests focusing on dropdown population, selection, and filtering.
- **user_creation** – tests specifically for the `create_user` flow (may be a subset of Positive/Validation).

Markers can also be defined explicitly using `@pytest.mark.positive`, etc., and then filtered with `-m positive`. The current implementation uses `-k` (keyword). You can modify the script to support `-m` markers if needed.

---

## Example Output

When you run the runner, you will see pytest’s normal output plus any logging from the tests. After completion, the Excel report should appear in the same folder.

```bash
$ python pages/access_screen/access_screens_test_cases/access_screen_test_runner.py --positive

  Running Positive tests only...

============================= test session starts ==============================
platform win32 -- Python 3.10.0, pytest-7.4.0, pluggy-1.0.0
rootdir: C:\project
collected 12 items / 8 deselected / 4 selected

test_entity_group.py::test_create_entity_group_positive PASSED
test_role_creation.py::test_create_role_positive PASSED
test_user_creation.py::test_create_user_positive PASSED
test_dropdowns.py::test_role_dropdown_values_positive PASSED

====================== 4 passed, 8 deselected in 45.23s =======================

Excel report generated: access_screen_report.xlsx
```

---

## Customising the Runner

You can extend the `run_tests()` function to accept more options:

- `--html` – to generate an HTML report alongside Excel.
- `--browser` – to pass a browser name as a pytest variable.
- `--headed` – to run Chrome in headed mode instead of headless.

Example extension:

```python
elif "--headed" in cli_args:
    exit_code = run_tests(["--headed", "-k", ...])
```

Remember to modify `conftest.py` accordingly to read those custom arguments.

## Notes

- The script assumes the test folder is the **same directory** as the runner. All `*.py` files starting with `test_` inside that folder will be discovered.
- If you have conftest.py hooks that generate Excel or other reports, ensure that the working directory has write permissions.
- The shortcuts `--positive`, `--validation`, etc. are **case‑sensitive** when matching test names. Use `--user-creation` (lowercase) as shown; test names should contain exactly `user_creation`.
- The script uses `sys.argv[1:]`, so you can combine shortcuts with extra arguments, e.g.:
  ```bash
  python runner.py --positive --tb=line
  ```
  The `--positive` is consumed by the script, and `--tb=line` goes to pytest.
```