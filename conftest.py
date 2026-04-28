"""
conftest.py
-----------
pytest configuration — fixtures that run automatically.

Fixtures provided:
- driver          : Launches browser, available to all tests
- login_page      : LoginPage object (not logged in)
- auth_section    : AuthSection helper (for manual login calls)
- logged_in_driver: Driver with completed login session

How it works:
1. pytest runs conftest.py BEFORE any test file
2. When a test has 'driver' as parameter → browser launches
3. When a test has 'logged_in_driver' → browser launches + login happens
4. After tests finish → browser closes AND Excel report is generated
"""

import os
import sys
import pytest
from datetime import datetime

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.logger import log
from common.browser_utils import get_driver
from common.auth_helper import AuthSection
from pages.login_screens.Login_Screens_.login_page import LoginPage
from config import REPORT_DIR


# ================================================================
# TEST RESULT STORAGE (for Excel report)
# ================================================================

test_results = []


# ================================================================
# FORGOT PASSWORD TEST DESCRIPTIONS
# ================================================================

FP_DESCRIPTIONS = {
    "test_fp_s1_01": {
        "name": "Unregistered Email Proceeds",
        "question": "Does the app proceed to OTP screen even for an email that doesn't exist in the system?",
    },
    "test_fp_s1_02": {
        "name": "Valid Email Sends OTP",
        "question": "Does a valid registered email trigger OTP delivery and navigate to the OTP screen?",
    },
    "test_fp_s1_03": {
        "name": "Blank Email Submission",
        "question": "Does clicking Send OTP without entering an email show a validation error or alert?",
    },
    "test_fp_s1_04": {
        "name": "Email with Spaces Trimmed",
        "question": "Does the app handle emails with leading/trailing spaces — trim them and proceed?",
    },
    "test_fp_s1_05": {
        "name": "Email Case Insensitive",
        "question": "Does the app treat uppercase and lowercase emails the same way?",
    },
    "test_fp_s1_06": {
        "name": "Double-Click Send OTP Safe",
        "question": "Does rapid double-clicking Send OTP cause issues like duplicate OTPs or crashes?",
    },
    "test_fp_s2_01": {
        "name": "Invalid OTP Shows Alert",
        "question": "Does entering a wrong OTP code show an error alert?",
    },
    "test_fp_s2_02": {
        "name": "Password Mismatch Shows Alert",
        "question": "Does entering different passwords in New Password and Confirm Password show an error?",
    },
    "test_fp_s2_03": {
        "name": "Password Policy Hints Visible",
        "question": "Do password policy hints (min 12 chars, uppercase, etc.) appear when typing a weak password?",
    },
    "test_fp_s2_04": {
        "name": "Recently Used Password Alert",
        "question": "Does the app show an error when trying to reset to a recently used password?",
    },
    "test_fp_ff_01": {
        "name": "Browser Back from OTP Screen",
        "question": "Does pressing browser back on the OTP screen return to email entry or login?",
    },
    "test_fp_ff_02": {
        "name": "Back to Login from Screen 1",
        "question": "Does clicking 'Back to Login' on Screen 1 return to the login page?",
    },
    "test_fp_ff_03": {
        "name": "Grand Finale: Reset → Login → Dashboard",
        "question": "THE BIG ONE: Full forgot password flow — reset password, login with new password, reach dashboard?",
    },
    "test_fp_ff_04": {
        "name": "Recently Used Password Rejected",
        "question": "Does the app reject a password that was just used in the previous reset?",
    },
    "test_fp_ff_05": {
        "name": "Current Password Rejected",
        "question": "Does the app reject setting the same password as the current one?",
    },
    "test_fp_ff_06": {
        "name": "Cleanup: Reset to Default Password",
        "question": "Does the cleanup reset the password back to the default so next test run starts clean?",
    },
}

FP_CATEGORIES = {
    "TestForgotPasswordScreen1": "Screen 1 / Email Entry",
    "TestForgotPasswordScreen2": "Screen 2 / OTP & Password",
    "TestForgotPasswordFullFlow": "Full Flow",
}


# ================================================================
# BROWSER FIXTURE
# ================================================================

