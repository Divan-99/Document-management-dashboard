@echo off
REM ============================================================
REM  setup.bat  -  First-time setup for Process Dashboard
REM  Run this ONCE from the process_dashboard\ folder.
REM ============================================================

set "PY=C:\Program Files\Python313\python.exe"

echo.
echo === Process Dashboard - First Time Setup ===
echo.

REM Check Python exists
if not exist "%PY%" (
    echo ERROR: Python not found at %PY%
    echo Please update the PY variable in this file to point to your Python install.
    pause
    exit /b 1
)

echo Python found: %PY%
echo.

REM Install Django
echo Installing Django...
"%PY%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause
    exit /b 1
)

REM Run migrations
echo.
echo Running database migrations...
"%PY%" manage.py migrate

REM Create admin user
echo.
echo === Create your login account ===
echo (Use this username and password to sign into the dashboard)
echo.
"%PY%" manage.py createsuperuser

echo.
echo =============================================
echo  Setup complete!
echo =============================================
echo.
echo To start the dashboard run:   start.bat
echo Then open:   http://localhost:8888/dashboard/
echo.
pause
