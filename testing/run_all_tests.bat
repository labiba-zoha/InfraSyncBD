@echo off
setlocal
cd /d "%~dp0"

echo ==============================================================
echo InfraSync BD - GOOGLE CHROME Selenium Test Runner
echo ==============================================================
echo.

python preflight.py
if errorlevel 1 (
  echo.
  echo PRECHECK FAILED. Selenium tests were NOT started.
  echo Fix the [FAIL] item above first.
  pause
  exit /b 1
)

echo.
echo Checking Google Chrome / ChromeDriver...
python test0_chrome_check.py
if errorlevel 1 (
  echo.
  echo GOOGLE CHROME CHECK FAILED.
  echo Run: python -m pip install -U selenium
  echo Make sure Google Chrome is installed.
  pause
  exit /b 1
)

echo.
echo Running Test 1 in Google Chrome...
python test1_navigation.py
if errorlevel 1 goto :failed

echo.
echo Running Test 2 in Google Chrome...
python test2_admin_login.py
if errorlevel 1 goto :failed

echo.
echo Running Test 3 in Google Chrome...
python test3_role_navigation.py
if errorlevel 1 goto :failed

echo.
echo ==============================================================
echo ALL 3 GOOGLE CHROME TESTS PASSED
echo ==============================================================
pause
exit /b 0

:failed
echo.
echo ==============================================================
echo A GOOGLE CHROME SELENIUM TEST FAILED.
echo Send the COMPLETE traceback and the generated failure PNG.
echo ==============================================================
pause
exit /b 1
