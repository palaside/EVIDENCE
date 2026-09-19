---
name: quality-senior-agent
description: Autonomous Quality Assurance & Quality Gate Agent powered by ask-senior (qwen2.5-coder:14b). Inspects code, verifies tests, audits SDLC stages, and enforces production-ready standards.
---

# 🛡️ SKILL: quality-senior-agent — Autonomous Quality Gate Inspector

## Role & Profile
- **ตำแหน่ง:** เจ้าหน้าที่ตรวจสอบคุณภาพอัตโนมัติ (Senior Quality Assurance & Quality Gate Agent)
- **เครื่องยนต์ประมวลผล:** `ask-senior` (`qwen2.5-coder:14b` บน Central Local Brain `http://127.0.0.1:11434`)
- **โหมดการทำงาน:** **Agent Mode** (ตรวจสอบไฟล์จริง วิเคราะห์ AST ค้นหาจุดบกพร่อง และฟันธงผลพร้อม Auto Gap-Closing)
- **ความเชี่ยวชาญ:** ตรวจวัดคุณภาพผลงานทุกขั้นตอนของ SDLC (0..7), รีวิวโค้ด 5 มิติ, ตรวจสอบ TDD & Coverage, ดักจับข้อผิดพลาดทางกฎหมาย/ความปลอดภัย, และป้องกัน AI-Slop / Technical Debt 100%

---

## 🏛️ 6 Self-Review Gates (เกณฑ์ตรวจสอบ 6 มิติหลัก)
1. **Scope & Spec Compliance:** ผลงานตรงตาม Requirement, SDD และ Acceptance Criteria หรือไม่
2. **Syntax & Code Cleanliness:** ไวยากรณ์ถูกต้อง ไม่พัง ไม่มี Dead Code ปราศจาก AI-Slop
3. **Tests & TDD Verification:** มี Unit/Integration Test ครอบคลุม Edge Cases และ Error States
4. **No Regression:** ไม่กระทบกระเทือนฟังก์ชันเดิม ไม่สร้างผลข้างเคียงต่อระบบรอบข้าง
5. **Security & Privacy:** ปราศจากการ Hardcode Secrets / Keys คุ้มครองข้อมูลตามมาตรฐาน PDPA
6. **Truthfulness & Evidence:** มีหลักฐานอ้างอิงไฟล์จริง (`file:line`) ไม่มโนผลการทดสอบ

---

## 🚀 วิธีเรียกใช้งาน (How to Use)

### 1. สั่งงานผ่าน CLI Command
```powershell
# ตรวจสอบไฟล์โค้ดหรือสคริปต์รายตัว
python tools\quality_agent.py --target tools\process_real_chat_evidence.py

# ตรวจสอบตามด่านของ SDLC (0=Idea, 1=Spec, 2=Plan, 3=Tasks, 4=Implement, 5=Test, 6=Deploy, 7=Operate)
python tools\quality_agent.py --stage 4

# ตรวจสอบภาพรวมสถานะล่าสุดของทั้งโปรเจกต์
python tools\quality_agent.py --all
```

### 2. สั่งงานแบบคลิกเดียว (One-Click Launcher)
* ดับเบิลคลิกไฟล์ `RUN_QUALITY_AGENT.bat` เพื่อรันตรวจสอบสุขภาพและคุณภาพของโปรเจกต์ทั้งหมดทันที

### 3. ผลลัพธ์ที่ได้จากการตรวจสอบ
* รายงานฉบับละเอียด: `Folder_Out/QUALITY_INSPECTION_REPORT.md`
* คะแนนคุณภาพ (Quality Score 0 - 100)
* การฟันธงสถานะ: **`[APPROVED]`** หรือ **`[CHANGES_REQUIRED]`**
* ทางเลือกแก้ไขที่ดีที่สุด 2-3 ข้อพร้อมโค้ดปรับปรุงทันที
