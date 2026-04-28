"""
company_onboarding_page.py
---------------------
Page Object Model for RhythmERP Company Onboarding screen.

KEY DESIGN DECISION:
  Never send Keys.ESCAPE anywhere except click_cancel_or_dismiss_dialog.
  Use backdrop click + JS removal for overlay panels.
"""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from common.base_page import BasePage
from common.logger import log
from config import RHYTHMERP_BASE_URL


class CompanyOnboardingPage(BasePage):
    PAGE_URL = f"{RHYTHMERP_BASE_URL}/#/dynamic-screens/Company%20Onboarding"

    # ---- Toolbar ----
    ADD_BUTTON = ("css", "button[mattooltip='ADD'], div[mattooltip='ADD'] button")
    REFRESH_BUTTON = ("css", "button[mattooltip='REFRESH'], div[mattooltip='REFRESH'] button")

    # ---- Header fields (outside stepper) ----
    COMPANY_NAME_INPUT = ("css", "input[name='Company Name']")
    ENTITY_GROUP_SELECT = ("xpath", "//mat-label[contains(.,'Entity Group')]/ancestor::mat-form-field//mat-select")
    PARENT_NAME_SELECT = ("xpath", "//mat-label[contains(.,'Parent Name')]/ancestor::mat-form-field//mat-select")
    COMPANY_LINKED_SELECT = ("xpath", "//mat-label[contains(.,'Company Linked')]/ancestor::mat-form-field//mat-select")

    # ---- Step 1 fields ----
    COMPANY_SHORT_NAME_INPUT = ("css", "input[name='Company Short Name']")
    CONTACT_NAME_INPUT = ("css", "input[name='Contact Name']")
    COMPANY_BACKGROUND_INPUT = ("css", "textarea[name='Company Background']")
    EMAIL_INPUT = ("css", "input[name='Email ']")
    MOBILE_NUMBER_INPUT = ("css", "input[name='Mobile Number']")
    PAN_INPUT = ("css", "input[name='PAN']")
    GSTIN_INPUT = ("css", "input[name='GSTIN']")
    CIN_INPUT = ("css", "input[name='CIN']")
    PASSWORD_INPUT = ("css", "input[name='Password']")

    PLAN_TYPE_SELECT = ("xpath", "//mat-label[contains(.,'Plan Type')]/ancestor::mat-form-field//mat-select")
    AUTH_TYPE_SELECT = ("xpath", "//mat-label[contains(.,'Authentication Type')]/ancestor::mat-form-field//mat-select")
    TWO_FA_TOGGLE = ("css", "app-slide-toggle-v2:not(.readonly) .slider")

    # ---- Next / Back ----
    NEXT_BUTTON_XPATH = (
        "//mat-dialog-container//button[@matsteppernext or @matStepperNext]"
        " | //mat-stepper//button[@matsteppernext or @matStepperNext]"
        " | //mat-dialog-container//button[normalize-space(.)='Next']"
    )
    STEP1_NEXT_BUTTON = ("xpath", NEXT_BUTTON_XPATH)
    STEP2_BACK_BUTTON = ("css", "form.step-form button[matstepperprevious]")

    # ---- Step 3: Address details ----
    ADDRESS_TYPE_SELECT = ("xpath", "//app-dynamic-details//mat-label[contains(.,'Address Type')]/ancestor::mat-form-field//mat-select")
    COUNTRY_SELECT = ("xpath", "//app-dynamic-details//mat-label[contains(.,'Country')]/ancestor::mat-form-field//mat-select")
    STATE_SELECT = ("xpath", "//app-dynamic-details//mat-label[contains(.,'State')]/ancestor::mat-form-field//mat-select")
    DISTRICT_SELECT = ("xpath", "//app-dynamic-details//mat-label[contains(.,'District')]/ancestor::mat-form-field//mat-select")
    TALUKA_SELECT = ("xpath", "//app-dynamic-details//mat-label[contains(.,'Taluka')]/ancestor::mat-form-field//mat-select")
    ADDRESS_INPUT = ("xpath", "//app-dynamic-details//input[@name='Address']")
    PIN_CODE_INPUT = ("xpath", "//app-dynamic-details//input[@name='Pin Code']")

    # ---- Step 2: Promoters ----
    PROMOTER_NAME_INPUT = ("xpath", "//app-dynamic-details//input[@name='Name']")
    STEP_REMARK_INPUT = ("xpath", "//app-dynamic-details//textarea[@name='Remark']")
    ADD_ROW_BUTTON = ("css", "button[mat-icon-button][color='primary']")

    # ---- Step 3: Business Details ----
    BUSINESS_MODEL_INPUT = ("xpath", "//app-dynamic-details//mat-label[normalize-space(.)='Business Model']/ancestor::mat-form-field//input")
    MARKET_LINKAGES_INPUT = ("xpath", "//app-dynamic-details//mat-label[normalize-space(.)='Market Linkages']/ancestor::mat-form-field//input")
    LINE_OF_BUSINESS_INPUT = ("xpath", "//app-dynamic-details//mat-label[normalize-space(.)='Line of Business']/ancestor::mat-form-field//input")
    ADDITIONAL_BUSINESS_INPUT = ("xpath", "//app-dynamic-details//mat-label[contains(.,'Additional Business Activities')]/ancestor::mat-form-field//input")

    # ---- Step 4: Infrastructure ----
    INFRA_TYPE_SELECT = ("xpath", "//app-dynamic-details//mat-label[normalize-space(.)='Infrastructure Type']/ancestor::mat-form-field//mat-select")
    INFRA_LOCATION_INPUT = ("xpath", "//app-dynamic-details//input[@name='Infrastructure Location']")
    INFRA_OWNERSHIP_SELECT = ("xpath", "//app-dynamic-details//mat-label[normalize-space(.)='Ownership Type']/ancestor::mat-form-field//mat-select")

    # ---- Dialog footer ----
    CANCEL_BUTTON = ("xpath", "//div[@class='popup-footer']//button[contains(.,'Cancel')]")
    SUBMIT_BUTTON = ("xpath", "//div[@class='popup-footer']//button[contains(.,'Submit')]")

    # ================================================================
    # Navigation & toolbar
    # ================================================================
    def navigate_to_page(self):
        log.info("Navigating to Company Onboarding page...")
        self.navigate_to(self.PAGE_URL)
        self.wait_seconds(2)

    def is_page_loaded(self):
        return self.is_displayed(self.ADD_BUTTON, timeout=10)

    def open_add_form(self):
        log.info("Clicking ADD button...")
        self.click(self.ADD_BUTTON)
        self.wait_seconds(1.5)

    def click_refresh(self):
        self.click(self.REFRESH_BUTTON)
        self.wait_seconds(2)

    # ================================================================
    # Overlay cleanup
    # ================================================================
    def _force_close_panels(self):
        """Remove ALL select overlay panes from the DOM via JS. Keeps dialog backdrop."""
        self.driver.execute_script("""
            document.querySelectorAll(
                'div.cdk-overlay-backdrop:not(.cdk-overlay-dark-backdrop)'
            ).forEach(function(el) { el.remove(); });
            document.querySelectorAll(
                'div.cdk-overlay-pane'
            ).forEach(function(el) {
                if (!el.querySelector('mat-dialog-container')) el.remove();
            });
        """)
        self.wait_seconds(0.2)

    def _close_select_panel(self):
        """Try backdrop click first; fall back to JS removal."""
        try:
            backdrops = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.cdk-overlay-backdrop:not(.cdk-overlay-dark-backdrop)",
            )
            for bd in backdrops:
                try:
                    if bd.is_displayed():
                        bd.click()
                        self.wait_seconds(0.3)
                        return
                except Exception:
                    pass
        except Exception:
            pass

        # Quick check if anything remains
        remaining = self.driver.find_elements(
            By.CSS_SELECTOR,
            "div.cdk-overlay-backdrop:not(.cdk-overlay-dark-backdrop), "
            "div.cdk-overlay-pane mat-option",
        )
        if remaining:
            self._force_close_panels()

    # ================================================================
    # Row management
    # ================================================================
    def add_row(self):
        """Click the + button to add a new row in the current step."""
        btns = self.driver.find_elements("css selector", "button[mat-icon-button][color='primary']")
        clicked = False
        for btn in btns:
            try:
                if btn.is_displayed() and btn.is_enabled():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
                        btn
                    )
                    clicked = True
                    break
            except Exception:
                continue
        if not clicked:
            raise Exception("+ (add) button not found or not clickable")
        self.wait_seconds(0.5)
        log.info("Added new row via + button")

    # ================================================================
    # Fill Step 1 (Company Details)
    # ================================================================

    def _idx(self, locator, index):
        """Wrap locator with 1-based XPath index."""
        strategy, path = locator
        return (strategy, f"({path})[{index}]")
    def fill_company_details(self, data):
        log.info("Filling Company Details...")

        field_map = {
            "company_name": self.COMPANY_NAME_INPUT,
            "company_short_name": self.COMPANY_SHORT_NAME_INPUT,
            "contact_name": self.CONTACT_NAME_INPUT,
            "company_background": self.COMPANY_BACKGROUND_INPUT,
            "email": self.EMAIL_INPUT,
            "mobile_number": self.MOBILE_NUMBER_INPUT,
            "pan": self.PAN_INPUT,
            "gstin": self.GSTIN_INPUT,
            "cin": self.CIN_INPUT,
        }
        for key, locator in field_map.items():
            if data.get(key):
                self.type_text(locator, str(data[key]), clear_first=True)

        select_map = {
            "entity_group": self.ENTITY_GROUP_SELECT,
            "parent_name": self.PARENT_NAME_SELECT,
            "plan_type": self.PLAN_TYPE_SELECT,
        }
        for key, locator in select_map.items():
            if data.get(key):
                self._select_mat_option(locator, str(data[key]))

        if data.get("company_linked"):
            values = (
                data["company_linked"]
                if isinstance(data["company_linked"], list)
                else [data["company_linked"]]
            )
            self._select_mat_options_multi(self.COMPANY_LINKED_SELECT, values)

        if data.get("is_2fa"):
            self._enable_2fa_toggle()

        if data.get("is_2fa") and data.get("auth_type"):
            self.wait_seconds(0.3)
            self._select_mat_option(self.AUTH_TYPE_SELECT, str(data["auth_type"]))

        # Clean up any open panels
        self._force_close_panels()

        log.info("Company Details filled")

        errors = self.driver.find_elements(
            By.CSS_SELECTOR, "mat-error, .mat-mdc-form-field-error"
        )
        if errors:
            texts = [e.text for e in errors if e.text.strip()]
            if texts:
                log.warning(f"Validation errors after fill: {texts}")

    # ================================================================
    # Step navigation â€” OPTIMIZED: JS click directly, no fallback chain
    # ================================================================
    def _click_next(self):
        """
        Find Next button and click it via JS directly.
        No normal click attempt (always gets intercepted by overlay).
        No 10s wait on primary locator (always times out).
        """
        self._force_close_panels()

        btn_element = None
        # Short 5s timeout instead of 10s
        try:
            btn_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, self.NEXT_BUTTON_XPATH))
            )
        except Exception:
            pass

        # Quick DOM fallback scan
        if btn_element is None:
            candidates = self.driver.find_elements(
                By.XPATH,
                "//button[@matsteppernext or @matStepperNext]"
                " | //button[normalize-space(.)='Next']",
            )
            for c in candidates:
                try:
                    if c.is_displayed() and c.is_enabled():
                        btn_element = c
                        break
                except Exception:
                    continue

        if btn_element is None:
            raise Exception("Next button not found")

        # JS click directly â€” skip normal click entirely
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            btn_element,
        )
        log.info("Clicked Next button")

    def go_to_step2(self):
        """Step 1 -> Step 2 (Promoters)."""
        if not self.is_add_form_open():
            raise Exception("Dialog closed before clicking Next")
        log.info("  Next: Step 1 -> Step 2 (Promoters)")
        self._click_next()
        self.wait_seconds(0.8)

    def go_to_step3(self):
        """Step 2 (Promoters) -> Step 3 (Business Details)."""
        log.info("  Next: Step 2 -> Step 3 (Business Details)")
        self._click_next()
        self.wait_seconds(0.8)

    def go_to_step4(self):
        """Step 3 (Business) -> Step 4 (Infrastructure)."""
        log.info("  Next: Step 3 -> Step 4 (Infrastructure)")
        self._click_next()
        self.wait_seconds(0.8)

    def go_to_address_step(self, company_data):
        """Navigate: Promoters -> Address -> Business -> Infrastructure."""
        self.click_next_button("2", "3", "Address")
        self.fill_address_details(company_data)
        self.click_next_button("3", "4", "Business Activities")
        self.fill_business_details(company_data)
        self.click_next_button("4", "5", "Infrastructure Details")
        self.fill_infrastructure(company_data)
        self.click_next_button("5", "6", "Submit")

    def go_back_to_step1(self):
        self.click(self.STEP2_BACK_BUTTON)
        self.wait_seconds(1)

    # ================================================================
    # Fill Address Details
    # ================================================================

    def _select_random_from_dropdown(self, select_locator, label_name):
        """
        Open a mat-select dropdown, read ALL options from the UI,
        pick one randomly, click it, and return the selected text.
        Bulletproof against case mismatches and missing options.
        """
        # Open dropdown
        try:
            self.click(select_locator)
        except Exception:
            trigger = (
                "xpath",
                f"{select_locator[1]}//div[contains(@class,'mat-mdc-select-trigger')]",
            )
            self.click(trigger)
        self.wait_seconds(0.5)

        # Wait for options to appear
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listbox'] mat-option"))
        )

        # Read all available options from UI
        options = self.driver.find_elements(By.CSS_SELECTOR, "div[role='listbox'] mat-option")
        option_texts = [t for t in [opt.text.strip() for opt in options] if t and not t.startswith("Select")]

        # Fallback for newer Angular Material
        if not option_texts:
            options = self.driver.find_elements(By.CSS_SELECTOR, "div[role='listbox'] [role='option']")
            option_texts = [opt.text.strip() for opt in options if opt.text.strip()]

        if not option_texts:
            raise Exception(f"No options found in '{label_name}' dropdown")

        # Pick random
        selected = random.choice(option_texts)

        # Click using JS (avoids interception issues)
        for opt in options:
            if opt.text.strip() == selected:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
                    opt
                )
                break

        self.wait_seconds(0.3)
        log.info(f"Random '{label_name}' selected: '{selected}'")
        return selected

    def fill_address_details(self, data, row_index=1):
        self._force_close_panels()
        log.info(f"Filling Address Details row {row_index}...")
        if data.get("address_type"):
            self._select_mat_option(self._idx(self.ADDRESS_TYPE_SELECT, row_index), data["address_type"])
        if data.get("country"):
            self._select_mat_option(self._idx(self.COUNTRY_SELECT, row_index), data["country"])
            self.wait_seconds(0.5)
        selected_state = self._select_random_from_dropdown(self._idx(self.STATE_SELECT, row_index), "State")
        self.wait_seconds(0.5)
        selected_district = self._select_random_from_dropdown(self._idx(self.DISTRICT_SELECT, row_index), "District")
        self.wait_seconds(0.5)
        selected_taluka = self._select_random_from_dropdown(self._idx(self.TALUKA_SELECT, row_index), "Taluka")
        uid = data.get("address", "").split(",")[0].strip() or str(row_index)
        address_text = f"{uid}, Test Street, {selected_taluka}"
        self.type_text(self._idx(self.ADDRESS_INPUT, row_index), address_text, clear_first=True)
        pin = "".join(random.choices("0123456789", k=6))
        self.type_text(self._idx(self.PIN_CODE_INPUT, row_index), pin, clear_first=True)
        log.info(f"Address Details row {row_index} filled")

    def fill_promoters(self, promoter, row_index=1):
        log.info(f"Filling Promoters row {row_index}...")
        self._force_close_panels()
        name_loc = ("xpath", f"(//app-dynamic-details//input[@name=\'Name\'])[{row_index}]")
        remark_loc = ("xpath", f"(//app-dynamic-details//textarea[@name=\'Remark\'])[{row_index}]")
        self.type_text(name_loc, promoter.get("name", "Mr Test Promoter"), clear_first=True)
        self.type_text(remark_loc, promoter.get("remark", "Test remark."), clear_first=True)
        self.wait_seconds(0.3)
        log.info(f"Promoters row {row_index} filled")

    # ================================================================
    # Fill Step 3: Business Details
    # ================================================================
    def fill_business_details(self, data, row_index=1):
        log.info(f"Filling Business Details row {row_index}...")
        self._force_close_panels()
        self.type_text(self._idx(self.BUSINESS_MODEL_INPUT, row_index), data.get("business_model", ""), clear_first=True)
        self.wait_seconds(0.3)
        self.type_text(self._idx(self.MARKET_LINKAGES_INPUT, row_index), data.get("market_linkages", ""), clear_first=True)
        self.wait_seconds(0.3)
        self.type_text(self._idx(self.LINE_OF_BUSINESS_INPUT, row_index), data.get("line_of_business", ""), clear_first=True)
        self.wait_seconds(0.3)
        self.type_text(self._idx(self.ADDITIONAL_BUSINESS_INPUT, row_index), data.get("additional_business_activities", ""), clear_first=True)
        self.wait_seconds(0.5)
        log.info(f"Business Details row {row_index} filled")

    def fill_infrastructure(self, data, row_index=1):
        log.info(f"Filling Infrastructure row {row_index}...")
        self._force_close_panels()
        self._select_random_from_dropdown(self._idx(self.INFRA_TYPE_SELECT, row_index), "Infrastructure Type")
        self.wait_seconds(0.5)
        self.type_text(self._idx(self.INFRA_LOCATION_INPUT, row_index), data.get("infra_location", "Test Location"), clear_first=True)
        self.wait_seconds(0.3)
        self._select_random_from_dropdown(self._idx(self.INFRA_OWNERSHIP_SELECT, row_index), "Ownership Type")
        self.wait_seconds(0.5)
        log.info(f"Infrastructure row {row_index} filled")

    def submit(self):
        log.info("Submitting form...")
        self._force_close_panels()
        self.scroll_to_element(self.SUBMIT_BUTTON)
        self.wait_seconds(0.3)
        self.click(self.SUBMIT_BUTTON)
        self.wait_seconds(2)

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        self.wait_seconds(1)

    # ================================================================
    # One-call creation
    # ================================================================
    def create_company(self, company_data):
        log.info(f"Creating company: {company_data.get('company_name', 'N/A')}")
        self.open_add_form()
        self.fill_company_details(company_data)
        # Step 2: Promoters (random 1-4 rows)
        self.go_to_step2()
        promoters = company_data.get("promoters", [])
        for idx, promoter in enumerate(promoters, 1):
            if idx > 1:
                self.add_row()
            self.fill_promoters(promoter, row_index=idx)
        # Step 3: Address (fixed 2 rows)
        self.go_to_step3()
        num_addr = company_data.get("num_addresses", 1)
        for idx in range(1, num_addr + 1):
            if idx > 1:
                self.add_row()
            self.fill_address_details(company_data, row_index=idx)
        # Step 4: Business Activities (random 1-4 rows)
        self.go_to_step4()
        num_biz = company_data.get("num_business_rows", 1)
        for idx in range(1, num_biz + 1):
            if idx > 1:
                self.add_row()
            self.fill_business_details(company_data, row_index=idx)
        # Step 5: Infrastructure (random 1-4 rows)
        self._click_next()
        num_infra = company_data.get("num_infra_rows", 1)
        for idx in range(1, num_infra + 1):
            if idx > 1:
                self.add_row()
            self.fill_infrastructure(company_data, row_index=idx)
        self.submit()
        msg = self.get_success_message(timeout=30)
        if msg:
            log.info(f"Server message: {msg}")
        else:
            log.warning("No success message detected")
        self.wait_seconds(2)

    def create_bulk_companies(self, companies_list, on_progress=None):
        total = len(companies_list)
        results = []
        for i, comp in enumerate(companies_list, 1):
            name = comp.get("company_name", f"Company_{i}")
            log.info(f"[{i}/{total}] Creating: {name}")
            result = {"index": i, "company_name": name, "status": "passed", "error": ""}
            try:
                self.create_company(comp)
            except Exception as e:
                result["status"] = "failed"
                result["error"] = str(e)
                log.failed(f"Failed: {name} - {e}")
                try:
                    self.click_cancel_or_dismiss_dialog()
                    self.click_refresh()
                except Exception:
                    self.navigate_to_page()
            results.append(result)
            if on_progress:
                on_progress(i, total, name)
        passed = sum(1 for r in results if r["status"] == "passed")
        log.info(f"Bulk creation: {passed}/{total} passed")
        return results

    # ================================================================
    # Verification helpers
    # ================================================================
    def is_add_form_open(self):
        return self.is_displayed(self.COMPANY_NAME_INPUT, timeout=5)

    def is_step2_visible(self):
        """Check if Address Details step is visible."""
        return self.is_displayed(self.ADDRESS_INPUT, timeout=5)

    def is_dialog_closed(self):
        return not self.is_displayed(self.COMPANY_NAME_INPUT, timeout=15)

    def get_success_message(self, timeout=10):
        toast = ("css", "snack-bar-container .mat-mdc-snack-bar-label, [role='alert']")
        if self.is_displayed(toast, timeout=timeout):
            return self.get_text(toast)
        return ""

    # ================================================================
    # Internal mat-select helpers
    # ================================================================
    def _select_mat_option(self, select_locator, option_text):
        try:
            self.click(select_locator)
        except Exception:
            trigger = (
                "xpath",
                f"{select_locator[1]}//div[contains(@class,'mat-mdc-select-trigger')]",
            )
            self.click(trigger)
        self.wait_seconds(0.3)
        opt_loc = (
            "xpath",
            f"//div[@role='listbox']//mat-option[contains(.,'{option_text}')]"
            f" | //div[@role='listbox']//div[@role='option'][contains(.,'{option_text}')]",
        )
        self.wait_for_visible(opt_loc, timeout=5)
        self.click(opt_loc)
        self.wait_seconds(0.3)
        log.info(f"Selected '{option_text}'")

    def _select_mat_options_multi(self, select_locator, option_texts):
        try:
            self.click(select_locator)
        except Exception:
            trigger = (
                "xpath",
                f"{select_locator[1]}//div[contains(@class,'mat-mdc-select-trigger')]",
            )
            self.click(trigger)
        self.wait_seconds(0.3)

        for opt in option_texts:
            opt_loc = (
                "xpath",
                f"//div[@role='listbox']//mat-option[contains(.,'{opt}')]"
                f" | //div[@role='listbox']//div[@role='option'][contains(.,'{opt}')]",
            )
            self.wait_for_visible(opt_loc, timeout=5)
            self.click(opt_loc)
            self.wait_seconds(0.2)
            log.info(f"Multi-select: '{opt}'")

        self._close_select_panel()

    def _enable_2fa_toggle(self):
        off = ("css", "app-slide-toggle-v2 .state-label.off.active")
        if self.is_displayed(off, timeout=3):
            log.info("Enabling 2FA toggle")
            self.click(self.TWO_FA_TOGGLE)
            self.wait_seconds(0.3)

    def click_cancel_or_dismiss_dialog(self):
        try:
            if self.is_displayed(self.CANCEL_BUTTON, timeout=2):
                self.click(self.CANCEL_BUTTON)
                return
        except Exception:
            pass
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.wait_seconds(0.5)
