@echo off
REM DIGITAL_EVIDENCE standalone launcher: ensure :1453 server, then open dashboard
set SRV=F:\Project\PYTHON_FOUNDATION_OS_Package\server.py
set DASH=F:\Project\evidence-webapp\dashboard.html
python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:1453/health', timeout=5)" 2>nul
if %errorlevel% neq 0 (
  start "" pythonw "%SRV%"
  timeout /t 6 >nul
)
start "" "%DASH%"
