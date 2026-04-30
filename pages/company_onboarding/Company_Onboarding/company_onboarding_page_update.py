"""
company_onboarding_page_update.py
---------------------------------
Page Object for UPDATE operations on Company Onboarding.
Inherits from CompanyOnboardingPage (reuses all locators + helpers).
Adds: edit, read, update, verify methods for the 5-step stepper.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.logger import log
from pages.company_onboarding.Company_Onboarding.company_onboarding_page import CompanyOnboardingPage


class CompanyOnboardingUpdatePage(CompanyOnboardingPage):
    """Update-focused page object. Inherits locators + base methods from parent."""

    # ---- SweetAlert ----
    SWEETALERT_TITLE = ("css", "#swal2-title")
    SWEETALERT_CONFIRM = ("css", ".swal2-confirm")

    # ---- Buttons ----
    UPDATE_BUTTON = ("xpath", "//div[@class='popup-footer']//button[contains(.,'Update')]")

    # ================================================================
    # HELPERS
    # ================================================================
    def _find_company_row(self, company_name):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "mat-row")
        for row in rows:
            try:
                cell = row.find_element(By.CSS_SELECTOR, "td.cdk-column-name")
                if cell and company_name.strip().lower() in cell.text.strip().lower():
                    return row
            except Exception:
                continue
        return None

    def _get_input_value(self, locator):
        el = self.driver.find_element(*locator)
        return el.get_attribute("value") or ""

    # ================================================================
    # TABLE OPERATIONS
    # ================================================================
    def click_edit_for_company(self, company_name):
        log.info(f"Looking for Edit button for: {company_name}")
        row = self._find_company_row(company_name)
        if not row:
            raise Exception(f"Company '{company_name}' not found in table")
        try:
            edit_btn = row.find_element(By.CSS_SELECTOR,
                "button[mattooltip='EDIT'], button[mattooltip='Edit']")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
                edit_btn)
            log.info(f"Clicked Edit for: {company_name}")
            self.wait_seconds(1.5)
        except Exception as e:
            raise Exception(f"Could not click Edit for '{company_name}': {e}")

    def read_table_row_values(self, company_name):
        row = self._find_company_row(company_name)
        if not row:
            raise Exception(f"Company '{company_name}' not found in table")
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        values = {}
        for cell in cells:
            try:
                col = cell.get_attribute("class")
                if col:
                    for cls in col.split():
                        if cls.startswith("cdk-column-"):
                            values[cls] = cell.text.strip()
            except Exception:
                continue
        return values

    def click_update_button(self):
        log.info("Clicking Update button...")
        self._force_close_panels()
        self.scroll_to_element(self.UPDATE_BUTTON)
        self.wait_seconds(0.3)
        self.click(self.UPDATE_BUTTON)
        self.wait_seconds(2)

    # ================================================================
    # SWEETALERT
    # ================================================================
    def wait_for_update_success(self, timeout=30):
        try:
            wait = WebDriverWait(self.driver, timeout)
            title_el = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#swal2-title")))
            msg = title_el.text
            log.info(f"SweetAlert appeared: {msg}")
            try:
                confirm = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm")))
                confirm.click()
                log.info("SweetAlert confirm clicked")
            except Exception:
                log.warning("Could not click confirm, waiting for auto-dismiss")
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.invisibility_of_element_located(
                            (By.CSS_SELECTOR, "#swal2-title")))
                except Exception:
                    pass
            return msg
        except Exception:
            log.warning("No SweetAlert detected after Update")
            return ""

    def wait_for_dialog_closed(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "mat-dialog-container")))
            log.info("Dialog closed")
            return True
        except Exception:
            log.warning("Dialog may still be open")
            return False

    # ================================================================
    # STEP 1 — Company Details
    # ================================================================
    def read_step1_values(self):
        values = {}
        for key, loc in [
            ("company_name", self.COMPANY_NAME_INPUT),
            ("company_short_name", self.COMPANY_SHORT_NAME_INPUT),
            ("contact_name", self.CONTACT_NAME_INPUT),
            ("email", self.EMAIL_INPUT),
            ("mobile_number", self.MOBILE_NUMBER_INPUT),
            ("pan", self.PAN_INPUT),
            ("gstin", self.GSTIN_INPUT),
            ("cin", self.CIN_INPUT),
        ]:
            try:
                values[key] = self._get_input_value(loc)
            except Exception:
                pass
        log.info(f"Step 1 read: {list(values.keys())}")
        return values

    def apply_step1_updates(self, updates):
        log.info(f"Applying Step 1 updates: {list(updates.keys())}")
        field_map = {
            "contact_name": self.CONTACT_NAME_INPUT,
            "email": self.EMAIL_INPUT,
            "mobile_number": self.MOBILE_NUMBER_INPUT,
            "company_short_name": self.COMPANY_SHORT_NAME_INPUT,
            "company_background": self.COMPANY_BACKGROUND_INPUT,
            "pan": self.PAN_INPUT,
            "gstin": self.GSTIN_INPUT,
            "cin": self.CIN_INPUT,
        }
        for key, locator in field_map.items():
            if key in updates and updates[key]:
                self.type_text(locator, str(updates[key]), clear_first=True)

    # ================================================================
    # STEP 2 — Promoters
    # ================================================================
    def read_step2_values(self, row_index=1):
        values = {}
        try:
            loc = ("xpath", f"(//app-dynamic-details//input[@name='Name'])[{row_index}]")
            values["promoter_name"] = self._get_input_value(loc)
        except Exception:
            pass
        try:
            loc = ("xpath", f"(//app-dynamic-details//textarea[@name='Remark'])[{row_index}]")
            values["promoter_remark"] = self._get_input_value(loc)
        except Exception:
            pass
        log.info(f"Step 2 read: {list(values.keys())}")
        return values

    def apply_step2_updates(self, updates, row_index=1):
        log.info(f"Applying Step 2 updates: {list(updates.keys())}")
        if updates.get("promoter_name"):
            loc = ("xpath", f"(//app-dynamic-details//input[@name='Name'])[{row_index}]")
            self.type_text(loc, updates["promoter_name"], clear_first=True)
        if updates.get("promoter_remark"):
            loc = ("xpath", f"(//app-dynamic-details//textarea[@name='Remark'])[{row_index}]")
            self.type_text(loc, updates["promoter_remark"], clear_first=True)

    # ================================================================
    # STEP 3 — Address
    # ================================================================
    def read_step3_values(self, row_index=1):
        values = {}
        try:
            values["address"] = self._get_input_value(
                self._idx(self.ADDRESS_INPUT, row_index))
        except Exception:
            pass
        try:
            values["pin_code"] = self._get_input_value(
                self._idx(self.PIN_CODE_INPUT, row_index))
        except Exception:
            pass
        log.info(f"Step 3 read: {list(values.keys())}")
        return values

    def apply_step3_updates(self, updates, row_index=1):
        log.info(f"Applying Step 3 updates: {list(updates.keys())}")
        if updates.get("address"):
            self.type_text(self._idx(self.ADDRESS_INPUT, row_index),
                          updates["address"], clear_first=True)
        if updates.get("pin_code"):
            self.type_text(self._idx(self.PIN_CODE_INPUT, row_index),
                          updates["pin_code"], clear_first=True)

    # ================================================================
    # STEP 4 — Business Details
    # ================================================================
    def read_step4_values(self, row_index=1):
        values = {}
        try:
            values["business_model"] = self._get_input_value(
                self._idx(self.BUSINESS_MODEL_INPUT, row_index))
        except Exception:
            pass
        try:
            values["market_linkages"] = self._get_input_value(
                self._idx(self.MARKET_LINKAGES_INPUT, row_index))
        except Exception:
            pass
        log.info(f"Step 4 read: {list(values.keys())}")
        return values

    def apply_step4_updates(self, updates, row_index=1):
        log.info(f"Applying Step 4 updates: {list(updates.keys())}")
        if updates.get("business_model"):
            self.type_text(self._idx(self.BUSINESS_MODEL_INPUT, row_index),
                          updates["business_model"], clear_first=True)
        if updates.get("market_linkages"):
            self.type_text(self._idx(self.MARKET_LINKAGES_INPUT, row_index),
                          updates["market_linkages"], clear_first=True)

    # ================================================================
    # STEP 5 — Infrastructure
    # ================================================================
    def read_step5_values(self, row_index=1):
        values = {}
        try:
            values["infra_location"] = self._get_input_value(
                self._idx(self.INFRA_LOCATION_INPUT, row_index))
        except Exception:
            pass
        log.info(f"Step 5 read: {list(values.keys())}")
        return values

    def apply_step5_updates(self, updates, row_index=1):
        log.info(f"Applying Step 5 updates: {list(updates.keys())}")
        if updates.get("infra_location"):
            self.type_text(self._idx(self.INFRA_LOCATION_INPUT, row_index),
                          updates["infra_location"], clear_first=True)

    # ================================================================
    # ONE-CALL: update_company()
    # ================================================================
    def update_company(self, company_name, all_updates):
        log.info(f"Starting one-call update for: {company_name}")
        before_values = {}
        after_values = {}
        try:
            self.click_edit_for_company(company_name)
            self.wait_seconds(1)
            before_values = self.read_all_step_values()
            log.info(f"BEFORE: {list(before_values.keys())}")

            if 1 in all_updates:
                self.apply_step1_updates(all_updates[1])
            self._click_next(); self.wait_seconds(1)
            if 2 in all_updates:
                self.apply_step2_updates(all_updates[2], row_index=1)
            self._click_next(); self.wait_seconds(1)
            if 3 in all_updates:
                self.apply_step3_updates(all_updates[3], row_index=1)
            self._click_next(); self.wait_seconds(1)
            if 4 in all_updates:
                self.apply_step4_updates(all_updates[4], row_index=1)
            self._click_next(); self.wait_seconds(1)
            if 5 in all_updates:
                self.apply_step5_updates(all_updates[5], row_index=1)

            self.click_update_button()
            self.wait_for_update_success(timeout=30)
            self.wait_for_dialog_closed(timeout=15)

            self.click_refresh(); self.wait_seconds(2)
            self.click_edit_for_company(company_name)
            self.wait_seconds(1)
            after_values = self.read_all_step_values()
            log.info(f"AFTER: {list(after_values.keys())}")

            self.click_cancel_or_dismiss_dialog()
            self.wait_seconds(1)

            return {"success": True, "before_values": before_values,
                    "after_values": after_values, "error": ""}
        except Exception as e:
            log.error(f"Update failed: {e}")
            return {"success": False, "before_values": before_values,
                    "after_values": after_values, "error": str(e)}

    # ================================================================
    # READ ALL STEPS
    # ================================================================
    def read_all_step_values(self):
        all_vals = {}
        all_vals[1] = self.read_step1_values()
        self._click_next(); self.wait_seconds(1)
        all_vals[2] = self.read_step2_values(row_index=1)
        self._click_next(); self.wait_seconds(1)
        all_vals[3] = self.read_step3_values(row_index=1)
        self._click_next(); self.wait_seconds(1)
        all_vals[4] = self.read_step4_values(row_index=1)
        self._click_next(); self.wait_seconds(1)
        all_vals[5] = self.read_step5_values(row_index=1)
        return all_vals

    # ================================================================
    # VERIFY
    # ================================================================
    def verify_updated_fields(self, after_values, expected_updates):
        mismatches = []
        for step_num, updates in expected_updates.items():
            if step_num not in after_values:
                mismatches.append(f"Step {step_num}: no after_values")
                continue
            for field, expected in updates.items():
                actual = after_values[step_num].get(field, "")
                if actual != expected:
                    mismatches.append(
                        f"Step {step_num}/{field}: expected '{expected}', got '{actual}'")
        if mismatches:
            log.warning(f"Mismatches: {mismatches}")
        else:
            log.info("All fields match!")
        return mismatches