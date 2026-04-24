"""
access_test_data.py
-------------------
Centralized test data for Access Screen pytest tests.

Contains:
- Duplicate values (username, email) for negative tests
- Weak passwords for validation tests
- Blank/empty values for negative tests
- Helper to generate random user data for positive tests

Import random data generators from access_data.py (used by module runner).
"""

import random
from datetime import datetime

from pages.access_screen.data.access_data import (
    USER_TYPES,
    ROLE_ENTITY_MAP,
    random_user_creation_data,
)


# ================================================================
# FIXED VALUES — for negative / validation tests
# ================================================================

DUPLICATE_USERNAME = "7686uyfthft"
DUPLICATE_EMAIL = "vedant@rhythmflows.com"

VALID_PASSWORD = "Test@1234567"

WEAK_PASSWORDS = {
    "too_short": "Ved@1",
    "no_uppercase": "vedant@12345",
    "no_lowercase": "VEDANT@12345",
    "no_number": "Vedant@abcdx",
    "no_special": "Vedant123456",
}

BLANK_VALUES = {
    "username": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "password": "",
}


# ================================================================
# RANDOM DATA GENERATORS — for positive tests
# ================================================================

def random_username():
    """Generate a unique username using timestamp + random number."""
    timestamp = datetime.now().strftime("%H%M%S")
    number = random.randint(10, 99)
    return f"testuser{timestamp}{number}"


def random_email():
    """Generate a unique email matching the username pattern."""
    return f"{random_username()}@mail.com"


def random_user_data(**overrides):
    """Generate random user creation data with optional overrides.

    Uses the same ROLE_ENTITY_MAP from access_data.py to ensure
    role and entity are always paired correctly.

    Args:
        overrides: Any key from random_user_creation_data() to override.

    Returns:
        dict with keys: username, email, first_name, last_name,
                        password, user_types, role, entity
    """
    data = random_user_creation_data()
    if overrides:
        data.update(overrides)
    return data


def random_user_data_single_type(**overrides):
    """Generate random user data with only ONE user type (not multi-select)."""
    data = random_user_creation_data()
    data["user_types"] = [random.choice(USER_TYPES)]
    if overrides:
        data.update(overrides)
    return data


def random_user_data_dcb(**overrides):
    """Generate random user data locked to DCB role + dcb1 entity."""
    data = random_user_creation_data()
    data["role"] = "DCB"
    data["entity"] = "dcb1"
    if overrides:
        data.update(overrides)
    return data
