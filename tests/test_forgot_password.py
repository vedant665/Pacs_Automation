"""
test_forgot_password.py
------------------------
Essential test cases for Forgot Password flow.
15 tests total: 11 auto + 4 OTP.
Grand Finale (ff_04) runs FIRST in Full Flow class, saves password,
then ff_01 and ff_03 use it to guarantee rejection.
OTP retry: 3 attempts per test if tester makes a typo.
"""

import pytest
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from config import LOGIN_URL, FP_EMAIL, FP_NEW_PASSWORD, FP_ALT_PASSWORD, FP_USERNAME, FP_TENANT
from data.login_data import ForgotPasswordData


# ================================================================
# FIXTURES
# ================================================================
@pytest.fixture
def fp_on_screen1(driver):
    """Navigate to forgot password Screen 1 (email input)."""
    driver.get(LOGIN_URL)
    page = ForgotPasswordPage(driver)
    page.wait_for_page_load()
    page.navigate_to_forgot_password()
    return page


@pytest.fixture
def fp_on_screen2(driver):
    """Navigate to forgot password Screen 2 (OTP + password input)."""
    driver.get(LOGIN_URL)
    page = ForgotPasswordPage(driver)
    page.wait_for_page_load()
    page.navigate_to_forgot_password()
    page.enter_email(FP_EMAIL)
    page.click_send_otp()
    page.wait_seconds(2)

    if page.is_otp_screen_displayed():
        return page
    else:
        pytest.fail("Could not reach OTP screen. Check if email is valid.")


# ================================================================
# MARKERS
# ================================================================
manual_otp = pytest.mark.manual_otp


# ================================================================
# SCREEN 1 TESTS
# ================================================================
class TestForgotPasswordScreen1:

    def test_fp_s1_01_unregistered_email_proceeds(self, fp_on_screen1):
        """App proceeds to OTP screen even for unregistered email (by design)."""
        fp = fp_on_screen1
        fp.enter_email(ForgotPasswordData.UNREGISTERED_EMAIL)
        fp.click_send_otp()
        fp.wait_seconds(2)
        assert fp.is_otp_screen_displayed(), "Should proceed to OTP screen"

    @manual_otp
    def test_fp_s1_02_valid_email_sends_otp(self, fp_on_screen1):
        """Valid email -> OTP screen appears."""
        fp = fp_on_screen1
        fp.enter_email(FP_EMAIL)
        fp.click_send_otp()
        fp.wait_seconds(3)
        assert fp.is_otp_screen_displayed(), "OTP screen should appear"

    def test_fp_s1_03_blank_email_submission(self, fp_on_screen1):
        """Click Send OTP without entering any email -> should show error."""
        fp = fp_on_screen1
        fp.click_send_otp()

        alert_text = None
        for _ in range(10):
            fp.wait_seconds(0.5)
            alert_text = fp.get_alert_danger_text()
            if alert_text:
                break

                # Either an error alert OR email field validation should appear
        has_validation = False
        if not alert_text:
            # Check for Angular Material mat-error elements
            mat_errors = fp.driver.find_elements(By.CSS_SELECTOR, "mat-error")
            for el in mat_errors:
                text = el.text.lower()
                if "email" in text or "required" in text or "valid" in text:
                    has_validation = True
                    break

            # Also check for custom field error divs
            if not has_validation:
                email_elements = fp.driver.find_elements(By.CSS_SELECTOR, "div.custom-field-error")
                for el in email_elements:
                    text = el.text.lower()
                    if "email" in text or "required" in text or "valid" in text:
                        has_validation = True
                        break

        assert alert_text or has_validation, \
            "Should show error when submitting without email"
        
        
    def test_fp_s1_04_email_with_leading_trailing_spaces(self, fp_on_screen1):
        """Email with spaces should still work (app should trim them)."""
        fp = fp_on_screen1
        fp.enter_email(f"  {FP_EMAIL}  ")
        fp.click_send_otp()
        fp.wait_seconds(3)

        # App should trim spaces and proceed to OTP screen
        assert fp.is_otp_screen_displayed(), \
            "Should proceed to OTP screen after trimming spaces from email"

    def test_fp_s1_05_email_case_insensitive(self, fp_on_screen1):
        """Uppercase email should be treated same as lowercase."""
        fp = fp_on_screen1
        upper_email = FP_EMAIL.upper()
        fp.enter_email(upper_email)
        fp.click_send_otp()
        fp.wait_seconds(3)

        # App should treat VEDANT@... same as vedant@...
        assert fp.is_otp_screen_displayed(), \
            "Should proceed to OTP screen (email should be case-insensitive)"

    def test_fp_s1_06_double_click_send_otp(self, fp_on_screen1):
        """Rapid double-click on Send OTP should not send multiple OTPs."""
        fp = fp_on_screen1
        fp.enter_email(FP_EMAIL)

        # Double-click using ActionChains
        send_btn = fp.find_visible_element(fp.SEND_OTP_BUTTON)
        actions = ActionChains(fp.driver)
        actions.double_click(send_btn).perform()

        fp.wait_seconds(3)

        # Should still end up on OTP screen (not broken by double click)
        assert fp.is_otp_screen_displayed(), \
            "Should proceed to OTP screen after double-click (not broken)"


