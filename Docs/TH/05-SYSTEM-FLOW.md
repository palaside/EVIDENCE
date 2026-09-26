# 05 · SYSTEM-FLOW — System Workflow & User Flow
# โครงการ DIGITAL_EVIDENCE (To-Be)

> ตำแหน่ง: `Docs/TH/05-SYSTEM-FLOW.md` (สร้างใหม่) | ผูก `01-PRD` + `02-SRS` + `04-DATA-MODEL`

## 1. User Journey & User Flow

**ธุรการ:** หยอดไฟล์ `EVIDENCE_IN`/`INBOX_*` → รอ OUTPUT เด้ง → ส่งต่อสืบสวน
**สืบสวน:** สั่ง `RUN_*` หรือลากวาง → ตรวจ Excel/JSON/PDF → ค้น Ref/หน้า → พิมพ์สำนวน
**ตรวจสอบ:** เปิด Hash Cert + Manifest → เทียบ SHA-256 → อนุมัติ
**Admin:** ติดตั้ง Startup ครั้งเดียว → กู้ state ด้วยเมนู [9] เมื่อค้าง

## 2. Workflow หลัก 2 เส้น

### Flow A — Slip (เดี่ยว/เป็นกอง)
```text
[หยอดรูป/โฟลเดอร์] → Watcher จับไฟล์ใหม่ → Preprocess (Morph+CLAHE)
→ Tier1 QR(BOT 3หลัก) → ไม่ออก? Tier2 OCR → ยังต่ำ? Tier3 Vision
→ Normalize (เดือนไทย/ISO/Branch→Memo/PII mask)
→ Dedup (Ref/FP vs batch + printed.log) → ไฮไลต์ส้ม/แดงถ้าซ้ำ
→ Export 13-col Excel Sarabun Center + JSON → Folder_Out/OUTPUT + เปิด Explorer
→ Gate 10 มิติ → certified
```

### Flow B — Chat (3 ชุด → Master)
```text
[หยอดแชท 3 โฟลเดอร์] → List_names group+sort → Streaming Canvas ต่อยาว
→ Slice QuietZone 1.30x (Pack-to-Bottom) → Dedup Rule14 → 2,387 หน้า
→ Block-Fit + Zoom 900px #FFFFFF → Gen PDF (PyMuPDF)
→ Hook Search_Slip → 10-col index + Hyperlink + สรุปท้ายเล่ม 20แถว/หน้า
→ Assembly Cover+Index 6p แยกเล่ม → Hash Cert → Gate → certified
```

### Flow C — Dashboard (To-Be อ่านอย่างเดียว)
```text
[เปิด Dashboard] → อ่าน Folder_Out/*.json → สรุปยอด/จำนวน/สถานะ/ซ้ำ
→ ค้นหา (Ref/ชื่อ/วันที่/ธนาคาร) → คลิก → เปิด PDF หน้านั้น
```

## 3. Data Flow (Frontend → API/CLI → DB/File)

| ขั้น | IN | PROC | OUT |
|---|---|---|---|
| รับงาน | JPG/PNG/PDF ใน INBOX | watcher/launcher | queue + `cases` |
| ประมวลผล | queue | `_skills/_engines` | `evidence_pages/slips/index` (ไฟล์) |
| ส่งออก | rows | openpyxl/PyMuPDF | XLSX+JSON+PDF (Sarabun Center) |
| รับรอง | artifacts | Gate + SHA-256 | Cert + Manifest + status=certified |
| สรุป | XLSX/JSON | Dashboard read | ตาราง/กราฟ/ค้นหา |

## 4. เงื่อนไขเปลี่ยนสถานะ

```text
queued → processing (จับไฟล์/กดรัน)
processing → audited (Auto-Audit 100% + Dedup)
audited → indexed (Search_Slip เสร็จ)
indexed → exported (Excel/JSON/PDF ครบ + Hyperlink)
exported → certified (Gate ALL GREEN + Hash ตรง)
ใดๆ → needs_review (เบลอ/QR_N/A/ซ้ำ/ไม่ใช่สลิป) → กลับ processing หลังแก้ที่ต้นตอ
```

## 5. เส้นทางเมื่อเกิดข้อผิดพลาด

| จุดพัง | ทำอย่างไร |
|---|---|
| ภาพเบลอ | ใช้ Vision พิกเซล, 标记 review, ห้ามเดา |
| QR อ่านไม่ออก | `QR_N/A` + Tier2/3, ไม่มโนธนาคาร |
| สลิปซ้ำ/เคยพิมพ์ | คงแถว + warn + สี FFF2CC/C00000 + ลง `audit_duplicates` |
| ไม่ใช่สลิป | Pure Gate คัดออก |
| PDF/xref เสีย | หยุด, คง checkpoint, ไม่ทับของดี, log ชัด |
| Port ค้าง/Path ผิด/OS encoding | แจ้งก่อนรัน, ลองใหม่ ≤2 ครั้งแบบเปลี่ยนตรรกะ |
| Gate ไม่ ALL GREEN | วนซ่อมที่ต้นตอ ห้ามส่งมอบ |

## 6. แยกตาม User Roles

- ธุรการเห็นแค่ INBOX/OUTPUT; สืบสวนเห็น ledger/index + ปุ่มรัน; ตรวจสอบเห็น Cert/Manifest + ปุ่มอนุมัติ; Admin เห็น log/state/startup; Watcher ทำงานเงียบไม่มี UI
- ทุก Role: คลิกเลขหน้า → เปิด PDF หน้านั้นทันที (Slip Index Navigation)

## ผลลัพธ์
รู้ว่ากดปุ่มหนึ่งครั้ง ระบบทำอะไรต่อจนจบ (A/B/C) พังตรงไหนไปไหนต่อ และ Rollback ที่ `LATEST_CHECKPOINT.md` + `state/`
