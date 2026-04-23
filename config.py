"""
config.py
---------
Central configuration for PACS Automation Project.
All URLs, timeouts, paths, and settings are defined here.
Other modules import from this file — change once, reflects everywhere.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# APPLICATION URLs
# ============================================================
BASE_URL = os.getenv("PACS_BASE_URL", "https://pacsdev.algorhythms.in")
LOGIN_URL = f"{BASE_URL}/#/authentication/signin"
FORGOT_PASSWORD_URL = f"{BASE_URL}/#/authentication/forgot-password"

MODULE_BASE_URL = os.getenv("MODULE_BASE_URL", "https://pacstest.algorhythms.in")
MODULE_LOGIN_URL = MODULE_BASE_URL


# ============================================================
# LOGIN CREDENTIALS (loaded from .env)
# ============================================================
PACS_EMAIL = os.getenv("PACS_EMAIL", "")
PACS_PASSWORD = os.getenv("PACS_PASSWORD", "")
PACS_FACILITY = os.getenv("PACS_FACILITY", "")


# ============================================================
# FORGOT PASSWORD CREDENTIALS (loaded from .env)
# ============================================================
FP_EMAIL = os.getenv("FP_EMAIL", "")
FP_CURRENT_PASSWORD = os.getenv("FP_CURRENT_PASSWORD", "")
FP_NEW_PASSWORD = os.getenv("FP_NEW_PASSWORD", "")
FP_ALT_PASSWORD = os.getenv("FP_ALT_PASSWORD", "")
FP_USERNAME = os.getenv("FP_USERNAME", "")
FP_TENANT = os.getenv("FP_TENANT", "")
FP_OLD_PASSWORDS = [
    os.getenv("FP_OLD_PASSWORD_1", ""),
    os.getenv("FP_OLD_PASSWORD_2", ""),
    os.getenv("FP_OLD_PASSWORD_3", ""),
]


# ============================================================
# BROWSER SETTINGS
# ============================================================
BROWSER = os.getenv("BROWSER", "chrome").lower()  # "chrome" or "edge"
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


# ============================================================
# TIMEOUTS (in seconds)
# ============================================================
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
IMPLICIT_WAIT = 5


# ============================================================
# DIRECTORY PATHS (relative to project root)
# ============================================================
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Ensure directories exist
for directory in [SCREENSHOT_DIR, REPORT_DIR, DATA_DIR]:
    os.makedirs(directory, exist_ok=True)


# ============================================================
# REPORT SETTINGS
# ============================================================
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")