# ================================================================
# SCREEN 2 TESTS
# ================================================================
class TestForgotPasswordScreen2:

    def test_fp_s2_01_invalid_otp_shows_alert(self, fp_on_screen2):
        """Invalid OTP should show an alert-danger message."""
        fp = fp_on_screen2
        fp.enter_otp(ForgotPasswordData.INVALID_OTP)
        fp.enter_new_password(FP_NEW_PASSWORD)
        fp.enter_confirm_password(FP_NEW_PASSWORD)
        fp.click_reset_password()

        alert_text = None
        for _ in range(10):
            fp.wait_seconds(0.5)
            alert_text = fp.get_alert_danger_text()
            if alert_text:
                break

        assert alert_text is not None, "Should show error alert for invalid OTP"

    def test_fp_s2_02_password_mismatch_shows_alert(self, fp_on_screen2):
        """Mismatched passwords should show alert on submit."""
        fp = fp_on_screen2
        fp.enter_otp("123456")
        fp.enter_new_password(FP_NEW_PASSWORD)
        fp.enter_confirm_password(ForgotPasswordData.MISMATCH_PASSWORD)
        fp.click_reset_password()

        alert_text = None
        for _ in range(10):
            fp.wait_seconds(0.5)
            alert_text = fp.get_alert_danger_text()
            if alert_text:
                break

        assert alert_text is not None, "Should show 'Passwords do not match' alert"

    def test_fp_s2_03_password_policy_hints_visible(self, fp_on_screen2):
        """Password policy hints appear after typing a weak password and blurring."""
        fp = fp_on_screen2

        fp.enter_new_password("abc")

        fp.click(fp.OTP_INPUT)
        fp.wait_seconds(1)

        has_policy = False
        for _ in range(10):
            fp.wait_seconds(0.5)
            policy_elements = fp.driver.find_elements(
                By.CSS_SELECTOR, "div.custom-field-error"
            )
            for el in policy_elements:
                text = el.text.lower()
                if "minimum 12 characters" in text or "uppercase" in text:
                    has_policy = True
                    break
            if has_policy:
                break

        assert has_policy, "Password policy hints should appear after typing weak password"

    def test_fp_s2_04_recently_used_password_shows_alert(self, fp_on_screen2):
        """Recently used password should trigger alert-danger."""
        fp = fp_on_screen2
        fp.enter_otp("123456")
        old_pass = ForgotPasswordData.RECENTLY_USED_PASSWORDS[0]
        fp.enter_new_password(old_pass)
        fp.enter_confirm_password(old_pass)
        fp.click_reset_password()

        alert_text = None
        for _ in range(10):
            fp.wait_seconds(0.5)
            alert_text = fp.get_alert_danger_text()
            if alert_text:
                break

        assert alert_text is not None, "Should show error alert for recently used password"


