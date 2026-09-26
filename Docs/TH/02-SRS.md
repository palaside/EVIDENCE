# 02 · SRS — Software Requirements Specification
# โครงการ DIGITAL_EVIDENCE (To-Be)

> ตำแหน่ง: `Docs/TH/02-SRS.md` (สร้างใหม่) | ผูก PRD: `Docs/TH/01-PRD.md`
> กฎเหล็ก: Pixel-Level OCR, ห้ามเดา (AGENTS.md), Pre-Delivery Gate 10 มิติ

## 1. Functional Requirements

### FR-01 List_names (Grouping & Sort)
- ตรวจ Prefix จากชื่อ Windows Ctrl+A: `V1- (1).jpg` → เคส `V1`
- Natural Sort: 1,2,…,9,10,11 (ห้าม sort แบบ string)
- Input: `EVIDENCE_CHAT_IN/`, `EVIDENCE_IN/` | Output: กลุ่มเคสเรียงลำดับ

### FR-02 Dicut_Chat (Slice & Stitch)
- Streaming Canvas ต่อสายพานเดียวยาวแล้วสไลซ์ตาม Quiet Zone Lookahead 1.30x
- Feather Stitch 12px, Strip แถบดำ 13-row, Slip-Block-Fit Canvas (645x890 / 807x1115)
- Smart Zoom: สลิปแนวตั้งสูง 900px บน Pure White #FFFFFF, Micro-trim 2px, เว้น Memo 180px ใต้ "วันที่ทำรายการ"
- Post-Slice Dedup Rule 14: SHA-256 + RefID ซ้ำหน้าก่อนหน้า → ตัดทิ้ง

### FR-03 Search_Slip (Locator & Index)
- สแกน PDF สำเร็จแล้ว หา badge/slip-card ระบุเลขหน้า (เช่น 64,65,97)
- สกัด: ยอดเงิน, วันที่, ผู้โอน, ผู้รับ, Ref
- ส่งออกสารบัญ 10 คอลัมน์ (Excel Sarabun Center + JSON) คอลัมน์แรก `หน้าระบุสลิป` ไฮไลต์ทอง/อำพัน + Hyperlink กระโดด PDF
- ตารางท้ายเล่มแชท: 20 แถว/หน้า A4 Landscape, ตัดแบนเนอร์ชื่อตารางออก

### FR-04 OCR_Slip (Extraction 13 คอลัมน์)
- Preprocess: Morphological BG Subtraction + CLAHE + Multi-Pass `tha+eng`
- Tier1: ถอด BOT Code 3 หลักจาก EMVCo QR Tag00 Sub-tag01 (100% bit-accurate)
- Tier2: Local Forensic CV/OCR | Tier3: Vision Fallback (Typhoon) + SHA-256 Cache
- Master Dict 18 สถาบันการเงิน, ดึงสาขา (`สาขา...`) → Memo, Normalize เดือนไทยเพี้ยน → มาตรฐาน 12 เดือน, ถอด ISO timestamp จาก Ref
- PII Guard `--mask-pii`: บัตรปชช. 13 หลัก, มือถือ 10 หลัก, เครดิต 16 หลัก, บัญชี 10–12 หลัก (8 ธนาคาร)

### FR-05 Duplicate & Printed-Log Auditor
- In-batch: RefID ซ้ำ / ชื่อไฟล์ซ้ำ / Fingerprint SHA-256 (16 หลัก) ซ้ำ → `⚠️ สลิปซ้ำ (Ref ซ้ำกับลำดับ X)`
- Cross-batch: เทียบ `memory/printed_slips.log` → `⚠️ เคยพิมพ์แล้ว (Printed)`
- Highlight: พื้นส้มอ่อน FFF2CC + ตัวแดงเข้ม C00000

### FR-06 Assembly & Certification
- Cover (Executive Dossier กล่องข้อ 6) + Index 5 หน้า + Chat 2,387 หน้า Master (เลขต่อเนื่องข้ามเล่ม)
- Decoupled: Cover+Index แยกไฟล์ ไม่กลืนเลขหน้า (แชทเริ่ม Physical 1 = พิมพ์ 1)
- Header Ribbon: โลโก้ซ้าย + MODE (SLIP/CHAT เท่านั้น) + CORROBORATED + PAGE | Footer: รับรอง 3 บรรทัด Sarabun Thin กึ่งกลาง
- Hash: SHA-256 Manifest + Certificate PDF (พ.ร.บ.ธุรกรรมฯ 2544)

### FR-07 Automation & Portable
- Watcher 24 ชม. `tools/slip_hotfolder_watcher.py`: หยอด → OCR/QR → Excel Sarabun Center → `Folder_Out` + เปิด Explorer
- Portable: `INBOX_SLIPS/INBOX_CHATS/OUTPUT`, `.bat` Pure ASCII → `launcher.py` UTF-8, Drag&Drop, เมนูไทย [1][2][3][9]
- Startup: `install_startup.bat`/`uninstall_startup.bat` + `run-silent.vbs` + `tick.py`
- Immortal: `open_project_state.py` อ่าน `LATEST_CHECKPOINT.md` ใน 0.1s

