# 04 · DATA-MODEL — Database Schema & Data Model
# โครงการ DIGITAL_EVIDENCE (To-Be สำหรับ Dashboard)

> ตำแหน่ง: `Docs/TH/04-DATA-MODEL.md` (สร้างใหม่)
> ปัจจุบันเป็น File-DB (`Folder_Out/*.xlsx|*.json` + `memory/printed_slips.log`); เอกสารนี้ map เป็น tables เพื่อทำ Dashboard โดยไม่แก้ pipeline เดิม

## 1. Entity & Tables (6 ตาราง)

| Table | คำอธิบาย | Source ปัจจุบัน |
|---|---|---|
| `cases` | สำนวน/เคส (V1, จิณห์นิภา...) | Prefix จาก List_names |
| `evidence_pages` | หน้ากระดาษ A4 ทุกหน้า (2,387 หน้า) | PDF Chat + xref/hash |
| `slips` | สลิปการเงิน 13 คอลัมน์ (94 รายการ) | OCR_Slip ledger |
| `slip_page_index` | สารบัญ 10 คอลัมน์ ผูกหน้า↔สลิป | Search_Slip index |
| `printed_log` | ประวัติเคยพิมพ์/ประมวลผล | `memory/printed_slips.log` |
| `audit_duplicates` | รายการซ้ำ + คำเตือนสี | Auditor output |

## 2. Columns & Types

**cases:** `case_id TEXT PK` (เช่น V1), `case_name TEXT`, `owner TEXT`, `created_at TEXT ISO`, `status TEXT` (queued/processing/audited/indexed/exported/certified)

**evidence_pages:** `page_id INTEGER PK`, `case_id FK→cases`, `page_no INTEGER`, `physical_xref TEXT`, `sha256 TEXT UNIQUE`, `mode TEXT CHECK(SLIP,CHAT)`, `corroborated TEXT`, `pdf_path TEXT`

**slips (13 คอลัมน์ + เสริม):** `slip_id INTEGER PK`, `case_id FK`, `page_no INTEGER`, `amount REAL`, `txn_date TEXT`, `sender TEXT`, `receiver TEXT`, `sender_bank_code TEXT(3)`, `receiver_bank TEXT`, `ref_id TEXT`, `branch_memo TEXT`, `qr_bot_code TEXT(3)`, `fingerprint TEXT(16)`, `image_path TEXT`, `warn TEXT`

**slip_page_index (10 คอลัมน์):** `idx INTEGER PK`, `slip_page_no INTEGER` (หน้าระบุสลิป, ทอง/อำพัน), `case_id FK`, `slip_id FK`, `amount REAL`, `txn_date TEXT`, `counterparty TEXT`, `ref_id TEXT`, `pdf_link TEXT`, `note TEXT`

**printed_log:** `log_id INTEGER PK`, `ref_id TEXT`, `fingerprint TEXT(16)`, `printed_at TEXT`, `batch TEXT`

**audit_duplicates:** `audit_id INTEGER PK`, `slip_id FK`, `dup_with TEXT`, `kind TEXT` (in_batch/cross_batch/printed), `message TEXT`, `color TEXT` (FFF2CC/C00000)

## 3. PK / FK

- PK: ทุกตารางมี PK เดี่ยว; `evidence_pages.sha256 UNIQUE`, `slips.(ref_id+fingerprint)` UNIQUE แบบมีเงื่อนไข (อนุญาตซ้ำแต่ต้องมี warn)
- FK: `evidence_pages.case_id→cases`, `slips.case_id→cases`, `slip_page_index.case_id→cases + slip_id→slips`, `audit_duplicates.slip_id→slips` (ON DELETE RESTRICT ห้ามลบหนี audit)

## 4. ERD (Text)

```text
cases 1───* evidence_pages
cases 1───* slips 1───* audit_duplicates
cases 1───* slip_page_index *───1 slips
slips *───* printed_log (via ref_id/fingerprint, ไม่ใช่ FK แข็ง)
```

## 5. Constraints & Indexes

- `CHECK(mode IN ('SLIP','CHAT'))`, `CHECK(amount>=0)`, ยอดว่าง→0 วันที่ว่าง→`''` (นับ Fail ที่ Gate ไม่ใช่ DB)
- ห้ามเลขบัญชี 10–12 หลักใน `sender/receiver` (validate ด้วย regex 8 ธนาคารก่อน insert)
- Indexes: `idx_slips_ref(ref_id)`, `idx_slips_fp(fingerprint)`, `idx_pages_case_page(case_id,page_no)`, `idx_index_case(case_id)`, `idx_printed_ref(ref_id)`
- JSON==Excel==PDF: จำนวนแถว/ยอดรวม/Ref ต้องตรงกันก่อนขึ้น Dashboard (Gate ข้อ 9)

## 6. การควบคุมสิทธิ์เข้าถึงข้อมูล

- ธุรการ/สืบสวน/ตรวจสอบ: SELECT อย่างเดียวผ่าน Dashboard
- Watcher/Pipeline: INSERT/UPDATE `slips/index/pages/printed_log`
- Admin: อนุมัติ certified + กู้ checkpoint; ห้าม DELETE `audit_duplicates` (เก็บเป็นหลักฐาน)
- PII: Dashboard แสดงแบบ mask ตาม `--mask-pii` (บัตร/มือถือ/บัญชีบางส่วน `***`)

## ผลลัพธ์
รู้ว่าข้อมูลมาจากไหน (OUTPUT+memory) เก็บอย่างไร (6 ตาราง) Dashboard ใช้คอลัมน์ใดได้บ้าง (ยอด/วันที่/คู่กรณี/Ref/หน้าสลิป/สถานะซ้ำ)