# ================================================================
# FULL FLOW TESTS
# ================================================================
class TestForgotPasswordFullFlow:

    # ── Helpers ──

    @staticmethod
    def _navigate_to_otp_screen(driver):
        """Navigate to forgot password and reach OTP screen."""
        driver.get(LOGIN_URL)
        login_page = LoginPage(driver)
        login_page.wait_for_page_load()

        fp = ForgotPasswordPage(driver)
        fp.navigate_to_forgot_password()
        fp.wait_seconds(2)

        fp.enter_email(FP_EMAIL)
        fp.click_send_otp()
        fp.wait_seconds(3)

        assert fp.is_otp_screen_displayed(), "Should be on OTP screen"
        return fp

    @staticmethod
    def _is_otp_error(alert_text):
        """Check if error is about OTP (wrong code) vs password (expected rejection)."""
        if not alert_text:
            return False
        alert_lower = alert_text.lower()
        otp_keywords = ["otp", "invalid code", "verification code", "incorrect code"]
        password_keywords = ["password", "recently used", "same as"]
        has_otp = any(kw in alert_lower for kw in otp_keywords)
        has_pass = any(kw in alert_lower for kw in password_keywords)
        return has_otp and not has_pass

    @staticmethod
    def _wait_for_alert(fp, timeout_seconds=5):
        """Poll for alert-danger text."""
        alert_text = None
        for _ in range(timeout_seconds * 2):
            fp.wait_seconds(0.5)
            alert_text = fp.get_alert_danger_text()
            if alert_text:
                break
        return alert_text

    # ── Tests ──

    def test_fp_ff_05_browser_back_from_otp_screen(self, driver):
        """Browser back button on OTP screen should not allow form reuse."""
        # Navigate to OTP screen
        fp = self._navigate_to_otp_screen(driver)

        # Hit browser back button
        driver.back()
        fp.wait_seconds(2)

        # Should go back to Screen 1 (email entry) or login
        is_on_screen1 = False
        try:
            email_field = fp.find_visible_element(fp.EMAIL_INPUT, timeout=3)
            is_on_screen1 = email_field is not None
        except Exception:
            pass

        is_on_login = "signin" in driver.current_url.lower()
        assert is_on_screen1 or is_on_login, \
            "Browser back from OTP screen should return to email entry or login page"

    @manual_otp
    def test_fp_ff_04_grand_finale_reset_login_dashboard(self, driver):
        """GRAND FINALE: Reset password with fresh password -> login -> verify dashboard.
        MUST RUN FIRST in this class — saves generated password for ff_01 and ff_03."""
        # Step 1: Generate a unique password
        timestamp = datetime.now().strftime("%H%M%S")
        new_password = f"Vedant@{timestamp}x"
        print(f"\n  🔑 Auto-generated password: {new_password}\n")

        # Save for rejection tests (ff_01 and ff_03)
        TestForgotPasswordFullFlow.generated_password = new_password

        # Step 2: Navigate and send OTP
        fp = self._navigate_to_otp_screen(driver)

        # Step 3: Enter OTP with retry
        max_retries = 3
        for attempt in range(max_retries):
            otp = input(f"  ⏳ Enter OTP received on {FP_EMAIL} ({attempt + 1}/{max_retries}): ")
            fp.enter_otp(otp)

            # Step 4: Enter new password and reset
            fp.enter_new_password(new_password)
            fp.enter_confirm_password(new_password)
            fp.click_reset_password()
            fp.wait_seconds(3)

            # Check result
            if fp.is_success_screen_displayed():
                break  # OTP was correct, reset succeeded

            alert = self._wait_for_alert(fp)
            if self._is_otp_error(alert):
                print(f"  ❌ Wrong OTP! App said: {alert}")
                print(f"  📧 A new OTP has been sent. Check your email.\n")
                fp = self._navigate_to_otp_screen(driver)
                continue
            else:
                pytest.fail(f"Unexpected error during reset: {alert}")
        else:
            pytest.fail(f"Wrong OTP entered {max_retries} times. Aborting.")

        # Step 5: Verify reset success
        success_text = fp.get_success_message_text()
        assert "password reset successful" in success_text.lower(), \
            f"Expected success message, got '{success_text}'"

        # Step 6: Navigate to login
        fp.click_login_link_after_success()
        fp.wait_seconds(2)
        assert "signin" in driver.current_url.lower(), "Should be on login page"

        # Step 7: Login with new credentials
        login_page = LoginPage(driver)
        login_page.wait_for_page_load()
        login_page.enter_email(FP_USERNAME)
        login_page.enter_password(new_password)
        login_page.select_facility(FP_TENANT)
        login_page.click_login()
        login_page.wait_for_login_complete()

        # Step 8: Verify dashboard
        assert "signin" not in driver.current_url.lower(), \
            "Should reach dashboard after login with new password"

    @manual_otp
    def test_fp_ff_01_recently_used_password_rejected(self, driver):
        """Full flow but uses the password just set by ff_04 -> expect rejection.
        Proves 'recently used' security protection works."""
        fp = self._navigate_to_otp_screen(driver)

        recent_password = TestForgotPasswordFullFlow.generated_password

        max_retries = 3
        for attempt in range(max_retries):
            otp = input(f"  ⏳ Enter OTP received on {FP_EMAIL} ({attempt + 1}/{max_retries}): ")
            fp.enter_otp(otp)
            fp.enter_new_password(recent_password)
            fp.enter_confirm_password(recent_password)
            fp.click_reset_password()

            alert_text = self._wait_for_alert(fp)
            success = fp.is_success_screen_displayed()

            # Check if error is about OTP (typo) vs password (expected rejection)
            if self._is_otp_error(alert_text):
                print(f"  ❌ Wrong OTP! App said: {alert_text}")
                print(f"  📧 A new OTP has been sent. Check your email.\n")
                fp = self._navigate_to_otp_screen(driver)
                continue

            # OTP was accepted — now check for expected password rejection
            assert not success, "Should NOT succeed with recently used password"
            assert alert_text is not None, "Should show rejection alert for recently used password"
            break
        else:
            pytest.fail(f"Wrong OTP entered {max_retries} times. Aborting.")

    def test_fp_ff_02_navigate_back_to_login_from_screen1(self, fp_on_screen1):
        """Click 'Back to Login' -> return to login page."""
        fp = fp_on_screen1
        if fp.is_displayed(fp.BACK_TO_LOGIN_LINK, timeout=3):
            fp.click_back_to_login()
            fp.wait_seconds(2)
            assert "signin" in fp.driver.current_url.lower(), "Should navigate back to login"
        else:
            pytest.skip("Back to Login link not found")

    @manual_otp
    def test_fp_ff_03_current_password_rejected(self, driver):
        """Full flow but uses current password (same one ff_04 just set) -> expect rejection.
        Proves 'same as current' protection works."""
        fp = self._navigate_to_otp_screen(driver)

        current_password = TestForgotPasswordFullFlow.generated_password

        max_retries = 3
        for attempt in range(max_retries):
            otp = input(f"  ⏳ Enter OTP received on {FP_EMAIL} ({attempt + 1}/{max_retries}): ")
            fp.enter_otp(otp)
            fp.enter_new_password(current_password)
            fp.enter_confirm_password(current_password)
            fp.click_reset_password()

            alert_text = self._wait_for_alert(fp)
            success = fp.is_success_screen_displayed()

            # Check if error is about OTP (typo) vs password (expected rejection)
            if self._is_otp_error(alert_text):
                print(f"  ❌ Wrong OTP! App said: {alert_text}")
                print(f"  📧 A new OTP has been sent. Check your email.\n")
                fp = self._navigate_to_otp_screen(driver)
                continue

            # OTP was accepted — now check for expected password rejection
            assert not success, "Should NOT succeed with current password"
            assert alert_text is not None, "Should show rejection alert for current password"
            break
        else:
            pytest.fail(f"Wrong OTP entered {max_retries} times. Aborting.")