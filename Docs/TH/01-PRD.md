# 01 · PRD — Product Requirements Document
# โครงการ DIGITAL_EVIDENCE (To-Be ต่อยอด)

> SSOT อ้างอิง: `README.md`, `PROJECT_STATUS.md`, `AGENTS.md`
> ภาษา: ไทย | ตำแหน่ง: `Docs/TH/01-PRD.md` (ไฟล์สร้างใหม่ ห้ามแก้ต้นฉบับ)
> สถานะ: To-Be สำหรับพัฒนาต่อ

## 1. วัตถุประสงค์และขอบเขต (Objective & Scope)

**วัตถุประสงค์:** ต่อยอดระบบประมวลพยานหลักฐานดิจิทัล (ภาพแชท + สลิปโอนเงิน) จากสถานะปัจจุบัน (เล่มแชท 2,387 หน้า A4 บริสุทธิ์, สลิป 94 รายการ 467,218.00 บาท, OCR 13 คอลัมน์ 18 ธนาคาร) ไปสู่ระบบที่มี Dashboard สรุปข้ามสำนวน (Cross-Case Dashboard — Roadmap Phase 7 ที่ยังค้างใน `PROJECT_STATUS.md:115`) โดยคงกฎ Zero-Guessing/Zero-Hallucination

**In-Scope:**
- Hot Folder 24 ชม. (`EVIDENCE_IN` → `Folder_Out`), Drag & Drop (`RUN_SLIP_EXTRACTOR.bat`), Portable Suite (`Portable/INBOX_SLIPS`, `INBOX_CHATS`, `OUTPUT`)
- Chat Pipeline: Streaming Canvas + Quiet Zone Lookahead 1.30x + Feather 12px + Post-Slice Dedup Rule 14
- Slip Pipeline: 3-Tier (EMVCo QR Tier1 + Local CV/OCR Tier2 + Vision Fallback Tier3), Search_Slip 10 คอลัมน์, OCR_Slip 13 คอลัมน์, Duplicate Auditor
- Hash Manifest SHA-256 + Evidence Certificate (พ.ร.บ.ธุรกรรมทางอิเล็กทรอนิกส์ฯ)
- Dashboard อ่านอย่างเดียว (Read-only) สรุปยอด/จำนวนสลิป/สถานะสำนวนข้ามเคส

**Out-of-Scope:**
- ไม่รื้อ Stack เป็น Web Framework ใหญ่ (ห้าม Spec Drift — คง Python + PyMuPDF + Tesseract)
- ไม่ส่งข้อมูลคดีจริงขึ้น Git/Remote (PDPA Shield ผ่าน `.gitignore`)
- ไม่ทำระบบ Login หลายชั้นในเฟสนี้ (คง Local single-user)
- ไม่แก้ไขไฟล์ต้นฉบับ (`README.md`, `AGENTS.md`, `PROJECT_STATUS.md`, `tools/`, `_skills/`, `_engines/`)

## 2. กลุ่มผู้ใช้งานและบทบาท (User Roles)

| Role | คำอธิบาย | สิทธิ์ |
|---|---|---|
| พงส./ฝ่ายสืบสวน | เจ้าของสำนวน ตรวจเล่ม PDF/Excel | อ่าน + สั่งประมวลผล + พิมพ์ |
| เจ้าหน้าที่ธุรการคดี | หยอดไฟล์ จัดโฟลเดอร์เคส | หยอด INBOX + อ่าน OUTPUT |
| ผู้ตรวจสอบ/หัวหน้าชุด | ตรวจความครบ + เซ็นรับรอง | อ่าน + ตรวจ Hash + อนุมัติ |
| Admin ระบบ | ติดตั้ง Startup, กู้สถานะ | ติดตั้ง/ถอน + รัน `open_project_state.py` |
| Watcher (ระบบอัตโนมัติ) | `slip_hotfolder_watcher.py` เฝ้า 24 ชม. | เขียน OUTPUT อัตโนมัติ |

