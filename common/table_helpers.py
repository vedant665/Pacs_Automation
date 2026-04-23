"""
common/table_helpers.py
-----------------------
Reusable table search + verify for any app-table in the PACS app.

Usage:
    from common.table_helpers import verify_in_table
    verify_in_table(driver, wait, "Admin Role", "name")
    verify_in_table(driver, wait, "Demo Group", "entity_group", check_date=False)
"""

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging

logger = logging.getLogger(__name__)


def verify_in_table(driver, wait, search_value, column_class, check_date=True):
    """
    Search for a value in the app-table and optionally verify creation date.

    Flow:
        1. Click search button to reveal input
        2. Type search_value into #erpSearchInput
        3. Check for 'No results' row
        4. Confirm value exists in the specified column
        5. Optionally verify creation date matches today
        6. Clear search to restore full table

    Args:
        driver:       Selenium WebDriver instance
        wait:         WebDriverWait instance
        search_value: text to search (e.g. role name, entity group name)
        column_class: cdk-column-* class (without 'cdk-column-' prefix),
                      e.g. 'name', 'entity_group'
        check_date:   if True, also verifies created_date_time starts
                      with today's date. Default True.

    Raises:
        Exception: if value not found or date doesn't match.
    """
    logger.info(f"  Verifying '{search_value}' in table (column: {column_class})...")

    # 1. Click search button
    try:
        search_btn = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.search-btn, button[aria-label='Search']")
        ))
        driver.execute_script("arguments[0].click();", search_btn)
        time.sleep(0.5)
    except Exception:
        logger.warning("  Could not click search button, trying input directly.")

    # 2. Type into search input
    search_input = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR,
         "input.search-input, "
         ".erp-search-container input, "
         "input[placeholder*='Search'], "
         "input[type='search']")
    ))
    search_input.clear()
    search_input.send_keys(search_value)
    time.sleep(1.5)

    # 3. Check for "No results" row
    try:
        no_data = driver.find_element(
            By.XPATH,
            "//*[contains(@class,'mat-mdc-no-data-row') or "
            "contains(text(),'No results found') or "
            "contains(text(),'No data found')]"
        )
        if no_data.is_displayed():
            raise Exception(
                f"Verification FAILED: '{search_value}' not found "
                f"(table shows: '{no_data.text.strip()}')"
            )
    except NoSuchElementException:
        pass

    # 4. Confirm value exists in the column
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH,
             f"//td[contains(@class,'cdk-column-{column_class}')]"
             f"//span[normalize-space()='{search_value}']")
        ))
        logger.info(f"  Found '{search_value}' in '{column_class}' column.")
    except TimeoutException:
        raise Exception(
            f"Verification FAILED: '{search_value}' not in '{column_class}' column."
        )

    # 5. Optionally check creation date matches today
    if check_date:
        today_str = datetime.now().strftime("%d-%b-%Y")
        try:
            date_cell = wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 f"//td[contains(@class,'cdk-column-created_date_time')]//span")
            ))
            date_text = date_cell.text.strip()
            if date_text.startswith(today_str):
                logger.info(f"  Date verified: {date_text} matches today ({today_str}).")
            else:
                raise Exception(
                    f"Date mismatch: expected {today_str}, got '{date_text}'."
                )
        except TimeoutException:
            logger.warning("  Could not find 'created_date_time' column — skipping date check.")

    # 6. Clear search
    try:
        search_input.clear()
        time.sleep(0.5)
    except Exception:
        pass

    logger.info(f"  Verification PASSED for '{search_value}'.")