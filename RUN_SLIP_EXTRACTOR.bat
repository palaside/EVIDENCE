@echo off
chcp 65001 >nul
title EVIDENCE SLIP EXTRACTOR — เครื่องมือสกัดสลิปอัตโนมัติ

set SCRIPT_DIR=%~dp0
set ENGINE=%SCRIPT_DIR%_skills\OCR_Slip\scripts\ocr_slip.py
set OUT_DIR=%SCRIPT_DIR%Folder_Out

if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"

REM Check if input was dragged onto this batch file
if not "%~1"=="" (
    echo ============================================================
    echo  [DETECTED] ตรวจพบไฟล์หรือโฟลเดอร์ที่ลากมาวาง:
    echo  %~1
    echo ============================================================
    echo.
    echo  [1] สกัดข้อมูลแบบปกติ (Standard Legal Ledger)
    echo  [2] สกัดข้อมูลพร้อมเซ็นเซอร์ข้อมูลส่วนบุคคล PDPA (--mask-pii)
    echo.
    set /p CHOICE="เลือกโหมดการทำงาน (1 หรือ 2) [กด Enter = 1]: "
    if "%CHOICE%"=="2" (
        python "%ENGINE%" --input "%~1" --mask-pii --output "%OUT_DIR%\Slip_Result_Masked.xlsx"
    ) else (
        python "%ENGINE%" --input "%~1" --output "%OUT_DIR%\Slip_Result.xlsx"
    )
    echo.
    echo [เสร็จสมบูรณ์] ผลลัพธ์ถูกบันทึกไว้ที่: %OUT_DIR%
    pause
    exit /b
)

:MENU
cls
echo ============================================================
echo   🏛️ DIGITAL EVIDENCE — เครื่องมือสกัดสลิปและตีตารางอัตโนมัติ
echo ============================================================
echo.
echo   [1] สแกนสลิปจากโฟลเดอร์ KTB (ฉบับปกติ)
echo   [2] สแกนสลิปจากโฟลเดอร์ TTB (ฉบับปกติ)
echo   [3] สแกนสลิปทั้งหมดพร้อม "เซ็นเซอร์ข้อมูลส่วนบุคคล PDPA" (--mask-pii)
echo   [4] พิมพ์พาทโฟลเดอร์หรือไฟล์ที่ต้องการสแกนเอง
echo   [5] เปิดโฟลเดอร์รับผลลัพธ์ (Folder_Out)
echo   [6] ติดตั้งให้ระบบตื่นมาทำงานเงียบๆ อัตโนมัติทุกครั้งที่เปิดเครื่อง (Startup)
echo   [0] ออกจากโปรแกรม
echo.
echo ============================================================
set /p MENU_CHOICE="กรุณาเลือกเมนู (0-6): "

if "%MENU_CHOICE%"=="1" (
    echo.
    echo กำลังสแกนสลิป KTB...
    python "%ENGINE%" --input "F:\Project\EDOK\Final_A4_Output\KTB" --output "%OUT_DIR%\KTB_Summary.xlsx"
    echo.
    echo [เสร็จสมบูรณ์] บันทึกลง: %OUT_DIR%\KTB_Summary.xlsx
    pause
    goto MENU
)

if "%MENU_CHOICE%"=="2" (
    echo.
    echo กำลังสแกนสลิป TTB...
    python "%ENGINE%" --input "F:\Project\EDOK\Final_A4_Output\TTB" --output "%OUT_DIR%\TTB_Summary.xlsx"
    echo.
    echo [เสร็จสมบูรณ์] บันทึกลง: %OUT_DIR%\TTB_Summary.xlsx
    pause
    goto MENU
)

if "%MENU_CHOICE%"=="3" (
    echo.
    echo กำลังสแกนพร้อมเซ็นเซอร์ข้อมูลส่วนบุคคล PDPA...
    python "%ENGINE%" --input "F:\Project\EDOK\Final_A4_Output" --mask-pii --output "%OUT_DIR%\All_Slips_MaskedPII.xlsx"
    echo.
    echo [เสร็จสมบูรณ์] บันทึกลง: %OUT_DIR%\All_Slips_MaskedPII.xlsx
    pause
    goto MENU
)

if "%MENU_CHOICE%"=="4" (
    echo.
    set /p CUSTOM_PATH="วางพาทโฟลเดอร์หรือไฟล์รูปภาพที่ต้องการสแกน: "
    echo.
    echo  [1] สกัดปกติ
    echo  [2] สกัดพร้อมเซ็นเซอร์ข้อมูลส่วนบุคคล (--mask-pii)
    set /p SUB_CHOICE="เลือกรูปแบบ (1 หรือ 2): "
    if "%SUB_CHOICE%"=="2" (
        python "%ENGINE%" --input "%CUSTOM_PATH%" --mask-pii --output "%OUT_DIR%\Custom_Masked.xlsx"
    ) else (
        python "%ENGINE%" --input "%CUSTOM_PATH%" --output "%OUT_DIR%\Custom_Result.xlsx"
    )
    echo.
    echo [เสร็จสมบูรณ์] ตรวจสอบไฟล์ได้ใน %OUT_DIR%
    pause
    goto MENU
)

if "%MENU_CHOICE%"=="5" (
    start "" "%OUT_DIR%"
    goto MENU
)

if "%MENU_CHOICE%"=="6" (
    call "%SCRIPT_DIR%install_startup.bat"
    pause
    goto MENU
)

if "%MENU_CHOICE%"=="0" exit /b
goto MENU
