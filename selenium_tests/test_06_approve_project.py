import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Configure Chrome options to keep the browser open after script ends
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Initialize the Chrome driver service
service_obj = Service()
driver = webdriver.Chrome(options=options, service=service_obj)

# Maximize the browser window
driver.maximize_window()
# Login as Admin
driver.get("http://localhost:5173/login")
time.sleep(2)
driver.find_element(By.XPATH, "//input[@type='email']").send_keys("admin@infrasync.gov.bd")
driver.find_element(By.XPATH, "//input[@type='password']").send_keys("admin123")
login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
driver.execute_script("arguments[0].click();", login_btn)
time.sleep(3)

# Navigate to Approvals Page
driver.get("http://localhost:5173/approvals")
time.sleep(2)

# Click on an Approve button
try:
    approve_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Approve')]")
    if approve_buttons:
        driver.execute_script("arguments[0].scrollIntoView(true);", approve_buttons[0])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", approve_buttons[0])
        time.sleep(2)
        print("Test 6: Clicked Approve button successfully.")
    else:
        print("Test 6: No projects pending approval found.")
except Exception as e:
    print("Test 6: Failed to approve project:", e)
