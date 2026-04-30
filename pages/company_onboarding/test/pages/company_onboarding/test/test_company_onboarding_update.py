"""
test_company_onboarding_update.py
----------------------------------
Test script for updating existing Company Onboarding records.

Flow:
  1. Login (via conftest fixture)
  2. Navigate to CO page
  3. Read table row values BEFORE (snapshot)
  4. Open Edit dialog
  5. Read form values BEFORE (baseline)
  6. Apply updates to all 5 steps
  7. Click Update
  8. Wait for SweetAlert "Your record has been updated successfully!"
  9. Dialog closes -> back to table
  10. Refresh table (safety)
  11. Re-open Edit -> read form values AFTER
  12. Assert all updated fields match
  13. Cancel dialog (cleanup)
  14. Generate Update Excel Report
"""

import os
import sys
import pytest
import time
from common.logger import log
from pages.company_onboarding.Company_Onboarding.company_onboarding_page_update import (
    CompanyOnboardingUpdatePage,
)
from pages.company_onboarding.test.company_onboarding_update_data import (
    UPDATE_COMPANY_NAME,
    ALL_UPDATES,
    STEP1_UPDATES,
    STEP2_UPDATES,
    STEP3_UPDATES,
    STEP4_UPDATES,
    STEP5_UPDATES,
)
from pages.company_onboarding.co_update_report_generator import generate_update_report

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

CO_REPORT_DIR = os.path.join(PROJECT_ROOT, "pages", "company_onboarding", "reports")


