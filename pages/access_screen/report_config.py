"""
Report Config for Access Screen Module (User Creation)
======================================================
This file holds User Creation test descriptions and category mappings.
Imported by the access screen conftest.py and passed to the report engine.
"""

# ─── Report Settings ─────────────────────────────────────────────────────────

REPORT_TITLE = "Access Screen — User Creation"
FILENAME_PREFIX = "UserCreation"


# ─── Test Descriptions (for Test Guide sheet) ────────────────────────────────
# Keys must match the test function names in user_creation_test.py
# Format: "name" = short label, "question" = human-readable what-we-checked

UC_DESCRIPTIONS = {
    # ── Positive Tests (TestUserCreationPositive) ──
    "test_create_user_with_valid_data": {
        "name": "Valid User Creation",
        "question": "Can a new user be created with all correct fields — username, email, password, user type, role, and entity?",
    },
    "test_create_user_with_all_user_types": {
        "name": "All User Types",
        "question": "Does the User Type dropdown have the expected options (e.g. Admin, Staff, etc.) and does each one work?",
    },
    "test_create_user_active_checkbox_default": {
        "name": "Active Checkbox Default",
        "question": "Is the 'Active' checkbox pre-checked by default when the form opens?",
    },

    # ── Validation Tests (TestUserCreationValidation) ──
    "test_duplicate_username_error": {
        "name": "Duplicate Username",
        "question": "Does the app show an error toast if you try to create a user with a username that already exists?",
    },
    "test_duplicate_email_error": {
        "name": "Duplicate Email",
        "question": "Does the app show an error toast if you try to create a user with an email that already exists?",
    },
    "test_weak_password_rejection": {
        "name": "Weak Password",
        "question": "Does the app block passwords that don't meet the rules (12+ chars, uppercase, lowercase, number, special char)?",
    },
    "test_blank_fields_validation": {
        "name": "Blank Required Fields",
        "question": "Does the app show red borders on required fields if you try to submit without filling them?",
    },

    # ── Dropdown Tests (TestUserCreationDropdown) ──
    "test_user_type_dropdown_options": {
        "name": "Dropdown Options Present",
        "question": "Are all expected options showing up in the key dropdowns (User Type, Role, Entity)?",
    },
}


# ─── Category Map (for Summary sheet) ────────────────────────────────────────
# Maps test class names → category labels

UC_CATEGORIES = {
    "TestUserCreationPositive": "Positive Tests",
    "TestUserCreationValidation": "Validation Tests",
    "TestUserCreationDropdown": "Dropdown Tests",
}