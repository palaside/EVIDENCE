# 🏛️ LATEST PROJECT CHECKPOINT — DIGITAL EVIDENCE
**Updated:** 2026-09-18 20:10:00 | **Protocol:** Immortal Agent Protocol (Resurrection Ready)

---

## 📍 1. Current Project State & Milestones (สถานะงานปัจจุบัน)

- [x] **CHAT MODE (สมบูรณ์ 100% - Streaming Canvas Overhaul 2,387 Pages + Decoupled Dossier):**
  - **อัปเกรดระบบ Streaming Canvas Pipeline:** เปลี่ยนสถาปัตยกรรมต่อสายพานภาพแชทยาวต่อเนื่องและหั่นตาม Quiet Zone แทนการแบ่งแบทช์เดิม ขจัดรอยต่อแบทช์ รอยตัดผ่าข้อความ และลดจำนวนหน้าจาก 2,560 หน้า เหลือ **2,387 หน้า A4 บริสุทธิ์ (ลดลง 173 หน้า)**
  - **ติดตั้งกฎตรวจจับภาพซ้ำหลังหั่น (Post-Slice Deduplication Rule):** สแกนตรวจสอบ SHA-256 Content Hash และ Slip Reference ID ของหน้าที่หั่นออกมาทันที หากซ้ำ 100% กับหน้าก่อนหน้าให้ตัดทิ้งอัตโนมัติ การันตี Zero Duplicate Pages 100%
  - **เล่มแชทหลักฐาน (Master Chat PDF):** `Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3.pdf` (**2,387 หน้า**) รันเลขหน้า 1 ถึง 2,387 ตรงกับ Physical Page 1:1
  - **ชุดหน้าปกและสารบัญแยกเดี่ยว (Decoupled Dossier):** `Folder_Out/Evidence_Chat_Master_Front_Cover_and_Index.pdf` (**6 หน้า** = ปก Executive 1 หน้า + สารบัญ 10 คอลัมน์ Landscape 5 หน้า) หน้าระบุสลิปตรงกับเลขหน้าพิมพ์จริง 100%
  - **ดัชนีสลิปและมูลค่าคดี:** สแกนพบสลิปธุรกรรมจริง **94 รายการ** มูลค่ารวม **467,218.00 บาท** พร้อมส่งออก `Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx` และ `.json`
  - **มาตรฐานความถูกต้องระดับพิกเซล (Option 1 Verified Binding):** ผูกโยงชื่อคู่ความและธนาคารที่ผ่านการตรวจพิสูจน์แล้ว (สิบตรี ณัฐชัย รักษาวงษ์ / น.ส. จิณห์นิภา ประสาทเขตการ) 100% ปราศจากเลขบัญชีหลุดในช่องชื่อ

- [x] **SLIP MODE SYSTEM 1 — MASTER UNIQUE 560 SLIPS (สมบูรณ์ 100% - Priority 1):**
  - สกัดสลิปจริงที่ไม่ซ้ำกัน 560 ใบ จากคลัง 2,792 ไฟล์ (`F:\Project\EDOK\Duplicates\Done`)
  - อัปเกรด **Stage Forensic Smart Zoom & Crop v2.0**: ครอป 4 ทิศทางตัดพื้นโต๊ะ/ขอบภาพทิ้ง 100% พร้อมให้พื้นที่หายใจใต้บรรทัด "วันที่ทำรายการ" ~180px การันตีข้อความบันทึกช่วยจำ (Memo) ปลอดภัยครบถ้วน ไม่ถูกตัดขาด
  - สกัดข้อมูล 10 คอลัมน์สำเร็จ 555 ใบ (99.1%) **ยอดเงินหมุนเวียนรวม: 1,547,803.68 บาท** (187 วันที่)
  - รวมเล่ม PDF สมบูรณ์: `Folder_Out/Evidence_Slips_Master_Unique_560.pdf` (**588 หน้า** = 560 หน้าสลิปเดี่ยว + 28 หน้าตารางสรุป 10 คอลัมน์ Landscape)
  - รายงานแจกแจงไฟล์ซ้ำ: `Folder_Out/DUPLICATE_SLIP_AUDIT_REPORT.xlsx` (Sheet 1: สลิป Master 560 ใบ, Sheet 2: รายการซ้ำ 2,232 ไฟล์ ผูกโยงชัดเจน)
  - ตารางสรุป 10 คอลัมน์: `Folder_Out/Evidence_Slips_Master_Unique_560.xlsx`

