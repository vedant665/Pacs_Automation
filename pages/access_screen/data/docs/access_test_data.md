# Access Screen Test Data – Centralized Test Data for Pytest

This module provides **fixed test data** (duplicate values, weak passwords, blank values) and **random data generators** for the Access Screen Pytest test suite. It reuses the core random data generator from `access_data.py` and adds convenience wrappers for specific test scenarios (single user type, DCB role locking).

## File Location

`pages/access_screen/data/access_test_data.py`

## Dependencies

- Python `random` (standard library)
- Python `datetime` (standard library)
- `pages.access_screen.data.access_data` – provides:
  - `USER_TYPES` (list of user type strings)
  - `ROLE_ENTITY_MAP` (role → valid entities dictionary)
  - `random_user_creation_data()` (core random user dict generator)

No external dependencies.

---

## Fixed Constants (for Negative / Validation Tests)

These values are used in validation test cases where specific error conditions must be triggered.

### `DUPLICATE_USERNAME`

**Type:** `str`  
**Example:** `"7686uyfthft"`  
**Purpose:** A username that already exists in the system. Used to test duplicate username validation.

### `DUPLICATE_EMAIL`

**Type:** `str`  
**Example:** `"vedant@rhythmflows.com"`  
**Purpose:** An email address that already exists in the system. Used to test duplicate email validation.

### `VALID_PASSWORD`

**Type:** `str`  
**Example:** `"Test@1234567"`  
**Purpose:** A password that meets all application password policy requirements (length, uppercase, lowercase, digit, special character). Used as a baseline in positive tests.

### `WEAK_PASSWORDS`

**Type:** `dict[str, str]`  
**Content:**

| Key             | Example Value        | Violation                      |
|-----------------|----------------------|--------------------------------|
| `"too_short"`   | `"Ved@1"`            | Length < minimum (likely 8)    |
| `"no_uppercase"`| `"vedant@12345"`     | No uppercase letter            |
| `"no_lowercase"`| `"VEDANT@12345"`     | No lowercase letter            |
| `"no_number"`   | `"Vedant@abcdx"`     | No digit                       |
| `"no_special"`  | `"Vedant123456"`     | No special character           |

**Purpose:** Used in password validation tests to verify that the application rejects weak passwords with appropriate error messages.

### `BLANK_VALUES`

**Type:** `dict[str, str]`  
**Content:**

```python
{
    "username": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "password": "",
}
```

**Purpose:** Used to test required field validation. All fields are set to empty strings.

---

## Random Data Generators

These functions generate unique, valid data for **positive test scenarios**. They rely on the core `random_user_creation_data()` from `access_data.py` and add customisation layers.

### `random_username()`

**Returns:** `str` – Unique username using timestamp + random number.

**Example:** `"testuser14321542"`

**Generation:**  
`f"testuser{datetime.now().strftime('%H%M%S')}{random.randint(10,99)}"`

---

### `random_email()`

**Returns:** `str` – Unique email derived from `random_username()`.

**Example:** `"testuser14321542@mail.com"`

---

### `random_user_data(**overrides)`

**Returns:** `dict` – Complete user creation dictionary (keys: `username`, `email`, `first_name`, `last_name`, `password`, `user_types`, `role`, `entity`).

**Parameters:**

- `**overrides` – Optional key‑value pairs to override any field in the generated data.

**Behavior:**

1. Calls `random_user_creation_data()` from `access_data.py` (which already respects role‑entity pairing).
2. Updates the dictionary with any `overrides` provided.

**Example:**

```python
data = random_user_data(username="custom_name", user_types=["Maker"])
```

---

### `random_user_data_single_type(**overrides)`

**Returns:** `dict` – Same as `random_user_data()`, but `user_types` is a list containing **exactly one** user type (randomly chosen from `USER_TYPES`).

**Purpose:** Some tests may require a user with only one role (rather than two).

**Example output:**

```python
{
    "username": "testuser14321542",
    "email": "testuser14321542@mail.com",
    "first_name": "Test42",
    "last_name": "User42",
    "password": "Test@1234567",
    "user_types": ["Maker"],           # single element
    "role": "PACS",
    "entity": "Maha Seva Society"
}
```

---

### `random_user_data_dcb(**overrides)`

**Returns:** `dict` – Same as `random_user_data()`, but forces:

- `role = "DCB"`
- `entity = "dcb1"`

**Purpose:** Tests that specifically require a DCB role (which only works with the `dcb1` entity). Overrides any other role/entity that the random generator might have chosen.

**Example output:**

```python
{
    "username": "testuser14321542",
    "email": "testuser14321542@mail.com",
    "first_name": "Test42",
    "last_name": "User42",
    "password": "Test@1234567",
    "user_types": ["Checker", "Approver"],
    "role": "DCB",
    "entity": "dcb1"                    # fixed
}
```

---

## Usage in Test Files

### 1. Importing fixed constants for validation tests

```python
from pages.access_screen.data.access_test_data import (
    DUPLICATE_USERNAME,
    DUPLICATE_EMAIL,
    WEAK_PASSWORDS,
    BLANK_VALUES
)

def test_duplicate_username(on_user_creation):
    driver, wait = on_user_creation
    # ... fill username with DUPLICATE_USERNAME
    # ... assert error toast appears
```

### 2. Generating random data for positive tests

```python
from pages.access_screen.data.access_test_data import random_user_data

def test_create_user(user_creation_screen):
    driver, wait = user_creation_screen
    data = random_user_data()   # fresh each time
    # ... fill form with data
```

### 3. Using overrides

```python
data = random_user_data(
    username="custom_test_user",
    user_types=["Checker"],
    role="PACS"
)
```

### 4. Single user type scenario

```python
from pages.access_screen.data.access_test_data import random_user_data_single_type

data = random_user_data_single_type()
assert len(data["user_types"]) == 1
```

### 5. DCB‑specific scenario

```python
from pages.access_screen.data.access_test_data import random_user_data_dcb

data = random_user_data_dcb()
assert data["role"] == "DCB"
assert data["entity"] == "dcb1"
```

---

## Relationship with `access_data.py`

| Module | Purpose |
|--------|---------|
| `access_data.py` | Core data generators used by the **module runner** (for manual/sequential test execution). Also defines `USER_TYPES`, `ROLE_ENTITY_MAP`, and `random_user_creation_data()`. |
| `access_test_data.py` | **Test‑specific** data layer. Adds fixed constants (duplicates, weak passwords, blanks) and convenience wrappers for pytest scenarios. **Imports** the core random generator. |

**Why two files?**  
- `access_data.py` is used by the **module runner** (single‑run script) and by the **pytest** tests.  
- `access_test_data.py` is **only used by pytest** tests, providing test‑focused constants and wrappers without cluttering the core `access_data.py`.

---

## Notes

- The duplicate username/email constants (`DUPLICATE_USERNAME`, `DUPLICATE_EMAIL`) must correspond to actual records that exist in the test database **before** the test runs. They are not created automatically.
- The weak password list includes five common failure cases. Not all applications enforce every rule – adjust the list as needed.
- The `BLANK_VALUES` dictionary is useful for **required field validation** tests. You can loop over it to test each field individually.
- All random generators produce **unique** values per call (timestamp + random suffix). However, if two calls happen in the same second and the same random number, a collision is possible – the risk is very low but not zero. For absolute uniqueness, consider adding a counter.
- The `overrides` parameter uses `dict.update()`, so any key present in the original data will be replaced. This allows flexible test customisation without rewriting the entire dictionary.
```