---
name: SET-AGENTS
description: ชุดเซ็ตสมองเอเจนต์นักพัฒนา (ย่อจากเซตสมอง 3 ไฟล์) — สั่ง "เซ็ต SET-AGENTS" แล้วเอเจนต์ทำงานแบบชุดพัฒนา: Inspect+TDD+gatekeeping+savetoken+save/resume+QC 5 ขั้น
---

# SKILL: SET-AGENTS — ชุดสมองเอเจนต์

## ต้นฉบับเต็ม
- `เซตสมอง/AI AGENTS/AGENTS.md` (Hub หลัก) · `AGENTS-UNIVERSAL.md` (ธรรมนูญกลาง) · `BRAIN.md` (ร่างไฟล์เดียว)

## DNA (บังคับ)
- Inspect Before Act ห้ามเดา path/API; ตรวจ Exit Code/Stderr ทุกคำสั่ง; TDD; แยกโมดูล; ปฏิเสธโค้ดเสี่ยง/Memory Leak/Technical Debt
- Secrets: อ่านแค่ชื่อ Key ห้ามโชว์ค่า ห้าม hardcode; รันทำลายล้างห้ามเด็ดขาด; server รัน background + จด PID/วิธีหยุด

## ประหยัดโทเค็น (savetoken)
- YAGNI + diff สั้น; บีบ log/JSON 40-80% ก่อนอ้าง; ร่างรอบเดียว→รีวิวรอบเดียว เกิน 3 รอบหยุดถามคน; ตอบมีหลักฐาน `path:line`/exit code

## จำข้ามแชท (save/resume)
- ปิดงาน ("เซฟ"): 4 เอกสาร + `LATEST_CHECKPOINT.md` ≤30 บรรทัด + `state/` + Git remote
- เปิดงาน ("เปิดงาน/ลุยต่อ"): อ่าน checkpoint+behavior+mistakes ก่อนทัก ตอบแบบ Memory Briefing

## QC + ส่งมอบ
- ลูป `/constitution→/clarify→/checklist→/analyze→/converge` + Auto Gap-Closing (ขาด test/validation/loading/error → เติมเองก่อนส่ง)
- Self-Review 6 ข้อ: Scope/Syntax/Tests/No Regression/Security/Clean
- ผิด→ลง mistakes.md + ตั้งกฎห้ามซ้ำ; สื่อสารไทยกระชับ; เสนอ 2-3 ทางเลือกพร้อมคำแนะนำครั้งเดียว
