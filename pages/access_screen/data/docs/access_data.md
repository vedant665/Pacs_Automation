```markdown
# Test Data Generator – Access Screens

This module provides random test data generation for the **Entity Group**, **Role Creation**, and **User Creation** screens of the Access module. It is used by the Pytest test suites to create unique, realistic data for positive test scenarios.

## File Location

`pages/access_screen/data/access_test_data.py`

## Dependencies

- Python `random` module (standard library)
- Python `datetime` module (standard library)

No external dependencies.

## Functions

### `random_entity_group_data()`

Generates a random dictionary for creating an Entity Group.

**Returns:**

```python
{
    "group_name": str,   # e.g., "Admin Role 143215"
    "level": str         # e.g., "5"
}
```

**Generation logic:**

- `timestamp` = current time in `HHMMSS` format (e.g., `143215`)
- `number` = random integer between 10 and 99
- `group_name` = randomly chosen prefix + suffix + timestamp + number  
  Prefixes: `["Admin", "Manager", "Super", "Test", "Demo", "Audit", "Ops"]`  
  Suffixes: `["Role", "Group", "Team", "Access", "Level", "Unit"]`
- `level` = random string from `1` to `10`

**Example output:**

```python
{"group_name": "Super Level 14321567", "level": "8"}
```

---

### `random_role_creation_data()`

Generates a random dictionary for creating a Role.

**Returns:**

```python
{
    "role_name": str,      # e.g., "Manager Position 14321588"
    "entity_group": str    # one of ["BRANCH", "DCB", "PACS"]
}
```

**Generation logic:**

- `timestamp` = current time in `HHMMSS`
- `number` = random integer between 10 and 99
- `role_name` = random prefix + random suffix + timestamp + number  
  Prefixes: `["Admin", "Manager", "Super", "Test", "Ops"]`  
  Suffixes: `["Role", "Position", "Designation"]`
- `entity_group` = randomly chosen from `["BRANCH", "DCB", "PACS"]`

**Example output:**

```python
{"role_name": "Admin Designation 14321542", "entity_group": "DCB"}
```

---

### `random_user_creation_data()`

Generates a random dictionary for creating a User, respecting **role‑entity compatibility**.

**Returns:**

```python
{
    "username": str,       # e.g., "testuser14321542"
    "email": str,          # e.g., "testuser14321542@mail.com"
    "first_name": str,     # e.g., "Test42"
    "last_name": str,      # e.g., "User42"
    "password": str,       # "Test@1234567" (fixed strong password)
    "user_types": list,    # e.g., ["Checker", "Maker"]
    "role": str,           # "DCB" or "PACS"
    "entity": str          # Compatible with the chosen role
}
```

**Generation logic:**

- `timestamp` = current time in `HHMMSS`
- `number` = random integer between 10 and 99
- `username` = `f"testuser{timestamp}{number}"`
- `email` = `f"{username}@mail.com"`
- `first_name` = `f"Test{number}"`
- `last_name` = `f"User{number}"`
- `password` = fixed `"Test@1234567"` (meets typical complexity requirements)
- `user_types` = random sample of **2** distinct values from  
  `["Maker", "Checker", "Approver", "Maker-Checker", "Checker-Approver"]`
- `role` = randomly chosen from `["DCB", "PACS"]`
- `entity` = randomly chosen from a **whitelist** that depends on the selected role:
  - If `role == "DCB"` → entity is always `"dcb1"`
  - If `role == "PACS"` → entity is randomly chosen from a large list of PACS‑specific entity names (e.g., `"Anand Shetkari ..."`, `"Maha Seva Society"`, etc.)

**Role‑Entity Mapping (const):**

```python
ROLE_ENTITY_MAP = {
    "DCB": ["dcb1"],
    "PACS": ["Anand Shetkari Vividh Karyakari Sahakari Sanstha Maryadit",
             "Maha Seva Society",
             "Songaon Primary Agricultural Cooperative Credit Society.",
             # ... 22 entries in total
    ]
}
```

**Example output (PACS role):**

```python
{
    "username": "testuser14521530",
    "email": "testuser14521530@mail.com",
    "first_name": "Test30",
    "last_name": "User30",
    "password": "Test@1234567",
    "user_types": ["Approver", "Checker"],
    "role": "PACS",
    "entity": "Songaon Primary Agricultural Cooperative Credit Society."
}
```

**Example output (DCB role):**

```python
{
    "username": "testuser14521530",
    "email": "testuser14521530@mail.com",
    "first_name": "Test30",
    "last_name": "User30",
    "password": "Test@1234567",
    "user_types": ["Maker", "Checker-Approver"],
    "role": "DCB",
    "entity": "dcb1"
}
```

---

## Pre‑generated Data Variables (for immediate use)

The module also provides **three pre‑generated data dictionaries** at the module level. These are generated **once** when the module is imported and remain fixed for the duration of the test run.

```python
entity_group_data = random_entity_group_data()
role_creation_data = random_role_creation_data()
user_creation_data = random_user_creation_data()
```

These are useful when a test needs **static, repeatable** random data (e.g., for a test that creates exactly one record and then verifies it). If you need fresh random data for each test, call the function directly instead of using the pre‑generated variable.

---

## Usage in Test Files

### Example 1 – Generating fresh random data inside a test

```python
from pages.access_screen.data.access_test_data import random_user_creation_data

def test_create_user(user_creation_screen):
    driver, wait = user_creation_screen
    data = random_user_creation_data()   # fresh each time
    # ... fill form using data
```

### Example 2 – Using the pre‑generated variable (static)

```python
from pages.access_screen.data.access_test_data import user_creation_data

def test_single_user_creation(user_creation_screen):
    driver, wait = user_creation_screen
    # user_creation_data is the same for all calls in this test session
    # ... fill form using user_creation_data
```

### Example 3 – Importing pre‑defined constants (for validation tests)

```python
from pages.access_screen.data.access_test_data import DUPLICATE_USERNAME, DUPLICATE_EMAIL, WEAK_PASSWORDS
```

**Note:** The validation constants (`DUPLICATE_USERNAME`, `DUPLICATE_EMAIL`, `VALID_PASSWORD`, `WEAK_PASSWORDS`) are **not shown** in the provided snippet but are assumed to exist in the same file. They are typically hard‑coded strings that represent pre‑existing data or predefined weak passwords.

---

## Customising Data Generation

You can easily extend or modify the generation logic:

- **Change password strength** – modify the hard‑coded `password` in `random_user_creation_data()`.
- **Add more user types** – extend the `USER_TYPES` list.
- **Add more entity groups** – extend `ROLE_ENTITY_MAP` with new roles and their valid entities.
- **Change the number of user types selected** – modify the second argument in `random.sample(USER_TYPES, 2)`.

---

## Notes

- All generated data is **non‑persistent** – it does not write to any database; it only provides values for test input.
- The timestamp ensures uniqueness across test runs, but if two tests run in the same second, there is a tiny chance of collision. The `number` suffix (10‑99) reduces that risk further.
- The module does **not** depend on Selenium or any test framework – it is pure Python and can be used anywhere.
- The `ROLE_ENTITY_MAP` is a design constraint: in the actual application, a DCB role only works with the `dcb1` entity, while a PACS role works with many PACS entities. This mapping ensures tests never attempt an invalid combination.
```