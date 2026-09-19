@echo off
REM ==============================================================================
REM DIGITAL EVIDENCE - WINRAR SFX ENCRYPTED CONTAINER LAUNCHER
REM Standalone Zero-Command Tool
REM ==============================================================================

cd /d "%~dp0"

set PYTHON_EXE=python
where %PYTHON_EXE% >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Users\EVE\miniconda3\python.exe" (
        set PYTHON_EXE=C:\Users\EVE\miniconda3\python.exe
    )
)

start "" "%PYTHON_EXE%" "tools\build_sfx_evidence_package.py"
exit /b 0