@pytest.fixture(scope="session")
def driver():
    """
    Launch browser ONCE for the entire test session.
    All tests in the session share this browser instance.
    Browser closes after ALL tests are done.
    """
    log.separator()
    log.info("LAUNCHING BROWSER...")
    log.separator()

    driver = get_driver()

    yield driver  # Tests run here

    # Teardown — runs after all tests finish
    log.separator()
    log.info("CLOSING BROWSER...")
    log.separator()
    try:
        driver.quit()
        log.info("Browser closed successfully")
    except Exception as e:
        log.error(f"Error closing browser: {e}")


# ================================================================
# PAGE OBJECT FIXTURES
# ================================================================

@pytest.fixture
def login_page(driver):
    """
    Provide a LoginPage object (not logged in).
    Use this when you want to TEST the login page itself.
    """
    page = LoginPage(driver)
    return page


@pytest.fixture
def auth_section(driver):
    """
    Provide an AuthSection helper object.
    Use this when you need manual control over login in tests.
    """
    auth = AuthSection(driver)
    return auth


# ================================================================
# AUTHENTICATED SESSION FIXTURE
# ================================================================

@pytest.fixture(scope="session")
def logged_in_driver(driver):
    """
    Driver with completed login session.
    Use this when testing features AFTER login.

    Usage in test:
        def test_dashboard(logged_in_driver):
            # Already logged in! Go straight to testing.
            driver = logged_in_driver
            ...

    This fixture logs in ONCE for the entire session.
    All tests using this fixture share the same logged-in session.
    """
    log.separator()
    log.info("PERFORMING SESSION LOGIN...")
    log.separator()

    auth = AuthSection(driver)
    try:
        auth.login_default()
        log.info("Session login successful!")
    except Exception as e:
        log.error(f"Session login failed: {e}")
        raise

    yield driver  # Tests run with logged-in browser


# ================================================================
# PYTEST HOOKS
# ================================================================

def _is_login_suite(session):
    """Check if tests belong to a module with its own conftest hooks."""
    items = getattr(session, "items", None)
    if not items:
        return False
    # Skip for login tests (have own conftest) and company_onboarding (have own conftest)
    return all(
        "Test_cases_login" in item.nodeid or "company_onboarding" in item.nodeid
        for item in items
    )


def pytest_configure(config):
    """Runs before test session starts."""
    # Skip header when running login tests — they have their own conftest
    if hasattr(config, "session") and _is_login_suite(config.session):
        return
    log.separator("=")
    log.info(" RHYTHMERP FORGOT PASSWORD TEST SUITE")
    log.info(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.separator("=")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture test results for Excel report.
    Also takes a screenshot automatically when a test FAILS.
    Skips when running login tests — they have their own conftest.
    """
    # Skip — login tests have their own conftest hooks
    if "Test_cases_login" in item.nodeid:
        outcome = yield
        return

    outcome = yield
    report = outcome.get_result()

    # Only capture during the "call" phase (actual test execution)
    if report.when == "call":
        result = {
            "nodeid": item.nodeid,
            "status": "PASSED" if report.passed else "FAILED",
            "message": str(report.longrepr) if report.failed else "",
            "duration": report.duration,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "screenshot": "",
        }

        # If test failed, take screenshot
        if report.failed:
            driver = None
            for fixture_name in ["driver", "logged_in_driver"]:
                if fixture_name in item.funcargs:
                    driver = item.funcargs[fixture_name]
                    break

            if driver:
                try:
                    login_page = LoginPage(driver)
                    os.makedirs(REPORT_DIR, exist_ok=True)
                    shot_name = f"FAILED_{item.name}"
                    shot_path = login_page.take_screenshot(shot_name)
                    result["screenshot"] = shot_path
                    log.error(f"Failure screenshot saved: {shot_path}")
                except Exception as e:
                    log.error(f"Could not take failure screenshot: {e}")

        test_results.append(result)


def pytest_sessionfinish(session, exitstatus):
    """Generate Excel report after all tests complete."""
    # Skip — login tests have their own conftest hooks
    if _is_login_suite(session):
        return

    if test_results:
        try:
            from common.report_generator import generate_report
            filepath = generate_report(
                test_results,
                output_dir=REPORT_DIR,
                title="RhythmERP Forgot Password Tests",
                filename_prefix="RhythmERPForgotPassword",
                descriptions=FP_DESCRIPTIONS,
                categories=FP_CATEGORIES,
            )
            log.separator()
            log.info(f" EXCEL REPORT GENERATED: {filepath}")
            log.separator()
        except Exception as e:
            log.error(f"Failed to generate Excel report: {e}")