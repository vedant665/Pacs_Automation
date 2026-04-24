"""
auth_helper.py
--------------
Reusable authentication helper — your "auth_section" equivalent.
Call login from any test without repeating code.

Usage in conftest.py (fixture):
    auth = AuthSection(driver)
    auth.login()  # Uses defaults from .env

Usage in tests (manual):
    auth = AuthSection(driver)
    auth.login_as("admin@mail.com", "Admin@123", "admin_facility")
"""

import os
from dotenv import load_dotenv

from pages.login_screens.Login_Screens_.login_page import LoginPage
from common.logger import log


load_dotenv()


class AuthSection:
    """
    Reusable authentication helper class.

    Provides methods to:
    - Login with default credentials from .env
    - Login with custom credentials
    - Login as different user roles
    - Verify login was successful
    """

    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def login(self, email=None, password=None, facility=None):
        """
        Login to PACS application.
        Uses credentials from .env if not provided.
        This is the main method — call it from anywhere.

        Args:
            email: User email (defaults to PACS_EMAIL from .env)
            password: User password (defaults to PACS_PASSWORD from .env)
            facility: Facility name (defaults to PACS_FACILITY from .env)
        """
        # Load defaults from .env if not provided
        email = email or os.getenv("PACS_EMAIL", "")
        password = password or os.getenv("PACS_PASSWORD", "")
        facility = facility or os.getenv("PACS_FACILITY", "")

        if not all([email, password, facility]):
            raise ValueError(
                "Login credentials are missing. "
                "Provide them directly or set them in .env file."
            )

        log.info("Attempting login...")
        log.info(f"  Email   : {email}")
        log.info(f"  Facility: {facility}")

        # Execute login steps
        self.login_page.load()
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.select_facility(facility)
        self.login_page.click_login()

        # Verify login succeeded
        self.login_page.wait_for_login_complete()

        log.info("Login successful!")
        return True

    def login_as(self, email, password, facility):
        """
        Login with specific credentials (for role-based testing).

        Args:
            email: Specific user email
            password: Specific user password
            facility: Specific facility to select

        Example:
            auth = AuthSection(driver)
            auth.login_as("admin@mail.com", "Admin@123", "admin_facility")
        """
        log.info(f"Logging in as: {email}")
        return self.login(email, password, facility)

    def login_default(self):
        """
        Quick login using default .env credentials.
        Shortcut for the most common case.

        Example:
            auth = AuthSection(driver)
            auth.login_default()
        """
        return self.login()
