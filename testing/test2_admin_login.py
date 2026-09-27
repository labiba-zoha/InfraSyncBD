# Uses Google Chrome via Selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("INFRASYNC_URL", "http://localhost:5173")
EMAIL = os.getenv("INFRASYNC_ADMIN_EMAIL", "admin@infrasync.gov.bd")
PASSWORD = os.getenv("INFRASYNC_ADMIN_PASSWORD", "admin123")

options = webdriver.ChromeOptions()
service_obj = Service()
driver = webdriver.Chrome(options=options, service=service_obj)
wait = WebDriverWait(driver, 30)

try:
    driver.maximize_window()
    driver.get(f"{BASE_URL}/login")
    # Remove any stale session from earlier manual testing.
    driver.execute_script("localStorage.clear();")
    driver.get(f"{BASE_URL}/login")

    email_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    password_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    email_box.send_keys(EMAIL)
    password_box.send_keys(PASSWORD)

    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
    driver.execute_script("arguments[0].click();", submit)

    # Successful login redirects /login -> / -> /dashboard.
    wait.until(EC.url_contains("/dashboard"))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav[aria-label='Main navigation']")))
    print("[OK] Super Admin login")

    verification = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Account Verification")))
    driver.execute_script("arguments[0].click();", verification)
    wait.until(EC.url_contains("/verification"))
    print("[OK] Account Verification route")

    logout = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='LOG OUT']")))
    driver.execute_script("arguments[0].click();", logout)
    wait.until(EC.url_contains("/login"))
    print("[OK] Logout")

    print("TEST 2 PASSED")
except Exception as exc:
    driver.save_screenshot("test2_failure.png")
    print("TEST 2 FAILED:", type(exc).__name__, exc)
    print("Current URL:", driver.current_url)
    print("Screenshot: testing\\test2_failure.png")
    raise
finally:
    driver.quit()
