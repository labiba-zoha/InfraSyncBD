from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# -------------------------------------------------------------
# Selenium Test for InfraSync BD
# -------------------------------------------------------------

# To Keep Browser Open Indefinitely
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# Chrome Driver setup
service_obj = Service()
driver = webdriver.Chrome(options=options, service=service_obj)

# Maximize the browser window
driver.maximize_window()

# Navigate to the local Vite development server
print("Navigating to http://localhost:5173/login...")
driver.get("http://localhost:5173/login")

# Add a small delay to ensure the page is fully loaded
time.sleep(2) 

print("Entering credentials...")
# Find the email field by its type and enter the demo email
driver.find_element(By.XPATH, "//input[@type='email']").send_keys("admin@infrasync.bd")

# Find the password field by its type and enter the demo password
driver.find_element(By.XPATH, "//input[@type='password']").send_keys("demo123")

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

print("Clicking the login button...")
# Scroll to button to avoid interception, then click
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
ActionChains(driver).move_to_element(submit_button).perform()
time.sleep(1) # wait for scroll
submit_button.click()

# Wait for URL to change or error to appear
try:
    WebDriverWait(driver, 5).until(EC.url_changes("http://localhost:5173/login"))
except:
    pass # Let the next lines handle it

# Check for error messages
error_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'alertError')]")
if error_elements:
    print("Login Error displayed:", error_elements[0].text)

print("Current URL after login:", driver.current_url)

# Note: You can add assert statements here to verify the login was successful
if "dashboard" in driver.current_url:
    print("Test Passed: Successfully logged in and navigated to the dashboard.")
else:
    print("Test Failed: Did not navigate to the dashboard.")
