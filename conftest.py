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
from pages.login_page import LoginPage
from config import REPORT_DIR


# ================================================================
# TEST RESULT STORAGE (for Excel report)
# ================================================================

test_results = []


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

def pytest_configure(config):
    """Runs before test session starts."""
    log.separator("=")
    log.info(" PACS AUTOMATION TEST SUITE")
    log.info(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.separator("=")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture test results for Excel report.
    Also takes a screenshot automatically when a test FAILS.
    """
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
    if test_results:
        try:
            from common.report_generator import generate_report
            filepath = generate_report(test_results, output_dir=REPORT_DIR)
            log.separator()
            log.info(f" EXCEL REPORT GENERATED: {filepath}")
            log.separator()
        except Exception as e:
            log.error(f"Failed to generate Excel report: {e}")