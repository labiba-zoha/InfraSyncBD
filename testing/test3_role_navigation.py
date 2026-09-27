# Uses Google Chrome via Selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("INFRASYNC_URL", "http://localhost:5173")
PASSWORD = os.getenv("INFRASYNC_DEMO_PASSWORD", "admin123")

ACCOUNTS = [
    ("Super Admin", "admin@infrasync.gov.bd", ["Dashboard", "Departments", "Account Verification", "User Access", "Reports"], ["Create Project", "Submit Complaint"]),
    ("Department Officer", "salman@rhd.gov.bd", ["Dashboard", "Projects", "Create Project", "Conflict Alerts", "Coordination", "Progress"], ["Departments", "User Access", "Submit Complaint"]),
    ("Contractor", "tariq@builder.com", ["Dashboard", "Projects", "Progress", "Complaints", "Inspections"], ["Create Project", "Departments", "Account Verification", "Reports"]),
    ("Citizen", "rahim@citizen.com", ["Dashboard", "Projects", "GIS Map", "Complaints", "Submit Complaint", "Notifications"], ["Create Project", "Account Verification", "Progress", "Inspections"]),
]

options = webdriver.ChromeOptions()
service_obj = Service()
driver = webdriver.Chrome(options=options, service=service_obj)
wait = WebDriverWait(driver, 30)


def go_to_clean_login():
    driver.get(f"{BASE_URL}/login")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    driver.execute_script("localStorage.removeItem('infrasync_token');")
    # The app has an older currentUser storage key in some copies. Remove it too.
    driver.execute_script("localStorage.removeItem('infrasync.mosh.v2.currentUser');")
    driver.get(f"{BASE_URL}/login")


def login(email):
    go_to_clean_login()
    email_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    password_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    email_box.clear(); email_box.send_keys(email)
    password_box.clear(); password_box.send_keys(PASSWORD)

    submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
    # JS click avoids CSS animation/overlay interception while still triggering React submit.
    driver.execute_script("arguments[0].click();", submit)

    try:
        wait.until(EC.url_contains("/dashboard"))
    except Exception:
        # Print the visible login error if authentication failed.
        errors = driver.find_elements(By.CSS_SELECTOR, "[class*='alertError']")
        if errors:
            print("LOGIN MESSAGE:", errors[0].text)
        raise

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav[aria-label='Main navigation']")))


def logout():
    button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='LOG OUT']")))
    driver.execute_script("arguments[0].click();", button)
    wait.until(EC.url_contains("/login"))


try:
    driver.maximize_window()

    for index, (role, email, must_have, must_not_have) in enumerate(ACCOUNTS, 1):
        print(f"\n[{index}/4] {role}: {email}")
        login(email)

        links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav[aria-label='Main navigation'] a")))
        nav_text = [x.text.strip() for x in links if x.text.strip()]
        print("Menu:", nav_text)

        for expected in must_have:
            assert expected in nav_text, f"{role} missing {expected}. Actual: {nav_text}"
        for forbidden in must_not_have:
            assert forbidden not in nav_text, f"{role} should not see {forbidden}. Actual: {nav_text}"

        print(f"[OK] {role} menu")
        logout()

    print("\nTEST 3 PASSED")
except Exception as exc:
    driver.save_screenshot("test3_failure.png")
    print("TEST 3 FAILED:", type(exc).__name__, exc)
    print("Current URL:", driver.current_url)
    print("Screenshot: testing\\test3_failure.png")
    raise
finally:
    driver.quit()
