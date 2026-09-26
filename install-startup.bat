@echo off
chcp 65001 >nul
echo [INSTALL] Registering Silent Heartbeat Suite to Windows Startup...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_VBS=%STARTUP_DIR%\DigitalEvidence_Heartbeat.vbs"

echo Set WshShell = CreateObject("WScript.Shell") > "%SHORTCUT_VBS%"
echo WshShell.Run "python ""%~dp0tick.py""", 0, False >> "%SHORTCUT_VBS%"
echo Set WshShell = Nothing >> "%SHORTCUT_VBS%"

echo [OK] Heartbeat registered at: %SHORTCUT_VBS%
echo [OK] Ready for silent background operation.
pause
