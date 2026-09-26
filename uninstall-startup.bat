@echo off
chcp 65001 >nul
echo [UNINSTALL] Removing Silent Heartbeat Suite from Windows Startup...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_VBS=%STARTUP_DIR%\DigitalEvidence_Heartbeat.vbs"

if exist "%SHORTCUT_VBS%" (
    del /f /q "%SHORTCUT_VBS%"
    echo [OK] Heartbeat service removed.
) else (
    echo [INFO] No startup entry found.
)
pause