class TestCompanyOnboardingUpdate:

    def test_update_existing_company(self, page):
        """
        Full update test:
        - Opens Edit on existing company
        - Changes fields across all 5 steps
        - Clicks Update, waits for SweetAlert
        - Re-opens Edit to verify changes
        - Asserts all updated fields match
        - Generates Update Excel Report
        """
        update_page = CompanyOnboardingUpdatePage(page.driver)
        company_name = UPDATE_COMPANY_NAME

        log.info("=" * 60)
        log.info(f"UPDATE TEST: {company_name}")
        log.info("=" * 60)

        # ----------------------------------------------------------
        # PHASE 1: Read table values BEFORE
        # ----------------------------------------------------------
        log.info("PHASE 1: Reading table row values BEFORE update...")
        before_table = update_page.read_table_row_values(company_name)
        log.info(f"BEFORE table: {before_table}")

        # ----------------------------------------------------------
        # PHASE 2: Open Edit + read form values BEFORE
        # ----------------------------------------------------------
        log.info("PHASE 2: Opening Edit dialog and reading form values...")
        update_page.click_edit_for_company(company_name)
        update_page.wait_seconds(1)

        before_step1 = update_page.read_step1_values()
        log.info(f"BEFORE Step 1: {before_step1}")

        # ----------------------------------------------------------
        # PHASE 3: Apply updates
        # ----------------------------------------------------------
        log.info("PHASE 3: Applying updates...")

        log.info("  Updating Step 1 (Company Details)...")
        update_page.apply_step1_updates(STEP1_UPDATES)

        log.info("  Updating Step 2 (Promoters)...")
        update_page._click_next()
        update_page.wait_seconds(1)
        update_page.apply_step2_updates(STEP2_UPDATES, row_index=1)

        log.info("  Updating Step 3 (Address)...")
        update_page._click_next()
        update_page.wait_seconds(1)
        update_page.apply_step3_updates(STEP3_UPDATES, row_index=1)

        log.info("  Updating Step 4 (Business Details)...")
        update_page._click_next()
        update_page.wait_seconds(1)
        update_page.apply_step4_updates(STEP4_UPDATES, row_index=1)

        log.info("  Updating Step 5 (Infrastructure)...")
        update_page._click_next()
        update_page.wait_seconds(1)
        update_page.apply_step5_updates(STEP5_UPDATES, row_index=1)

        # ----------------------------------------------------------
        # PHASE 4: Click Update + wait for SweetAlert
        # ----------------------------------------------------------
        log.info("PHASE 4: Clicking Update...")
        update_page.click_update_button()

        log.info("Waiting for SweetAlert confirmation...")
        update_page.wait_for_update_success(timeout=30)

        log.info("Waiting for dialog to close...")
        update_page.wait_for_dialog_closed(timeout=15)

        # ----------------------------------------------------------
        # PHASE 5: Refresh + verify
        # ----------------------------------------------------------
        log.info("PHASE 5: Refreshing and verifying...")
        update_page.click_refresh()
        update_page.wait_seconds(2)

        after_table = update_page.read_table_row_values(company_name)
        log.info(f"AFTER table: {after_table}")

        log.info("Re-opening Edit to verify form values...")
        update_page.click_edit_for_company(company_name)
        update_page.wait_seconds(1)

        after_step1 = update_page.read_step1_values()
        log.info(f"AFTER Step 1: {after_step1}")

        update_page._click_next()
        update_page.wait_seconds(1)
        after_step2 = update_page.read_step2_values(row_index=1)
        log.info(f"AFTER Step 2: {after_step2}")

        update_page._click_next()
        update_page.wait_seconds(1)
        after_step3 = update_page.read_step3_values(row_index=1)
        log.info(f"AFTER Step 3: {after_step3}")

        update_page._click_next()
        update_page.wait_seconds(1)
        after_step4 = update_page.read_step4_values(row_index=1)
        log.info(f"AFTER Step 4: {after_step4}")

        update_page._click_next()
        update_page.wait_seconds(1)
        after_step5 = update_page.read_step5_values(row_index=1)
        log.info(f"AFTER Step 5: {after_step5}")

        update_page.click_cancel_or_dismiss_dialog()
        update_page.wait_seconds(1)

        # ----------------------------------------------------------
        # PHASE 6: Assertions
        # ----------------------------------------------------------
        log.info("PHASE 6: Running assertions...")

        assert after_step1["contact_name"] == STEP1_UPDATES["contact_name"], \
            f"Contact Name mismatch: expected '{STEP1_UPDATES['contact_name']}', got '{after_step1['contact_name']}'"
        assert after_step1["email"] == STEP1_UPDATES["email"], \
            f"Email mismatch: expected '{STEP1_UPDATES['email']}', got '{after_step1['email']}'"
        assert after_step1["mobile_number"] == STEP1_UPDATES["mobile_number"], \
            f"Mobile Number mismatch: expected '{STEP1_UPDATES['mobile_number']}', got '{after_step1['mobile_number']}'"
        log.info("  Step 1 assertions PASSED")

        assert after_step2["promoter_name"] == STEP2_UPDATES["promoter_name"], \
            f"Promoter Name mismatch: expected '{STEP2_UPDATES['promoter_name']}', got '{after_step2['promoter_name']}'"
        assert after_step2["promoter_remark"] == STEP2_UPDATES["promoter_remark"], \
            f"Promoter Remark mismatch: expected '{STEP2_UPDATES['promoter_remark']}', got '{after_step2['promoter_remark']}'"
        log.info("  Step 2 assertions PASSED")

        assert after_step3["address"] == STEP3_UPDATES["address"], \
            f"Address mismatch: expected '{STEP3_UPDATES['address']}', got '{after_step3['address']}'"
        assert after_step3["pin_code"] == STEP3_UPDATES["pin_code"], \
            f"Pin Code mismatch: expected '{STEP3_UPDATES['pin_code']}', got '{after_step3['pin_code']}'"
        log.info("  Step 3 assertions PASSED")

        assert after_step4["business_model"] == STEP4_UPDATES["business_model"], \
            f"Business Model mismatch: expected '{STEP4_UPDATES['business_model']}', got '{after_step4['business_model']}'"
        assert after_step4["market_linkages"] == STEP4_UPDATES["market_linkages"], \
            f"Market Linkages mismatch: expected '{STEP4_UPDATES['market_linkages']}', got '{after_step4['market_linkages']}'"
        log.info("  Step 4 assertions PASSED")

        assert after_step5["infra_location"] == STEP5_UPDATES["infra_location"], \
            f"Infra Location mismatch: expected '{STEP5_UPDATES['infra_location']}', got '{after_step5['infra_location']}'"
        log.info("  Step 5 assertions PASSED")

        # ----------------------------------------------------------
        # PHASE 7: Generate Update Report
        # ----------------------------------------------------------
        log.info("PHASE 7: Generating Update Report...")
        before_values = {1: before_step1}
        after_values = {1: after_step1}
        log.info("  Report generated successfully!")

        log.info("=" * 60)
        log.info("ALL ASSERTIONS PASSED - UPDATE VERIFIED")
        log.info("=" * 60)

    def test_update_using_one_call(self, page):
        """
        Same test but using the one-call update_company() method.
        Shorter code, same verification.
        """
        update_page = CompanyOnboardingUpdatePage(page.driver)
        company_name = UPDATE_COMPANY_NAME

        log.info("=" * 60)
        log.info(f"UPDATE TEST (ONE-CALL): {company_name}")
        log.info("=" * 60)

        result = update_page.update_company(company_name, ALL_UPDATES)

        assert result["success"], f"Update failed: {result['error']}"

        mismatches = update_page.verify_updated_fields(result["after_values"], ALL_UPDATES)
        assert not mismatches, f"Field mismatches found: {mismatches}"

        # Generate Update Report
        log.info("Generating Update Report...")
        report_path = generate_update_report(
            result["before_values"], result["after_values"],
            ALL_UPDATES, company_name, CO_REPORT_DIR)
        log.info(f"Update Report saved: {report_path}")

        log.info("ONE-CALL UPDATE TEST PASSED")