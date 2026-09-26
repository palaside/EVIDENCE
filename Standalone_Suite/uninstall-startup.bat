@echo off
chcp 65001 >nul
echo [DIGITAL EVIDENCE] Removing Silent Background Service from Windows Startup...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%STARTUP_FOLDER%\DigitalEvidence_Watcher.lnk" (
    del "%STARTUP_FOLDER%\DigitalEvidence_Watcher.lnk"
    echo [SUCCESS] Service uninstalled successfully.
) else (
    echo [INFO] Service shortcut was not found in Startup.
)
pause
