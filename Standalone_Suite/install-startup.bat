@echo off
chcp 65001 >nul
echo [DIGITAL EVIDENCE] Installing Silent Background Service to Windows Startup...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_PATH=%~dp0tools\run-silent.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%STARTUP_FOLDER%\DigitalEvidence_Watcher.lnk" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "wscript.exe" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Arguments = """%VBS_PATH%""" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"

cscript //nologo "%TEMP%\create_shortcut.vbs"
del "%TEMP%\create_shortcut.vbs" 2>nul

echo [SUCCESS] Service installed successfully. Daemon will run quietly on Windows startup.
pause
