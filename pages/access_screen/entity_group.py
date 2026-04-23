"""
pages/access_screen/entity_group.py
------------------------------------
Entity Group Definition screen — create only.
Uses _fill_field() pattern that can be reused across all screen files.

Usage:
    from pages.access_screen.entity_group import create_entity_group
    create_entity_group(driver, wait, "Admin Role", "2")
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S'
    ))
    logger.addHandler(console)


# ================================================================
# PRIVATE HELPERS
# ================================================================

def _fill_field(driver, wait, label_text, value):
    """Fill any mat-form-field input by its visible label text.
    Uses send_keys with JS fallback for Angular Material inputs."""
    logger.info(f"  Filling '{label_text}' = '{value}'")

    input_el = wait.until(EC.element_to_be_clickable(
        (By.XPATH,
         f"//mat-label[normalize-space()='{label_text}']"
         f"/ancestor::mat-form-field//input")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_el)
    time.sleep(0.3)

    try:
        input_el.click()
        input_el.clear()
        input_el.send_keys(value)
    except Exception:
        logger.warning(f"  send_keys failed for '{label_text}', using JS fallback.")
        driver.execute_script("arguments[0].value = arguments[1];", input_el, value)


def _check_result(driver, wait):
    """Check if submit succeeded or failed after form submission."""
    time.sleep(2)

    # Check for error alert
    try:
        error = driver.find_element(
            By.CSS_SELECTOR, ".alert-danger, .toast-error, .snack-bar-error"
        )
        if error.is_displayed():
            error_text = error.text.strip()
            logger.error(f"  Submit failed: {error_text}")
            raise Exception(f"Submit failed: {error_text}")
    except NoSuchElementException:
        pass

    # Check for SweetAlert success popup
    try:
        driver.find_element(By.CSS_SELECTOR, ".swal2-success")
        logger.info("  Submit succeeded (SweetAlert confirmed).")
        # Auto-dismiss the popup
        try:
            ok_btn = driver.find_element(By.CSS_SELECTOR, ".swal2-confirm")
            driver.execute_script("arguments[0].click();", ok_btn)
            time.sleep(0.5)
        except Exception:
            pass
    except NoSuchElementException:
        logger.info("  No SweetAlert popup — checking for inline success.")
        # Some apps show inline toast instead of SweetAlert
        try:
            toast = driver.find_element(
                By.CSS_SELECTOR, ".toast-success, .snack-bar-success"
            )
            if toast.is_displayed():
                logger.info(f"  Success toast: {toast.text.strip()}")
        except NoSuchElementException:
            pass


# ================================================================
# MAIN FUNCTION
# ================================================================

def create_entity_group(driver, wait, group_name, level):
    """
    Navigate to Entity Group Definition form, fill and submit.

    Args:
        driver: Selenium WebDriver instance (already logged in, already on page)
        wait: WebDriverWait instance
        group_name: Entity Group Name (str)
        level: Level value (str or int)

    Raises:
        Exception: If submit fails (duplicate, validation error, etc.)
    """
    logger.info(f"Creating Entity Group: '{group_name}' with Level '{level}'")

    # 1. Click Add button
    logger.info("  Clicking Add button...")
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class,'mat-fab') or .//mat-icon[text()='add']]")
    ))
    driver.execute_script("arguments[0].click();", add_btn)
    time.sleep(1)

    # 2. Fill form fields
    _fill_field(driver, wait, "Entity Group Name", group_name)
    _fill_field(driver, wait, "Level", level)

    # 3. Submit
    logger.info("  Clicking Submit...")
    submit = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']//span[normalize-space()='Submit']")
    ))
    driver.execute_script("arguments[0].click();", submit)

    # 4. Verify result
    _check_result(driver, wait)

    logger.info(f"Done: Entity Group '{group_name}' with Level '{level}'")