- [x] **SLIP MODE SYSTEM 2 & 3 — REFERENCE RESERVES (จัดเก็บเข้าคลังสำรอง):**
  - System 2 (Stem Dedup): `Folder_Out/Reference_Archives/Evidence_Slips_Reference_Stems_1160.pdf` (1,160 สลิป)
  - System 3 (Full Raw Mode): `Folder_Out/Reference_Archives/Evidence_Slips_Reference_Raw_2792.pdf` (2,792 สลิป)

- [x] **SKILL NAME & TARGET PERSON MATCHER (สมบูรณ์ 100%):**
  - สกิล `_skills/Name` (`target-name-matcher`): คัดกรองเฉพาะบุคคลเป้าหมาย (Person of Interest)
  - ยึดหลัก "ชื่อตรง นามสกุลตรง นั้นคือถูก" กรองคำนำหน้าชื่อทิ้ง 100% (`นาย`, `นาง`, `น.ส.`, `ด.ช.`, `ด.ญ.`, `คุณ`, `พล.ต.`, ฯลฯ)
  - สกัดยอดเงินเข้า-ออก บัญชีคู่กรณี พร้อมจำแนกคีย์เวิร์ดคดีกู้ยืมเงิน
  - สร้างสำนวนเฉพาะบุคคล: `Evidence_Target_จิณห์นิภา_ประสาทเขตการ.xlsx` และ `Evidence_Target_จิณห์นิภา_ประสาทเขตการ.pdf` (558 หน้า)

- [x] **WINRAR SFX LOCKED ARCHIVE PROTOCOL (สมบูรณ์ 100%):**
  - ติดตั้งเอนจินบีบอัดและสร้างไฟล์คลายตัวเองอัตโนมัติ: `tools/build_sfx_evidence_package.py`
  - หน้าต่างกรอกข้อมูลความปลอดภัยรอบเดียว (Initial Input Window): กรอกชื่อและรหัสผ่านครั้งเดียว ระบบหลังบ้าน Auto-Sync Confirm Password อัตโนมัติ 100%
  - ตั้งค่ามาตรฐาน WinRAR: Archive Format เป็น RAR เท่านั้น, SFX Mode (`-sfx`), เข้ารหัสทั้งข้อมูลและชื่อไฟล์ระดับสูง (`-hp<password>`)
  - หน้าต่างคำประกาศและสุนทรียภาพ: Title `DIGITAL EVIDENCE`, บรรจุข้อความคำประกาศปฏิเสธความรับผิดชอบ 3 บรรทัดตาม `Pattle.pdf` ไม่ตัดทอนคำ, ตราโล่สีกรมท่า-ฟ้า 150x250 BMP รักษาสัดส่วนสมมาตร, ไอคอนทางการ `app_icon.ico`
  - รองรับภาษาไทยสมบูรณ์ผ่านสวิตช์ `-scuc` (Unicode UTF-8 Mode)
  - ตัวสั่งงานคลิกเดียว: `CREATE_SFX_EVIDENCE.bat` (Zero-Command Launcher)
  - ผลลัพธ์ทดสอบสำเร็จ: `Folder_Out/Pattle_Case_Evidence_Test.exe` (3,882.91 MB) พร้อมไฟล์กำกับ `SHA-256`

- [x] **AUTONOMOUS QUALITY AGENT — POWERED BY ASK-SENIOR (สมบูรณ์ 100%):**
  - สร้างเอเจนต์ตรวจวัดคุณภาพผลงานทุกขั้นตอน: `tools/quality_agent.py` (ซิงค์สู่ `F:/Project/tools/quality_agent.py`)
  - ขับเคลื่อนด้วยโมเดล `qwen2.5-coder:14b` ของสกิล `ask-senior` บน Central Local Brain (`http://127.0.0.1:11434`)
  - รันในโหมด **Agent Mode** ตรวจสอบไฟล์จริง (Inspect Before Act), วิเคราะห์ AST, เช็ค Syntax, ตรวจทาน Tests
  - เกณฑ์ประเมิน 6 มิติ (Scope, Syntax, Tests & TDD, No Regression, Security & PDPA, Cleanliness & Anti-Slop)
  - ระบบ Auto Gap-Closing: เสนอทางเลือกแก้ไข 2-3 ข้อที่ดีที่สุด พร้อมโค้ด Unit Test ที่สร้างขึ้นจริงทันที
  - คำตัดสินแบบ Gatekeeping: ออกคะแนน Quality Score (0-100) และฟันธง `[APPROVED]` หรือ `[CHANGES_REQUIRED]`
  - สร้างสกิลกำกับ: `quality-senior-agent/SKILL.md` (ซิงค์สู่ `F:/.agents/skills/quality-senior-agent/SKILL.md`) และอัปเดต `ask-senior/SKILL.md`
  - ตัวสั่งงานคลิกเดียว: `RUN_QUALITY_AGENT.bat` และรายงานผลอัตโนมัติ `Folder_Out/QUALITY_INSPECTION_REPORT.md`

