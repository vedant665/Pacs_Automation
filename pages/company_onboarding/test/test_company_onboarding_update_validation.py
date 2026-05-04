"""
Company Onboarding UPDATE Validation Tests.
Target company: Zenith Core Systems

Tests:
  01 - Form Opens
  02 - Step 1 Next-click validations (required + format + non-required) [ONE form open]
  03 - 2FA + Auth Type dependency
  04 - Duplicate Company Name SweetAlert (Update click)
  05 - Invalid CIN SweetAlert (Update click)
  06 - Max Length SweetAlert (Update click)
"""

import os
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from common.logger import log
from pages.company_onboarding.Company_Onboarding.company_onboarding_page_update import CompanyOnboardingUpdatePage
from pages.company_onboarding.test.update_validation_results_store import update_validation_results

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "pages", "company_onboarding", "screenshots")
REPORT_DIR = os.path.join(PROJECT_ROOT, "pages", "company_onboarding", "reports")

TEST_COMPANY = "Zenith Core Systems"


class TestUpdateValidation:

    # ================================================================
    # HELPERS
    # ================================================================

    def _page(self, driver):
        return CompanyOnboardingUpdatePage(driver)

    def _screenshot(self, driver, name):
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        path = os.path.join(SCREENSHOT_DIR,
                            f"upd_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        driver.save_screenshot(path)
        return path

    def _record(self, test_name, expected, actual, status, category="",
                 field="", bad_value="", original_value="", screenshot="", is_bug=False):
        """Record a test result for the Excel report."""
        update_validation_results.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "test_name": test_name,
            "expected": expected,
            "actual": actual,
            "status": status,
            "category": category,
            "field": field,
            "bad_value": bad_value,
            "original_value": original_value,
            "screenshot": screenshot,
            "is_bug": is_bug,
        })

    # ---- Form open / cleanup ----

    def _open_form(self, page):
        page.driver.refresh()
        time.sleep(1.5)
        page.navigate_to_page()
        time.sleep(1.5)
        page.search_company(TEST_COMPANY)
        time.sleep(1)
        page._click_edit_button(TEST_COMPANY)
        time.sleep(3)  # form needs time to fully render all fields

    def _cleanup(self, page):
        try:
            # Dismiss any open dialogs/overlays first
            page._force_close_panels()
        except Exception:
            pass
        page.navigate_to_page()
        time.sleep(1)

    # ---- Field helpers ----

    def _clear_field(self, driver, field_name, tag="input"):
        """Clear a field using Ctrl+A -> Delete -> Tab (triggers ng-touched)."""
        el = driver.find_element(By.CSS_SELECTOR, f"{tag}[name='{field_name}']")
        try:
            el.click()
        except Exception:
            driver.execute_script("arguments[0].focus();", el)
        time.sleep(0.2)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.DELETE)
        time.sleep(0.3)
        el.send_keys(Keys.TAB)  # THE FIX: triggers ng-touched in Angular
        time.sleep(0.3)

    def _type_field(self, driver, field_name, value, tag="input"):
        """Type a value into a field using Ctrl+A -> type -> Tab (triggers ng-touched)."""
        el = driver.find_element(By.CSS_SELECTOR, f"{tag}[name='{field_name}']")
        try:
            el.click()
        except Exception:
            driver.execute_script("arguments[0].focus();", el)
        time.sleep(0.2)
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(value)
        time.sleep(0.3)
        el.send_keys(Keys.TAB)
        time.sleep(0.3)

    def _check_field_invalid(self, driver, field_name, tag="input"):
        """Check if Angular marks a field as invalid (ng-invalid + ng-touched)."""
        try:
            input_el = driver.find_element(By.CSS_SELECTOR, f"{tag}[name='{field_name}']")
            classes = input_el.get_attribute("class") or ""
            is_invalid = "ng-invalid" in classes and "ng-touched" in classes
            error_id = input_el.get_attribute("aria-describedby") or ""
            error_text = ""
            if error_id:
                try:
                    err_el = driver.find_element(By.ID, error_id)
                    error_text = err_el.text.strip()
                except Exception:
                    pass
            return is_invalid, error_text
        except Exception:
            return False, ""

    def _read_field(self, page, locator):
        return page._read_text_field(locator)

    # ---- SweetAlert helpers ----

    def _check_sweetalert(self, driver, timeout=8):
        """Wait for SweetAlert and return (title, has_download_button)."""
        try:
            title_el = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#swal2-title"))
            )
            title_text = title_el.text.strip()
            has_download = bool(driver.find_elements(
                By.CSS_SELECTOR, ".swal2-confirm"))
            return title_text, has_download
        except Exception:
            return "", False

    def _dismiss_sweetalert(self, driver):
        """Click Cancel on SweetAlert to dismiss."""
        try:
            cancel_btn = driver.find_element(By.CSS_SELECTOR, ".swal2-cancel")
            driver.execute_script("arguments[0].click();", cancel_btn)
            time.sleep(0.5)
        except Exception:
            pass

    # ---- Navigation helpers ----

    def _click_update_direct(self, driver):
        """Click Update button directly from Step 1 -- no need to navigate all steps."""
        try:
            update_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[@class='popup-footer']//button[contains(.,'Update')]"
                ))
            )
        except Exception:
            update_btn = driver.find_element(
                By.XPATH,
                "//div[@class='popup-footer']//button[contains(.,'Submit')]"
            )
        driver.execute_script("arguments[0].click();", update_btn)
        time.sleep(2)

    def _go_back_if_needed(self, page):
        """If Next succeeded (moved to Step 2), click Back to return to Step 1."""
        try:
            # Check if we're on Step 2 (promoter name visible)
            WebDriverWait(page.driver, 3).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//app-dynamic-details//input[@name='Name']")
                )
            )
            # We're on Step 2 -- find and click Back button
            back_btn = WebDriverWait(page.driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@matstepperprevious or @matStepperPrevious]"
                    " | //button[normalize-space(.)='Back']"
                ))
            )
            page.driver.execute_script("arguments[0].click();", back_btn)
            time.sleep(0.8)
            return True
        except Exception:
            return False

    def _is_on_step2(self, driver):
        """Check if form moved to Step 2 (promoter details)."""
        try:
            driver.find_element(
                By.XPATH, "//app-dynamic-details//input[@name='Name']", timeout=3
            )
            return True
        except Exception:
            return False

    # ================================================================
    # TEST 01: Form Opens
    # ================================================================

    def test_01_form_opens(self, logged_in_driver):
        driver = logged_in_driver
        page = self._page(driver)
        self._open_form(page)
        name = self._read_field(page, page.COMPANY_NAME_INPUT)
        email = self._read_field(page, page.EMAIL_INPUT)
        shot = self._screenshot(driver, "form_opens")
        loaded = bool(name) or bool(email)
        self._record(
            test_name="Form Opens",
            expected=f"Pre-filled data for '{TEST_COMPANY}'",
            actual=f"name='{name}', email='{email}'",
            status="PASSED" if loaded else "FAILED",
            category="Setup",
            field="",
            screenshot=shot,
        )
        self._cleanup(page)
        assert loaded, "Form did not load with data"

    # ================================================================
    # TEST 02: Step 1 Next-click validations (one form open)
    #   - Required fields (6)
    #   - Format validations (6)
    #   - Non-required fields (1 combined)
    # ================================================================

    def test_02_step1_all_validations(self, logged_in_driver):
        """All Step 1 Next-click validations in a single form open."""
        driver = logged_in_driver
        page = self._page(driver)
        self._open_form(page)

        # ---- Read all original values ----
        orig_short_name = self._read_field(page, page.COMPANY_SHORT_NAME_INPUT)
        orig_contact = self._read_field(page, page.CONTACT_NAME_INPUT)
        orig_bg = self._read_field(page, page.COMPANY_BACKGROUND_INPUT)
        orig_email = self._read_field(page, page.EMAIL_INPUT)
        orig_mobile = self._read_field(page, page.MOBILE_NUMBER_INPUT)
        orig_pan = self._read_field(page, page.PAN_INPUT)

        # ============================================================
        # SECTION A: REQUIRED FIELD VALIDATIONS
        # ============================================================

        # A1. Company Short Name (required)
        self._clear_field(driver, "Company Short Name")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Company Short Name")
        shot = self._screenshot(driver, "req_short_name")
        self._record(
            test_name="Required: Company Short Name",
            expected="Error shown for empty field",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Required",
            field="Company Short Name",
            bad_value="(empty)",
            original_value=orig_short_name,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Company Short Name", orig_short_name)

        # A2. Contact Name (required)
        self._clear_field(driver, "Contact Name")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Contact Name")
        shot = self._screenshot(driver, "req_contact_name")
        self._record(
            test_name="Required: Contact Name",
            expected="Error shown for empty field",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Required",
            field="Contact Name",
            bad_value="(empty)",
            original_value=orig_contact,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Contact Name", orig_contact)

        # A3. Company Background (textarea, required)
        self._clear_field(driver, "Company Background", tag="textarea")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Company Background", tag="textarea")
        shot = self._screenshot(driver, "req_company_bg")
        self._record(
            test_name="Required: Company Background",
            expected="Error shown for empty field",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Required",
            field="Company Background",
            bad_value="(empty)",
            original_value=orig_bg,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Company Background", orig_bg, tag="textarea")

        # A4. Email (required, trailing space in name)
        self._clear_field(driver, "Email ")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Email ")
        shot = self._screenshot(driver, "req_email")
        self._record(
            test_name="Required: Email",
            expected="Error shown for empty email",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Required",
            field="Email",
            bad_value="(empty)",
            original_value=orig_email,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Email ", orig_email)

        # A5. Mobile Number (required, 10 digits)
        self._clear_field(driver, "Mobile Number")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Mobile Number")
        shot = self._screenshot(driver, "req_mobile")
        self._record(
            test_name="Required: Mobile Number",
            expected="Error shown for empty mobile",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Required",
            field="Mobile Number",
            bad_value="(empty)",
            original_value=orig_mobile,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Mobile Number", orig_mobile)

        # A6. PAN (required, format AAAAA9999A)
        self._clear_field(driver, "PAN")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "PAN")
        shot = self._screenshot(driver, "req_pan")
        self._record(
            test_name="Required: PAN",
            expected="Error shown / Invalid Pan No",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Required",
            field="PAN",
            bad_value="(empty)",
            original_value=orig_pan,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "PAN", orig_pan)

        # ============================================================
        # SECTION B: FORMAT VALIDATIONS
        # ============================================================

        # B1. Invalid email "abc"
        self._type_field(driver, "Email ", "abc")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Email ")
        shot = self._screenshot(driver, "fmt_email_abc")
        self._record(
            test_name="Format: Email 'abc'",
            expected="Invalid email error",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Format",
            field="Email",
            bad_value="abc",
            original_value=orig_email,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Email ", orig_email)

        # B2. Invalid email "abc@"
        self._type_field(driver, "Email ", "abc@")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Email ")
        shot = self._screenshot(driver, "fmt_email_abc_at")
        self._record(
            test_name="Format: Email 'abc@'",
            expected="Invalid email error",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Format",
            field="Email",
            bad_value="abc@",
            original_value=orig_email,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Email ", orig_email)

        # B3. Invalid mobile "12345" (too short)
        self._type_field(driver, "Mobile Number", "12345")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Mobile Number")
        shot = self._screenshot(driver, "fmt_mobile_short")
        self._record(
            test_name="Format: Mobile '12345'",
            expected="Invalid mobile error",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Format",
            field="Mobile Number",
            bad_value="12345",
            original_value=orig_mobile,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Mobile Number", orig_mobile)

        # B4. Invalid mobile "abcdefghij" (letters)
        self._type_field(driver, "Mobile Number", "abcdefghij")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "Mobile Number")
        shot = self._screenshot(driver, "fmt_mobile_alpha")
        self._record(
            test_name="Format: Mobile 'abcdefghij'",
            expected="Invalid mobile error",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Format",
            field="Mobile Number",
            bad_value="abcdefghij",
            original_value=orig_mobile,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "Mobile Number", orig_mobile)

        # B5. Invalid PAN "12345ABCDE" (wrong format: starts with digits)
        self._type_field(driver, "PAN", "12345ABCDE")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "PAN")
        shot = self._screenshot(driver, "fmt_pan_digits")
        self._record(
            test_name="Format: PAN '12345ABCDE'",
            expected="Invalid Pan No",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Format",
            field="PAN",
            bad_value="12345ABCDE",
            original_value=orig_pan,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "PAN", orig_pan)

        # B6. Invalid PAN "ABCDE1234" (9 chars, too short)
        self._type_field(driver, "PAN", "ABCDE1234")
        page._click_next()
        time.sleep(0.5)
        has_err, err_txt = self._check_field_invalid(driver, "PAN")
        shot = self._screenshot(driver, "fmt_pan_9chars")
        self._record(
            test_name="Format: PAN 'ABCDE1234' (9 chars)",
            expected="Invalid Pan No",
            actual=f"error={has_err}, text='{err_txt}'",
            status="PASSED" if has_err else "FAILED",
            category="Format",
            field="PAN",
            bad_value="ABCDE1234",
            original_value=orig_pan,
            screenshot=shot,
        )
        self._go_back_if_needed(page)
        self._type_field(driver, "PAN", orig_pan)

        # ============================================================
        # SECTION C: NON-REQUIRED FIELDS (LAST -- no need to go back)
        # ============================================================

        # D1. Clear GSTIN only (CIN is required) -> Next should succeed (move to Step 2)`n        self._clear_field(driver, "GSTIN")`n        time.sleep(0.3)
        page._click_next()
        time.sleep(1)

        on_step2 = self._is_on_step2(driver)
        shot = self._screenshot(driver, "non_required_gstin_cin")
        self._record(
            test_name="Non-Required: GSTIN cleared (CIN is required)",
            expected="Next succeeds, moves to Step 2",
            actual=f"moved_to_step2={on_step2}",
            status="PASSED" if on_step2 else "FAILED",
            category="Non-Required",
            field="GSTIN",
            bad_value="(empty)",
            screenshot=shot,
        )

        self._cleanup(page)

    # ================================================================
    # TEST 03: 2FA + Auth Type Dependency
    # ================================================================

    def _find_auth_select(self, driver, timeout=10):
        """Find Auth Type mat-select with wait + scroll into view."""
        auth_select = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//mat-label[contains(.,'Authentication Type')]/ancestor::mat-form-field//mat-select"
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", auth_select)
        time.sleep(0.3)
        return auth_select

    def test_03_2fa_auth_type_dependency(self, logged_in_driver):
        """Test 2FA toggle controls Auth Type dropdown enable/disable."""
        driver = logged_in_driver
        page = self._page(driver)
        self._open_form(page)

        # ---- Step 1: Verify Auth Type is DISABLED when 2FA is OFF ----
        auth_select = self._find_auth_select(driver)
        is_disabled_off = auth_select.get_attribute("aria-disabled") == "true"
        shot = self._screenshot(driver, "2fa_off_auth_disabled")
        self._record(
            test_name="2FA OFF -> Auth Type Disabled",
            expected="Auth Type dropdown is disabled",
            actual=f"aria-disabled={is_disabled_off}",
            status="PASSED" if is_disabled_off else "FAILED",
            category="2FA Dependency",
            field="Authentication Type",
            screenshot=shot,
        )

        # ---- Step 2: Click .slider to enable 2FA ----
        try:
            slider = driver.find_element(
                By.CSS_SELECTOR, "app-slide-toggle-v2:not(.readonly) .slider"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", slider); ActionChains(driver).move_to_element(slider).click().perform()
            time.sleep(1)  # Angular needs time to re-render
        except Exception as e:
            shot = self._screenshot(driver, "2fa_slider_not_found")
            self._record(
                test_name="2FA Toggle: Click .slider",
                expected="Toggle switches to ON",
                actual=f"Error: {e}",
                status="FAILED",
                category="2FA Dependency",
                field="2FA Toggle",
                screenshot=shot,
            )
            self._cleanup(page)
            return  # Can't continue without toggle

        # Verify toggle switched to ON
        on_label = driver.find_element(
            By.CSS_SELECTOR, "app-slide-toggle-v2 .state-label.on"
        )
        is_on = "active" in (on_label.get_attribute("class") or "")
        shot = self._screenshot(driver, "2fa_toggled_on")
        self._record(
            test_name="2FA Toggle ON",
            expected="ON label becomes active",
            actual=f"on_label_active={is_on}",
            status="PASSED" if is_on else "FAILED",
            category="2FA Dependency",
            field="2FA Toggle",
            screenshot=shot,
        )

        # ---- Step 3: Verify Auth Type is now ENABLED ----
        time.sleep(0.5)
        auth_select = self._find_auth_select(driver)
        is_disabled_on = auth_select.get_attribute("aria-disabled") == "true"
        shot = self._screenshot(driver, "2fa_on_auth_enabled")
        self._record(
            test_name="2FA ON -> Auth Type Enabled",
            expected="Auth Type dropdown is enabled",
            actual=f"aria-disabled={is_disabled_on}",
            status="PASSED" if not is_disabled_on else "FAILED",
            category="2FA Dependency",
            field="Authentication Type",
            screenshot=shot,
        )

        # ---- Step 4: Select 'email' from Auth Type dropdown ----
        if not is_disabled_on:
            try:
                auth_select = self._find_auth_select(driver)
                driver.execute_script("arguments[0].click();", auth_select)
                time.sleep(0.5)
                email_opt = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//div[@role='listbox']//mat-option[contains(.,'email')]"
                    ))
                )
                driver.execute_script("arguments[0].click();", email_opt)
                time.sleep(0.3)
                shot = self._screenshot(driver, "2fa_email_selected")
                self._record(
                    test_name="2FA ON -> Select 'email'",
                    expected="Email option selected from Auth Type",
                    actual="Email selected successfully",
                    status="PASSED",
                    category="2FA Dependency",
                    field="Authentication Type",
                    bad_value="email",
                    screenshot=shot,
                )
            except Exception as e:
                shot = self._screenshot(driver, "2fa_email_failed")
                self._record(
                    test_name="2FA ON -> Select 'email'",
                    expected="Email option selected",
                    actual=f"Error: {e}",
                    status="FAILED",
                    category="2FA Dependency",
                    field="Authentication Type",
                    screenshot=shot,
                )

        # ---- Step 5: Toggle 2FA OFF again ----
        try:
            slider = driver.find_element(
                By.CSS_SELECTOR, "app-slide-toggle-v2:not(.readonly) .slider"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", slider); ActionChains(driver).move_to_element(slider).click().perform()
            time.sleep(1)
        except Exception:
            pass

        auth_select = self._find_auth_select(driver)
        is_disabled_again = auth_select.get_attribute("aria-disabled") == "true"
        shot = self._screenshot(driver, "2fa_off_again")
        self._record(
            test_name="2FA OFF -> Auth Type Disabled Again",
            expected="Auth Type dropdown is disabled after toggle off",
            actual=f"aria-disabled={is_disabled_again}",
            status="PASSED" if is_disabled_again else "FAILED",
            category="2FA Dependency",
            field="Authentication Type",
            screenshot=shot,
        )

        self._cleanup(page)

    # ================================================================
    # TEST 04: Duplicate Company Name -> SweetAlert
    # ================================================================

    def test_04_duplicate_name_sweetalert(self, logged_in_driver):
        """Change company name to existing 'Washim' -> expect Validation Failed SweetAlert."""
        driver = logged_in_driver
        page = self._page(driver)
        self._open_form(page)

        # Change company name to "Washim" (already exists)
        self._type_field(driver, "Company Name", "Washim")
        time.sleep(0.3)

        # Click Update directly from Step 1
        self._click_update_direct(driver)

        # Check SweetAlert
        title, has_download = self._check_sweetalert(driver)
        shot = self._screenshot(driver, "dup_name_sweetalert")
        is_validation_failed = "validation failed" in title.lower()
        self._record(
            test_name="Duplicate Name: SweetAlert",
            expected="Title='Validation Failed' + Download Errors button",
            actual=f"title='{title}', download_btn={has_download}",
            status="PASSED" if is_validation_failed and has_download else "FAILED",
            category="Backend Validation",
            field="Company Name",
            bad_value="Washim",
            screenshot=shot,
        )

        # Dismiss SweetAlert (Cancel = don't download, form stays open unsaved)
        self._dismiss_sweetalert(driver)
        time.sleep(0.5)

        # Cleanup -- navigate away, changes not saved
        self._cleanup(page)

    # ================================================================
    # TEST 05: Invalid CIN -> SweetAlert
    # ================================================================

    def test_05_invalid_cin_sweetalert(self, logged_in_driver):
        """Enter invalid CIN -> expect Validation Failed SweetAlert on Update."""
        driver = logged_in_driver
        page = self._page(driver)
        self._open_form(page)

        # Change CIN to invalid value
        self._type_field(driver, "CIN", "INVALID123")
        time.sleep(0.3)

        # Click Update directly from Step 1
        self._click_update_direct(driver)

        # Check SweetAlert
        title, has_download = self._check_sweetalert(driver)
        shot = self._screenshot(driver, "invalid_cin_sweetalert")
        is_validation_failed = "validation failed" in title.lower()
        self._record(
            test_name="Invalid CIN: SweetAlert",
            expected="Title='Validation Failed' + Download Errors button",
            actual=f"title='{title}', download_btn={has_download}",
            status="PASSED" if is_validation_failed and has_download else "FAILED",
            category="Backend Validation",
            field="CIN",
            bad_value="INVALID123",
            screenshot=shot,
        )

        # Dismiss SweetAlert
        self._dismiss_sweetalert(driver)
        time.sleep(0.5)

        # Cleanup -- navigate away, changes not saved
        self._cleanup(page)

    # ================================================================
    # TEST 06: Max Length -> SweetAlert (backend validation on Update)
    # ================================================================

    def test_06_max_length_sweetalert(self, logged_in_driver):
        """Enter values exceeding max length -> expect 'Failed to save record' toast on Update."""
        driver = logged_in_driver
        page = self._page(driver)
        self._open_form(page)

        # ---- Company Short Name: max 255, enter 300 ----
        self._type_field(driver, "Company Short Name", "A" * 300)
        time.sleep(0.3)

        self._click_update_direct(driver)

        # Toast: "Failed to save record" (auto-dismisses, no buttons)
        title, has_download = self._check_sweetalert(driver)
        shot = self._screenshot(driver, "maxlen_short_name")
        is_failed = "failed to save record" in title.lower()
        self._record(
            test_name="Max Length: Company Short Name (300 chars)",
            expected="Toast='Failed to save record'",
            actual=f"title='{title}'",
            status="PASSED" if is_failed else "FAILED",
            category="Backend Validation",
            field="Company Short Name",
            bad_value="A" * 300,
            screenshot=shot,
        )

        # Toast auto-dismisses, no need to click Cancel
        time.sleep(2)
        self._cleanup(page)
