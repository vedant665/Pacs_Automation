"""
main.py
--------
Quick flow checks for PACS Automation.
NOT for running test cases — use tests/runner.py for that.

Usage:
    python main.py                       → shows help
    python main.py --flow login          → login with dcb1, verify dashboard
    python main.py --flow forgot-password → full forgot password flow (manual OTP)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from common.browser_utils import get_driver, quit_driver
from common.logger import log
from config import (
    LOGIN_URL, BASE_URL,
    PACS_EMAIL, PACS_PASSWORD, PACS_FACILITY,
    FP_EMAIL, FP_CURRENT_PASSWORD, FP_NEW_PASSWORD,
    EXPLICIT_WAIT, PAGE_LOAD_TIMEOUT,
)
from pages.login_screens.Login_Screens_.login_page import LoginPage
from pages.login_screens.Login_Screens_.forgot_password_page import ForgotPasswordPage




def flow_login():
    """Flow Check: Login with dcb1 credentials → verify dashboard loads."""
    log.info("=" * 50)
    log.info("  FLOW CHECK: LOGIN")
    log.info("=" * 50)

    driver = get_driver()
    try:
        # Step 1: Open login page
        log.info("[1/3] Opening login page...")
        login_page = LoginPage(driver)
        driver.get(LOGIN_URL)
        login_page.wait_for_page_load()
        log.passed("Login page loaded")

        # Step 2: Enter credentials and login
        log.info("[2/3] Entering credentials...")
        login_page.enter_email(PACS_EMAIL)
        login_page.enter_password(PACS_PASSWORD)
        login_page.select_facility(PACS_FACILITY)
        login_page.click_login()
        login_page.wait_for_login_complete()
        log.passed("Login completed successfully")

        # Step 3: Verify dashboard
        log.info("[3/3] Verifying dashboard...")
        if "signin" not in driver.current_url.lower():
            log.passed(f"Dashboard reached: {driver.current_url}")
        else:
            log.failed("Login did not complete — still on login page")
            return False

        log.separator()
        log.passed("LOGIN FLOW CHECK — PASSED")
        log.separator()
        return True

    except Exception as e:
        log.failed(f"Login flow failed: {e}")
        return False
    finally:
        quit_driver(driver)


def flow_forgot_password():
    """Flow Check: Forgot Password — email → OTP → reset → success.
    ⚠️ Terminal will prompt you to enter the OTP manually."""
    log.info("=" * 50)
    log.info("  FLOW CHECK: FORGOT PASSWORD")
    log.info("=" * 50)

    driver = get_driver()
    try:
        # Step 1: Open login page and navigate to forgot password
        log.info("[1/5] Opening login page...")
        login_page = LoginPage(driver)
        driver.get(LOGIN_URL)
        login_page.wait_for_page_load()
        log.passed("Login page loaded")

        log.info("[2/5] Navigating to Forgot Password...")
        fp = ForgotPasswordPage(driver)
        fp.navigate_to_forgot_password()
        fp.wait_seconds(2)
        log.passed("Forgot Password page loaded")

        # Step 2: Enter email and send OTP
        log.info("[3/5] Sending OTP to " + FP_EMAIL + "...")
        fp.enter_email(FP_EMAIL)
        fp.click_send_otp()
        fp.wait_seconds(3)

        if not fp.is_otp_screen_displayed():
            log.failed("OTP screen did not appear. Check if email is correct.")
            return False
        log.passed("OTP screen appeared — check your email!")

        # Step 3: Get OTP from user
        log.info("[4/5] Waiting for OTP input...")
        log.info("  ⏳  Check your inbox: " + FP_EMAIL)
        otp = input("  ⏳  Enter the OTP: ").strip()
        while len(otp) != 6 or not otp.isdigit():
            log.failed("OTP must be exactly 6 digits. Try again.")
            otp = input("  ⏳  Enter the OTP: ").strip()
        log.passed(f"OTP entered: {otp[:2]}****")

        # Step 4: Enter new password and reset
        log.info("[5/5] Resetting password...")
        fp.enter_otp(otp)
        fp.enter_new_password(FP_NEW_PASSWORD)
        fp.enter_confirm_password(FP_NEW_PASSWORD)
        fp.click_reset_password()
        fp.wait_seconds(3)

        # Step 5: Verify success
        if fp.is_success_screen_displayed():
            success_text = fp.get_success_message_text()
            log.passed(f"Success: {success_text}")

            # Navigate back to login
            fp.click_login_link_after_success()
            fp.wait_seconds(2)
            if "signin" in driver.current_url.lower():
                log.passed("Returned to login page")

            log.separator()
            log.passed("FORGOT PASSWORD FLOW CHECK — PASSED")
            log.separator()
            return True
        else:
            errors = fp.get_all_error_messages()
            toast = fp.get_toast_message()
            log.failed("Password reset did not succeed.")
            if errors:
                log.info("Errors found: " + " | ".join(errors))
            if toast:
                log.info("Toast message: " + toast)
            return False

    except Exception as e:
        log.failed(f"Forgot password flow failed: {e}")
        return False
    finally:
        quit_driver(driver)


def show_help():
    print("""
╔══════════════════════════════════════════════════╗
║           PACS Automation — main.py              ║
║         Quick Flow Checks (not test suite)       ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  python main.py --flow login                     ║
║      Login with dcb1, verify dashboard loads     ║
║                                                  ║
║  python main.py --flow forgot-password           ║
║      Full forgot password reset (needs OTP)      ║
║      Check your email when prompted              ║
║                                                  ║
║  For test cases with reports, use:               ║
║      python tests/runner.py                      ║
║                                                  ║
╚══════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2 or "--flow" not in sys.argv:
        show_help()
        sys.exit(0)

    flow = sys.argv[sys.argv.index("--flow") + 1].lower() if "--flow" in sys.argv else ""

    if flow == "login":
        success = flow_login()
        sys.exit(0 if success else 1)
    elif flow in ["forgot-password", "forgotpassword", "fp", "forgot"]:
        success = flow_forgot_password()
        sys.exit(0 if success else 1)
    else:
        print(f"\n  Unknown flow: '{flow}'")
        print("  Use: --flow login  or  --flow forgot-password\n")
        sys.exit(1)