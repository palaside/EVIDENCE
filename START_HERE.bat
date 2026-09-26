@echo off
chcp 65001 >nul
title DIGITAL EVIDENCE — Forensic Dashboard & Native Backend Engine
echo ===============================================================================
echo   🏛️ DIGITAL EVIDENCE — NATIVE PRODUCTION FORENSIC SYSTEM
echo   Single Source of Truth: core/evidence_theme.py
echo ===============================================================================
echo.
echo [1/2] กำลังเริ่มทำงาน Forensic Backend Server (Port 8088)...
start "Digital Evidence Server" /B python server.py
timeout /t 2 /nobreak >nul

echo [2/2] กำลังเปิดหน้าต่างแดชบอร์ด Digital Evidence...
start http://localhost:8088/index.html

echo.
echo  ===============================================================================
echo   ✓ ระบบพร้อมทำงาน 100%% ALL GREEN
echo   ⚡ Web Dashboard: http://localhost:8088
echo   📂 โฟลเดอร์นำเข้า: EVIDENCE_CHAT_IN / EVIDENCE_IN
echo   📂 โฟลเดอร์ส่งออก: Folder_Out
echo  ===============================================================================
echo.
pause