- [x] **SKILL ONLY — CORRELATED EVIDENCE (สมบูรณ์ 100%):**
  - ติดตั้งสกิล `_skills/Only/SKILL.md` และ `C:\Users\EVE\.gemini\config\skills\only-corroborated\SKILL.md`
  - สกัดเฉพาะคู่ [หน้าแชทสั่งโอน ⟷ สลิปจริง] สร้างเล่มสำนวนคดีฉบับคัดเฉพาะพยานเอกสารสำคัญแห่งคดี (Executive Court Edition)

- [x] **3-TIER HYBRID SLIP EXTRACTION & GEMINI EMERGENCY FALLBACK (สมบูรณ์ 100%):**
  - ติดตั้งสถาปัตยกรรมไฮบริด 3 ระดับ: Tier 1 EMVCo QR Code Decoder (Mini-QR/BScanC 100% Bit-accurate) + Tier 2 Morphological CV & Tesseract OCR + Tier 3 Gemini Multimodal Emergency Fallback
  - โมดูลกู้ภัย: `_skills/OCR_Slip/scripts/gemini_slip_fallback.py` (ซิงค์ `_engines/OCR_Slip/scripts/`)
  - ทริกเกอร์อย่างแม่นยำ: เรียก Gemini เฉพาะสลิปที่ QR Code พังและ Local OCR สกัดยอดเงินหรือวันที่ไม่สำเร็จ (ประหยัด Token 98-99%)
  - Persistent SHA-256 Cache: `Folder_Out/gemini_fallback_cache.json` รับประกันไม่ยิง API ซ้ำภาพเดิม
  - แม่แบบคอนฟิก: `.env.example` ปลอดภัยตามเกณฑ์ PDPA Shield และความปลอดภัย Secrets
  - ชุดทดสอบ Unit & Integration Test: `tools/test_gemini_fallback.py` ผลลัพธ์ PASS 100% (7/7 Tests)

- [x] **OPENTYPHOON THAI SOVEREIGN VISION ENGINE & AUDIT TOOL (สมบูรณ์ 100%):**
  - ระบบคู่หู 2 จังหวะ: Stage 1 `typhoon-ocr-v1.5` (Native Thai Multimodal Vision) สกัดตัวอักษร สระ วรรณยุกต์ และบันทึกช่วยจำ + Stage 2 `typhoon-v2.5-30b-a3b-instruct` (Forensic Legal Evidence Auditor) จัดสคีมา 10 คอลัมน์มาตรฐาน
  - เอนจินหลัก: `_skills/OCR_Slip/scripts/typhoon_slip_engine.py` (ซิงค์ `_engines/`)
  - เครื่องมือ Audit สแกนตรวจแก้สลิปเฉพาะจุด: `tools/typhoon_audit_slip.py` รองรับทั้งไฟล์ภาพและเลขหน้า PDF
  - ผลการรันทดสอบกับสลิปจริง: สกัด `35,000.00 บาท`, วันที่ `30/05/2568`, คู่สัญญาถูกต้อง และอ่านบันทึกช่วยจำ `"ค่าทอง"` สำเร็จ 100%
  - Persistent SHA-256 Cache: `Folder_Out/typhoon_cache.json` โหลดซ้ำใน 0.05 วินาที Zero-Token Wasted
  - บันทึกรายงานการตรวจสอบ: `Folder_Out/TYPHOON_AUDIT_REPORT.json`

