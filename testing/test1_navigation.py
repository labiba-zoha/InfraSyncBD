# Uses Google Chrome via Selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("INFRASYNC_URL", "http://localhost:5173")
options = webdriver.ChromeOptions()
service_obj = Service()
driver = webdriver.Chrome(options=options, service=service_obj)
wait = WebDriverWait(driver, 20)

try:
    driver.maximize_window()
    driver.get(f"{BASE_URL}/login")

    heading = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[contains(., 'Welcome back')]"))
    )
    assert "Welcome back" in heading.text
    print("[OK] Login page")

    signup = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Create an account')]"))
    )
    signup.click()
    wait.until(EC.url_contains("/signup"))
    print("[OK] Signup navigation")

    driver.back()
    wait.until(EC.url_contains("/login"))
    print("[OK] Back navigation")

    driver.forward()
    wait.until(EC.url_contains("/signup"))
    print("[OK] Forward navigation")

    driver.refresh()
    wait.until(EC.url_contains("/signup"))
    print("[OK] Refresh")

    print("TEST 1 PASSED")
except Exception as exc:
    driver.save_screenshot("test1_failure.png")
    print("TEST 1 FAILED:", type(exc).__name__, exc)
    print("Screenshot: testing\\test1_failure.png")
    raise
finally:
    driver.quit()
