@echo off
REM ==============================================================================
REM DIGITAL EVIDENCE - AUTONOMOUS QUALITY AGENT LAUNCHER
REM Powered by: ask-senior (qwen2.5-coder:14b)
REM ==============================================================================

cd /d "%~dp0"

set PYTHON_EXE=python
where %PYTHON_EXE% >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Users\EVE\miniconda3\python.exe" (
        set PYTHON_EXE=C:\Users\EVE\miniconda3\python.exe
    )
)

echo [QUALITY AGENT] Launching Autonomous Quality Gate Inspector...
"%PYTHON_EXE%" "tools\quality_agent.py" --all
pause
exit /b 0