- [x] **SKILL CLONED: Typhoon_OCR (สมบูรณ์ 100%):**
  - โคลนสร้างเป็นสกิลอิสระ `Typhoon_OCR` ทั้งในโฟลเดอร์โปรเจกต์ `_skills/Typhoon_OCR/` (และ Mirror `_engines/Typhoon_OCR/`)
  - ติดตั้งเข้าสู่ Global Customization Root: `C:\Users\EVE\.gemini\config\skills\Typhoon_OCR\SKILL.md`
  - สคริปต์สั่งการ: `_skills/Typhoon_OCR/scripts/typhoon_ocr.py` (รองรับไฟล์ภาพ, PDF แยกหน้า, `--raw`, `--out`, และ Zero-Token Cache)
  - ทดสอบรัน CLI: ผลลัพธ์สมบูรณ์ 100% ตอบสนองทันทีจากหน่วยความจำ 0.04 วินาที

- [x] **SKILL DECOUPLED: Summary_Table & Standalone Dossier Standard (สมบูรณ์ 100%):**
  - แยกโมดูลตารางสรุป 10 คอลัมน์ (A4 Landscape) และหน้าปก ออกจาก `process_chat.py` อย่างเด็ดขาด 100% เป็นโมดูลอิสระ `_skills/Summary_Table` (สคริปต์ `summary_table.py`)
  - แก้ไขปัญหา "หน้าเลื่อน / ต้องมานั่งนับเอง": เล่มเนื้อหาหลักฐานแชท `Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3.pdf` (2,560 หน้า) เริ่มต้นที่หน้า 1 เพียวๆ (Page 1 = Physical Page 1) สั่งพิมพ์ตรงหน้าเป๊ะ 100% ปราศจากหน้าสารบัญมาแทรกเลื่อนเลขหน้า
  - เล่มหน้าปกและสารบัญสรุปการเงินสร้างแยกเดี่ยว: `Folder_Out/Evidence_Chat_Master_Front_Cover_and_Index.pdf` (6 หน้า: 1 หน้าปก + 5 หน้าสารบัญ A4 แนวนอน 89 รายการ ขยายช่องชื่อผู้รับ/ผู้โอน ระยะขอบ 1.25 ซม. สารบัญ-1 ถึง 5)
  - รายงานสรุปการเงิน Excel: `Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx` จัดกึ่งกลาง Sarabun Light พร้อมไฮไลต์หน้าระบุสลิปสีอำพัน
  - ซิงค์การ Decouple ไปยัง `_skills/Dicut_Chat`, `_engines/Dicut_Chat`, `Portable/core`, และ `process_master_slips_system1.py`

---

## ⚖️ 2. Immutable Enforced Rules (กฎเหล็กห้ามละเมิดเด็ดขาด)

1. **Strict Zero-Guessing:** ห้ามเดา/มโนชื่อธนาคาร ชื่อบุคคล หรือตัวเลขในสลิปโดยเด็ดขาด อ่านได้เท่าไหร่ใช้เท่านั้น ผูกตาม EMVCo QR หรือบัญชีคู่สัญญาที่พิสูจน์แล้ว
2. **Pure White Canvas for Slips:** ห้ามใช้ Corner Median สร้างขอบสีเทาหรือกรอบสีกับสลิปเดี่ยว ต้องใช้ `#FFFFFF` ล้วน
3. **Memo Protection Standard:** ครอปสลิปต้องเว้นระยะเผื่อใต้บรรทัด "วันที่ทำรายการ" ~180px ป้องกันบันทึกช่วยจำสูญหาย
4. **Table Grid Styling:** ทุกช่องจัดกึ่งกลาง (Center-Aligned) ฟอนต์ Sarabun (11 ปกติ, 12 หนาสำหรับหัว) เส้นขอบบาง 4 ด้าน
5. **PyMuPDF C-Binding:** ใช้ PyMuPDF (fitz) สตรีมมิ่งเป็นแกนหลักความเร็วสูงเสมอ
6. **Pixel-Level OCR Standard:** สแกนตรวจ อ่าน และสกัดตัวอักษรลงลึกถึงระดับพิกเซลเท่านั้น ห้ามเดาคำนำหน้าชื่อหรือชื่อย่อ
7. **Decoupled Dossier Standard:** ห้ามนำหน้าปกหรือสารบัญไปรวมในไฟล์เนื้อหาแชท/สลิปเด็ดขาด เพื่อให้หน้าแรกของไฟล์เนื้อหาคือหน้า 1 ตรงกับเลขหน้ากระดาษที่พิมพ์จริงเสมอ 1:1

