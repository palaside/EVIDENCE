@echo off
chcp 65001 >nul
title ติดตั้งระบบทำงานอัตโนมัติพร้อมเปิดเครื่อง (DIGITAL EVIDENCE)

set SCRIPT_DIR=%~dp0

echo ============================================================
echo   DIGITAL EVIDENCE — ติดตั้งระบบทำงานอัตโนมัติเบื้องหลัง
echo ============================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%tools\manage_startup.ps1" -Action install

echo.
echo ============================================================
echo  💡 วิธีใช้งาน (ทำงานตลอดเวลา ไม่ต้องจำคำสั่งอีกต่อไป):
echo  1. เพียงนำรูปสลิป หรือโฟลเดอร์สลิปมาวางใน:
echo     %SCRIPT_DIR%EVIDENCE_IN
echo  2. ระบบจะตรวจจับและแปลงเป็นไฟล์ Excel ส่งไปยัง:
echo     %SCRIPT_DIR%Folder_Out
echo     โดยอัตโนมัติทันที 24 ชม.
echo.
echo  * หากลง Windows ใหม่ในอนาคต: ดับเบิลคลิกไฟล์นี้ 1 ครั้ง จบเลย!
echo ============================================================
echo.
pause
