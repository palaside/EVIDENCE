@echo off
setlocal
cd /d "%~dp0"
title DIGITAL EVIDENCE - Forensic Processing Suite

set "PY="
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY=python"
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PY=py"
    ) else if exist "%USERPROFILE%\miniconda3\python.exe" (
        set "PY=%USERPROFILE%\miniconda3\python.exe"
    ) else if exist "C:\Python311\python.exe" (
        set "PY=C:\Python311\python.exe"
    ) else if exist "C:\Python310\python.exe" (
        set "PY=C:\Python310\python.exe"
    )
)

if "%PY%"=="" (
    echo [ERROR] Python not found in system! Please install Python.
    pause
    exit /b 1
)

"%PY%" "core\launcher.py" %*
if %errorlevel% neq 0 (
    pause
)
