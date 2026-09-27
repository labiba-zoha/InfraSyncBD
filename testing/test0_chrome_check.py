import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("INFRASYNC_URL", "http://localhost:5173")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# Selenium Manager will automatically locate/download a compatible
# ChromeDriver when Selenium 4.6+ and Google Chrome are installed.
service_obj = Service()

print("Starting Google Chrome...")
try:
    driver = webdriver.Chrome(options=options, service=service_obj)
except Exception as exc:
    print("CHROME CHECK FAILED")
    print(type(exc).__name__ + ":", exc)
    print()
    print("Make sure Google Chrome is installed and Selenium is up to date:")
    print("  python -m pip install -U selenium")
    raise

try:
    driver.get(BASE_URL + "/login")
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return document.readyState") == "complete")
    print("[OK] Google Chrome opened")
    print("[OK] Current URL:", driver.current_url)
    print("[OK] Page title:", driver.title)
    print("CHROME CHECK PASSED")
finally:
    driver.quit()
