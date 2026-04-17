@echo off
REM ============================================================
REM  start.bat  -  Start the Process Dashboard
REM
REM  Port 8888 is used so it does not clash with your existing
REM  apps on 8000 and 8080.
REM
REM  --noreload is required so process handles stay in memory.
REM ============================================================

set "PY=C:\Program Files\Python313\python.exe"

echo.
echo  Starting Process Dashboard...
echo  Open http://localhost:8888/dashboard/ in your browser
echo  Press Ctrl+C to stop.
echo.

"%PY%" manage.py runserver 0.0.0.0:8888 --noreload
