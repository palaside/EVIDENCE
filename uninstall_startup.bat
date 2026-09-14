@echo off
chcp 65001 >nul
title ถอนการติดตั้งระบบทำงานอัตโนมัติ (DIGITAL EVIDENCE)

set SCRIPT_DIR=%~dp0

echo ============================================================
echo   🛑 DIGITAL EVIDENCE — ถอนการติดตั้งระบบทำงานอัตโนมัติ
echo ============================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%tools\manage_startup.ps1" -Action uninstall

echo.
pause
