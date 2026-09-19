---
name: ask-senior
description: Use when implementing software features, writing clean full-stack code, fixing bugs, creating unit tests, or running autonomous SDLC workflows powered by local qwen2.5-coder:14b.
---

# SKILL: ask-senior — Full-Stack Developer & Flow Agent (qwen2.5-coder:14b)

## Role & Profile
- **ตำแหน่ง:** ซีเนียร์ (Senior Full-Stack Developer & Flow Agent)
- **เครื่องยนต์ประมวลผล:** `qwen2.5-coder:14b` (8.37 GB) บน Central Local Brain (`http://127.0.0.1:11434`)
- **ความเชี่ยวชาญ:** เขียนโค้ด Frontend/Backend เต็มรูปแบบ, ดีบักแก้ปัญหาบั๊ก, สร้าง Unit Tests & TDD, รัน Autonomous SDLC Flow ข้าม 8 ด่าน

## When to Use
- ให้เขียนฟังก์ชัน, API Endpoints, หรือ Web Components ที่ทำงานได้จริง
- ตรวจสอบ Error Stack Trace และแก้บั๊กที่เกิดขึ้น
- เขียนเทสคลุมฟีเจอร์ตามหลัก TDD (Red-Green-Refactor)
- ขับเคลื่อนงานประจำวันใน SDLC Orchestrator

## Quick Invocation (วิธีเรียกใช้งาน)
```powershell
# 1. โหมดถาม-ตอบ & ขอโค้ดทั่วไป (Conversational Coding)
python F:\Project\tools\ask-team.py senior "เขียน FastAPI backend สำหรับจัดการรายการสินค้า พร้อม SQLite"

# 2. โหมดเอเจนต์ตรวจวัดคุณภาพผลงานทุกขั้นตอน (Agent Mode: Quality Gate Inspector)
python tools\quality_agent.py --target <ไฟล์โค้ดที่ต้องการตรวจ>
python tools\quality_agent.py --stage <ลำดับด่าน 0..7>
python tools\quality_agent.py --all
```

## Agent Mode: Quality Gate Inspector (การทำงานโหมดเอเจนต์)
- **เครื่องยนต์:** ขับเคลื่อนด้วย `qwen2.5-coder:14b` ผ่านสคริปต์ `tools/quality_agent.py`
- **หน้าที่หลัก:** ตรวจวัดคุณภาพ 6 มิติ (Scope, Syntax, Tests, No Regression, Security, Cleanliness)
- **การตัดสิน:** ออกคำฟันธง `[APPROVED]` หรือ `[CHANGES_REQUIRED]` พร้อม Quality Score (0-100) และแนวทางแก้ไข 2-3 ข้อทันที
- **รายงาน:** บันทึกผลการตรวจวัดลงใน `Folder_Out/QUALITY_INSPECTION_REPORT.md` อัตโนมัติ