## 3. รายการฟีเจอร์ทั้งหมด (Feature List)

| ID | ฟีเจอร์ | อ้างอิงปัจจุบัน | To-Be |
|---|---|---|---|
| F-01 | List_names Prefix Grouping (V1- (1).jpg → V1) + Natural Sort | มีแล้ว | คงเดิม |
| F-02 | Dicut_Chat Stitch + Slip-Block-Fit + Smart Zoom 900px Pure White #FFFFFF | มีแล้ว | คงเดิม + Memo-Safe 180px |
| F-03 | Search_Slip สแกนหน้าสลิป + สารบัญ 10 คอลัมน์ (Excel/JSON) | มีแล้ว | เพิ่ม Hyperlink กระโดด PDF |
| F-04 | OCR_Slip 13 คอลัมน์ + BOT Code 3 หลัก + Branch→Memo | มีแล้ว | คงเดิม |
| F-05 | Duplicate Auditor (In-batch + Printed Log) ไฮไลต์ส้ม FFF2CC/แดง C00000 | มีแล้ว | เพิ่มรายงานรวม |
| F-06 | Cover + Index 6 หน้าแยกเล่ม + Hash Cert | มีแล้ว | คงเดิม |
| F-07 | Portable Standalone + Silent Run + Startup | มีแล้ว | คงเดิม |
| F-08 | Cross-Case Dashboard (ยอดรวม/จำนวน/สถานะ/ค้นหา Ref) | ยังไม่มี (Phase 7) | **สร้างใหม่ Read-only** |
| F-09 | Target Matcher + Consistency Engine (Only/Consistent) | มีแล้ว | ผูกเข้า Dashboard |
| F-10 | Immortal Protocol (`LATEST_CHECKPOINT.md` + save/open state) | มีแล้ว | คงเดิม |

## 4. ปัญหาที่ระบบต้องแก้ไข (Problems)

1. สลิปซ้ำ/วนใช้ใบเดิมเบิกซ้ำ → แก้ด้วย RefID + Fingerprint SHA-256 (16 หลัก) + Printed Log
2. ภาพแชทยาวถูกตัดผ่ากลางข้อความ/มีรอยต่อแบทช์ → แก้ด้วย Streaming Canvas + Quiet Zone + Dedup
3. ชื่อคนปนเลขบัญชี/OCR เดือนไทยเพี้ยน (Gn./&.A.) → แก้ด้วย Pixel-Level OCR + Month Normalization + คลีนบัญชีออกจากชื่อ
4. เลขหน้า PDF ไม่ตรงเลขพิมพ์ → แก้ด้วย Decoupled Cover/Index (แชทเริ่ม Physical Page 1)
5. ไม่มีภาพรวมข้ามสำนวน → แก้ด้วย Dashboard F-08 (สาเหตุหลักของเอกสารชุดนี้)

## 5. เงื่อนไขความสำเร็จ (Success Criteria)

- [ ] Pre-Delivery Gate 10 มิติ ALL GREEN (`AGENTS.md:20`): แยกเล่ม 1:1, เลขหน้าตรง, สลิปครบ, ยอดว่าง=0, วันที่ว่าง=0, ไม่ระบุชื่อ=0, คลีนบัญชี, ตาราง Sarabun Center Contrast สูง, JSON==Excel==PDF, ไร้ไฟล์ขยะ
- [ ] Zero Duplicate Pages (SHA-256/Xref = 0)
- [ ] ดึงธนาคารผู้รับสำเร็จ 100%, OCR 40-slip stress test 100%
- [ ] 100 หน้าใน ≤1s (PyMuPDF C-Binding)
- [ ] Dashboard อ่านจาก OUTPUT จริง ไม่เดาข้อมูล

## ผลลัพธ์
รู้ว่าระบบต้องทำอะไร (F-01–F-10) และอะไรอยู่นอกขอบเขต (ไม่รื้อ Stack, ไม่แตะต้นฉบับ, ไม่ส่งคดีขึ้น Git)
