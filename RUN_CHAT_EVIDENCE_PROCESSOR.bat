@echo off
chcp 65001 >nul
title DIGITAL EVIDENCE — ตัวประมวลผลภาพแชทหลักฐาน (Chat Evidence Processor)

set SCRIPT_DIR=%~dp0
set ENGINE=%SCRIPT_DIR%tools\process_real_chat_evidence.py
set OUT_DIR=%SCRIPT_DIR%Folder_Out

cls
echo ============================================================
echo   🏛️ DIGITAL EVIDENCE — ตัวประมวลผลภาพแชทหลักฐานคดี
echo ============================================================
echo.
echo   โฟลเดอร์ต้นทางที่ตั้งค่าไว้ (เรียงตามลำดับ 1 -> 2 -> 3):
echo   [1] F:\Project\EDOK\แชทที่ 1  (322 รูป)
echo   [2] F:\Project\EDOK\แชทที่ 2  (6 รูป)
echo   [3] F:\Project\EDOK\แชทที่ 3  (143 รูป)
echo.
echo   ผลลัพธ์ที่จะได้ใน %OUT_DIR%:
echo   - Evidence_Chat_Volume_1.pdf + สารบัญสลิป (Excel/JSON)
echo   - Evidence_Chat_Volume_2.pdf + สารบัญสลิป (Excel/JSON)
echo   - Evidence_Chat_Volume_3.pdf + สารบัญสลิป (Excel/JSON)
echo   - Evidence_Chat_Master_Combined_Vol1_to_3.pdf (ฉบับรวมเล่มสมบูรณ์)
echo.
echo ============================================================
echo   [1] เริ่มการประมวลผลทั้ง 3 เล่มทันที (Start Processing)
echo   [2] เปิดโฟลเดอร์ผลลัพธ์ (Open Folder_Out)
echo   [0] ออกจากโปรแกรม
echo ============================================================
set /p CHOICE="เลือกตัวเลือก (0-2): "

if "%CHOICE%"=="1" (
    echo.
    echo กำลังตรวจหา Python ในระบบ...
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
        ) else if exist "C:\miniconda3\python.exe" (
            set "PY=C:\miniconda3\python.exe"
        ) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
            set "PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        ) else if exist "C:\Python311\python.exe" (
            set "PY=C:\Python311\python.exe"
        ) else if exist "C:\Python310\python.exe" (
            set "PY=C:\Python310\python.exe"
        )
    )

    if "%PY%"=="" (
        echo [ERROR] ไม่พบ Python ในระบบ! กรุณาติดตั้ง Python หรือเปิดใช้งาน Miniconda
        pause
        exit /b 1
    )

    echo ตรวจพบ Python: %PY%
    echo กำลังเริ่มประมวลผล กรุณารอสักครู่...
    "%PY%" "%ENGINE%"
    echo.
    echo [เสร็จสมบูรณ์] ตรวจสอบเอกสารทั้งหมดได้ที่: %OUT_DIR%
    start "" "%OUT_DIR%"
    pause
    exit /b
)

if "%CHOICE%"=="2" (
    start "" "%OUT_DIR%"
    exit /b
)

if "%CHOICE%"=="0" exit /b