### FR-08 Dashboard (To-Be ใหม่)
- Read-only อ่านจาก `Folder_Out/*.xlsx|*.json` เท่านั้น ห้ามเขียนกลับ
- สรุป: ยอดรวม/จำนวนสลิป/จำนวนเคส/สถานะ Gate/รายการซ้ำ
- ค้นหา: RefID, ชื่อ, ช่วงวันที่, ธนาคาร | คลิก → เปิด PDF หน้านั้น

## 2. Non-functional Requirements

| หมวด | เกณฑ์ |
|---|---|
| Performance | สร้าง/รวม PDF 100 หน้า ≤1s (PyMuPDF), OCR 6-core 560 ใบ ≤5 นาที |
| Accuracy | Stress 40 ใบ 100%, ธนาคารผู้รับ 100%, 0 หน้าซ้ำ |
| Integrity | Zero-Guessing, Pixel-Level ทุกตัวอักษร/สระ/วรรณยุกต์/เลขบัญชี |
| Usability | ดับเบิลคลิกใช้ได้ ไม่ต้องพิมพ์คำสั่ง, เมนูไทย, ฟอนต์ Sarabun |
| Typography | Center ทุกเซลล์ (H+V), Border thin 4 ด้าน, กว้าง 9.5–32pt, A4 Landscape, Disclaimer 3 บรรทัดกึ่งกลาง |
| Reliability | Auto-Audit 100% ทุกหน้า, Fallback ห้ามเดา |
| Security | PDPA mask, `.gitignore` กันคดีหลุด, อ่าน `.env` เฉพาะชื่อ Key |
| Portability | ยก `Portable/` ไปรันที่อื่นได้, ลง Windows ใหม่รัน `install_startup.bat` ครั้งเดียว |

## 3. Business Rules & Validation

- BR-01: ยอดว่าง = 0, วันที่ว่าง = 0, ชื่อไม่ระบุ = 0 (นับเป็น Fail ถ้าเกิน)
- BR-02: ห้ามเลขบัญชีในช่องชื่อบุคคล (ต้องคลีน 100%)
- BR-03: MODE มีแค่ SLIP/CHAT (ห้าม SUMMARY)
- BR-04: ภาพปกติ CORROBORATED=`บทสนทนาต่อเนื่อง`, ภาพมีสลิป=`สลิปหลักฐานหน้าที่ [X] / สารบัญการเงินลำดับที่ [Y]`
- BR-05: JSON==Excel==PDF 100% (จำนวน/ยอด/Ref ตรงกัน)
- BR-06: ฟอนต์ตัวเลข/ข้อความกึ่งกลางทุกช่อง, ขยายช่องกันตัดคำ, Auto scale 12→10/9pt กันล้น

## 4. สิทธิ์การเข้าถึง (Access Matrix)

| ฟังก์ชัน | ธุรการ | สืบสวน | ตรวจสอบ | Admin | Watcher |
|---|---|---|---|---|---|
| หยอด INBOX | ✓ | ✓ | – | ✓ | – |
| สั่งประมวลผล | – | ✓ | – | ✓ | auto |
| อ่าน OUTPUT/Dashboard | ✓ | ✓ | ✓ | ✓ | เขียน |
| ตรวจ Hash/อนุมัติ | – | – | ✓ | ✓ | – |
| ติดตั้ง Startup/กู้ state | – | – | – | ✓ | – |

## 5. เงื่อนไขเมื่อข้อมูลผิดพลาด

| เคส | พฤติกรรม |
|---|---|
| ภาพเบลอ/ความละเอียดต่ำ | ยกระดับ Typhoon Vision ระดับพิกเซล, ห้ามเดา, 标记 `ต้องตรวจซ้ำ` |
| QR อ่านไม่ได้ | ตกไป Tier2/Tier3 + Cache, ระบุ `QR_N/A` ห้ามมโนธนาคาร |
| สลิปซ้ำ | คงแถวไว้ + Warning + สี, ไม่ลบ, นับในรายงานซ้ำ |
| ไม่ใช่สลิป (ภาพอาหาร/ถ่ายทั่วไป) | คัดออก Pure Financial Gate เหลือเฉพาะสลิปจริง |
| PDF เสีย/xref ชน | หยุด pipeline + log + คง checkpoint ไม่เขียนทับของดี |
| Port/Process ค้าง, Path `\` vs `/` | แจ้งเตือนก่อนสตาร์ต, ไม่รันซ้ำเกิน 2 ครั้งโดยไม่เปลี่ยนตรรกะ |

## 6. Acceptance Criteria

- ผ่าน Pre-Delivery Gate 10 มิติ ALL GREEN (`py tools/pre_delivery_quality_gate.py`)
- `py tools/run-tests.py` เขียว 18 ข้อ (ถ้ามี)
- ตรวจ 4-Tier: Tier1 Static [PASS] + Tier2 Unit (40-slip) [PASS] + Tier3 Integration [PASS/ยังไม่ได้ทดสอบ] + Tier4 E2E [PASS/ยังไม่ได้ทดสอบ] — ห้ามเหมารวม
- Self-Review 6 ข้อ (Scope/Syntax/Verification/Env/Security/Clean) ครบ

## ผลลัพธ์
รู้ว่าแต่ละฟังก์ชันต้องทำอย่างไร ตรวจด้วยอะไร และเมื่อพังต้องทำอย่างไร
