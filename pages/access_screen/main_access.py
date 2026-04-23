import sys
import os
import time
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import MODULE_LOGIN_URL, PACS_EMAIL, PACS_PASSWORD, PACS_FACILITY
from common.nav_section import navigate_to
from pages.access_screen.Acess_screens.entity_group import create_entity_group
from pages.access_screen.Acess_screens.role_creation import create_role
from pages.access_screen.Acess_screens.user_creation import create_user


#dataImportsForAll
from common.test_data import entity_group_data, role_creation_data, user_creation_data



# ── Logger ──
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S'))
    logger.addHandler(console)


# ──────────────────────────────────────────────
# DRIVER SETUP
# ──────────────────────────────────────────────

def build_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────

def login(driver, wait):
    logger.info("--- LOGIN ---")
    driver.get(MODULE_LOGIN_URL)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@formcontrolname='email']")
    )).send_keys(PACS_EMAIL)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//mat-select")
    )).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//mat-option//span[contains(text(),'{PACS_FACILITY}')]")
    )).click()

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@formcontrolname='password']")
    )).send_keys(PACS_PASSWORD)

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    )

    time.sleep(3)
    logger.info("Login Done")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

driver = build_driver()
wait = WebDriverWait(driver, 60)

try:
    login(driver, wait)

    # ── NAV TEST ──
    # navigate_to(driver, wait, "Access", "Entity Group Definition")
    # navigate_to(driver, wait, "Access", "Role Creation Screen")
    # navigate_to(driver, wait, "Access", "Role Screen Link")
    # navigate_to(driver, wait, "Access", "User Creation Screen")
    # navigate_to(driver, wait, "Access", "Screen Api Link")

    # ── ENTITY GROUP ──
    # navigate_to(driver, wait, "Access", "Entity Group Definition")
    # create_entity_group(driver, wait, **entity_group_data)

    # ── ROLE CREATION ──
    # navigate_to(driver, wait, "Access", "Role Creation Screen")
    # create_role(driver, wait, **role_creation_data)

    # ── ROLE SCREEN LINK ──
    # navigate_to(driver, wait, "Access", "Role Screen Link")
    # create_role_screen_link(driver, wait, ...)

    # ── USER CREATION ──
    navigate_to(driver, wait, "Access", "User Creation Screen")
    create_user(driver, wait, **user_creation_data)

    # ── SCREEN API LINK ──
    # navigate_to(driver, wait, "Access", "Screen Api Link")
    # create_screen_api_link(driver, wait, ...)

    logger.info("SUCCESS: All forms filled!")
    time.sleep(5)

finally:
    driver.quit()