<!-- ============================================================================== -->
<!-- 🏛️ PROJECT IDENTITY & SYSTEM ARCHITECTURE BLUEPRINT                          -->
<!-- 👤 ROLE: SENIOR FULL-STACK DEVELOPER AGENT                                     -->
<!-- 📦 PROJECT: DIGITAL_EVIDENCE                                                   -->
<!-- 📅 UPDATED: 2026-09-14T12:46:00+07:00                                          -->
<!-- ============================================================================== -->

# 🏛️ DIGITAL_EVIDENCE — Digital Evidence Processing & Automation System

> **System Mission:** ระบบอัตโนมัติระดับ Production Ready สำหรับการตรวจจับ รวบรวม จัดหมวดหมู่ ตัดต่อ และประมวลผลพยานหลักฐานดิจิทัล (ภาพแชทหลักฐาน, สลิปโอนเงิน, บัญชีธุรกรรม) พร้อมระบบค้นหาและสกัดตำแหน่งหน้าสลิป (`Search_Slip`) และระบบสกัดข้อมูลสลิปการเงินจริง 13 คอลัมน์ (`OCR_Slip`) พร้อมระบบตรวจจับสลิปซ้ำซ้อนและประวัติการพิมพ์ ผลิตรายงานคดีความในรูปแบบ PDF และ Excel สอดคล้องตามมาตรฐานงานสืบสวน นิติวิทยาศาสตร์ดิจิทัล และกฎหมายพยานหลักฐานอิเล็กทรอนิกส์ ภายใต้ธรรมนูญความซื่อสัตย์ระดับสูงสุด (Zero-Guessing / Zero-Hallucination)

---

## 🎯 1. 🧭 Executive Summary & Core Capabilities

ระบบ **`DIGITAL_EVIDENCE`** ประกอบด้วยสถาปัตยกรรม 7 มิติหลัก:
1. **Chat Evidence Stitching & Layout Normalization:** ตัดต่อภาพแคปหน้าจอแชทแบบยาว (Long Screenshot Stitched Chat) ไร้รอยต่อ ไร้เส้นดำ และจัดหน้า A4 แนบชิดเต็มบล็อคโดยไม่มีช่องว่างขาวโหว่ (`slip-block-fit` 5 ขั้นตอน)
2. **Dynamic Prefix Grouping & Natural Sorting (`List_names`):** ตรวจจับและจัดกลุ่มไฟล์หลักฐานที่ถูก Rename อัตโนมัติจาก Windows (`Ctrl+A` เช่น `V1- (1).jpg` $\rightarrow$ เคส `V1`) แล้วส่งออกเป็นเอกสารหลักฐานตรงเคส
3. **Automated Slip Search & Page Indexing (`Search_Slip`):** สแกนตรวจจับหน้ากระดาษ A4 ใน PDF ที่สร้างเสร็จแล้วเพื่อระบุเลขหน้าที่แปะสลิปธนาคาร (เช่น หน้า 64, 65, 97) พร้อมสกัดข้อมูลธุรกรรม (ยอดเงิน, วันที่, ผู้โอน, ผู้รับ, รหัสอ้างอิง) ส่งออกเป็นตารางสารบัญ Excel และ JSON ทันที
4. **Universal 18-Bank Slip Extraction Engine (`OCR_Slip`):** สกัดข้อมูลสลิปโอนเงินจริง 13 คอลัมน์ รองรับ 18 สถาบันการเงินในไทย ด้วยการกรองสีพื้นหลังแบบ Morphological Filter + CLAHE + ถอดรหัสรหัสธนาคาร 3 หลักจาก EMVCo QR Code (BOT Standard Tag 00 $\rightarrow$ 01) + Multi-Pass OCR (`tha+eng`) พร้อมระบบผูกคู่สัญญาบัญชี (Ground Truth Knowledge Binding)
5. **Duplicate Slip & Printed Log Forensic Auditor:** ตรวจจับสลิปที่ซ้ำซ้อนกันในแบทช์เดียวกัน (ตรวจจากเลขอ้างอิง Ref ID และชื่อไฟล์) และตรวจสอบเทียบกับประวัติสลิปที่เคยถูกพิมพ์/ประมวลผลแล้ว พร้อมไฮไลต์เตือนสีส้ม-แดงใน Excel ป้องกันการนำสลิปใบเดิมมาวนใช้หรือเบิกซ้ำในคดี
6. **Bank Branch & Memo Extraction:** ดึงสาขาธนาคารจากสลิปเคาน์เตอร์/ตู้ ATM ลงในช่องบันทึกช่วยจำอัตโนมัติ
7. **Strict Honesty & Evidence Integrity Governance:** กฎเหล็กห้ามคาดเดา มโน หรือสร้างข้อมูลเท็จในเอกสารหลักฐานโดยเด็ดขาด ทุกจุดต้องพิสูจน์ได้จากภาพจริงหรือรหัสธุรกรรมจริง
8. **Git Remote Repository & Disaster Recovery:** ผูกกับคลังข้อมูลหลักบน GitHub [`https://github.com/palaside/EVIDENCE.git`](https://github.com/palaside/EVIDENCE.git) พร้อมกักกันข้อมูลส่วนบุคคลและหลักฐานคดี (PDPA Shielded via `.gitignore`)

---

## 📦 Git Remote Repository (SSOT)
* **URL:** `https://github.com/palaside/EVIDENCE.git`
* **Clone Command:**
  ```bash
  git clone https://github.com/palaside/EVIDENCE.git
  ```
* **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

---

## 🌟 0. ⚡ คู่มือใช้งานแบบไม่ต้องพิมพ์คำสั่ง (Zero-Command Automation)

### 1. ระบบเฝ้าโฟลเดอร์อัตโนมัติ 24 ชม. (Hot Folder Background Service)
* **โฟลเดอร์รับงาน:** [`EVIDENCE_IN`](file:///d:/Project/DIGITAL_EVIDENCE/EVIDENCE_IN)
* **โฟลเดอร์ผลลัพธ์:** [`Folder_Out`](file:///d:/Project/DIGITAL_EVIDENCE/Folder_Out)
* **วิธีใช้งาน:**
  - นำรูปสลิป หรือโฟลเดอร์สลิปมาวางไว้ใน `EVIDENCE_IN`
  - เซอร์วิสหลังบ้าน [`tools/slip_hotfolder_watcher.py`](file:///d:/Project/DIGITAL_EVIDENCE/tools/slip_hotfolder_watcher.py) จะตรวจจับไฟล์ใหม่ สกัดข้อมูลด้วย OCR + QR Code + PII Guard และสร้างไฟล์ Excel (ฟอนต์ Sarabun จัดกึ่งกลาง) ส่งไปยัง `Folder_Out` ให้อัตโนมัติทันที 24 ชม.

### 2. ติดตั้งให้เริ่มทำงานพร้อมเปิดเครื่อง Windows (Auto Startup) — *แก้ปัญหาลง Windows ใหม่*
* **ไฟล์ติดตั้งคลิกเดียว:** [`install_startup.bat`](file:///d:/Project/DIGITAL_EVIDENCE/install_startup.bat)
* **ไฟล์ถอนการติดตั้ง:** [`uninstall_startup.bat`](file:///d:/Project/DIGITAL_EVIDENCE/uninstall_startup.bat)
* **เมื่อลง Windows ใหม่ในอนาคต:**
  1. เปิดไดรฟ์ `D:\Project\DIGITAL_EVIDENCE` (ไฟล์ทั้งหมดของคุณยังอยู่ที่เดิม ไม่หายไปกับการลง Windows)
  2. ดับเบิลคลิก [`install_startup.bat`](file:///d:/Project/DIGITAL_EVIDENCE/install_startup.bat) **เพียง 1 ครั้ง**
  3. ระบบจะค้นหาตำแหน่ง Python และสร้างทางลัดเข้าสู่โฟลเดอร์ Windows Startup (`shell:startup`) ให้อัตโนมัติทันที
  4. ทุกครั้งที่เปิดคอมพิวเตอร์ ระบบจะตื่นขึ้นมาทำงานเงียบๆ อยู่เบื้องหลัง (Background Silent Mode ไม่มีหน้าต่างดำกวนใจ)

### 3. ทางลัดแบบลากไฟล์มาหย่อนทับ (Drag & Drop Launcher)
* **ไฟล์โปรแกรม:** [`RUN_SLIP_EXTRACTOR.bat`](file:///d:/Project/DIGITAL_EVIDENCE/RUN_SLIP_EXTRACTOR.bat)
* **วิธีใช้งาน:**
  - **ลากวางทันที:** คลิกค้างที่ไฟล์รูปสลิป หรือโฟลเดอร์ที่มีสลิป แล้วลากมาหย่อนทับไอคอน `RUN_SLIP_EXTRACTOR.bat` ระบบจะเริ่มสกัดและเปิดโฟลเดอร์ผลลัพธ์ให้ทันที
  - **กดเลือกเมนู:** ดับเบิลคลิกเปิด จะมีเมนูภาษาไทย [1]-[6] ให้เลือกโหมดได้ง่ายๆ เช่น สแกนปกติ, สแกนพร้อมเซ็นเซอร์ข้อมูลส่วนบุคคล PDPA, หรือกดติดตั้ง Startup ได้ในปุ่มเดียว

---

## 🗺️ 2. 🚀 Project Roadmap & Milestones

```
[Phase 1: Foundation & Ingestion] (Completed)
  ├── 🟢 Multi-channel Evidence Ingestion (EVIDENCE_IN, EVIDENCE_CHAT_IN)
  ├── 🟢 Windows Explorer Ctrl+A Rename Detection Engine (List_names)
  └── 🟢 Natural Sequence File Sorter & Case Prefix Extractor

[Phase 2: Core Processing & Engine Pipeline] (Completed & Production Ready)
  ├── 🟢 Dicut_Chat: Smart Quiet Zone Detector & Edge Noise Filter
  ├── 🟢 Slip-Block-Fit Protocol (645x890 & 807x1115 Canvas Wallpaper Filler)
  ├── 🟢 Dark Edge Band Strip & Feather Stitching
  └── 🟢 QR Slip Decoding & Bank Classification Pipeline

[Phase 3: Automated Indexing & Forensic Reporting] (Completed & Active)
  ├── 🟢 Search_Slip: Computer Vision Badge & Slip Card Scanner
  ├── 🟢 Post-PDF Transaction Detail Extractor (Tesseract OCR + Regex Engine)
  ├── 🟢 10-Column Forensic Slip Indexing (Excel & JSON Outputs)
  └── 🟢 Pipeline Hook: Auto-trigger Search_Slip right after PDF generation

[Phase 4: Universal Slip Mode Engine & Forensic Audit] (Completed & Production Ready)
  ├── 🟢 OCR_Slip: Morphological Background Subtraction + CLAHE Filter
  ├── 🟢 3-Digit BOT Financial Institution Code Extractor (EMVCo QR Tag 00 -> Sub-tag 01)
  ├── 🟢 SSOT Master Dictionary covering 18 Thai Financial Institutions
  ├── 🟢 Bank Branch (สาขา) Extraction integrated into Memo
  ├── 🟢 Duplicate Slip & Historical Printed Log Auditor (In-batch + Cross-batch warning)
  ├── 🟢 13-Column Legal Forensic Ledger with Warning Cell Highlighting
  └── 🟢 40-Slip Stress Test (KTB 20 + TTB 20) Achieved 100.0% Accuracy

[Phase 5: Legal Evidence Table Grid Layout & Typography] (Completed & Enforced)
  ├── 🟢 Chat Evidence Blueprint Alignment: Exact layout matching Chat_Evidence+Automation+excel+AGENTS.md
  ├── 🟢 Absolute Center Alignment: Every data cell & numeric field center-aligned horizontally & vertically
  ├── 🟢 Official Typography Standard: Sarabun & Sarabun Light/Bold font hierarchy across Excel & PDFs
  ├── 🟢 Complete 4-Sided Cell Border: Crisp thin borders on every cell (Border(left=thin, right=thin, ...))
  ├── 🟢 Generous Column Widths: Expanded from 9.5 to 32pt preventing text truncation
  ├── 🟢 A4 Landscape Sheet Setup: Standardized print dimensions, margins, and 20-row page breaks
  └── 🟢 Centered Legal Disclaimer: 3-line statutory non-modification disclaimer at table footer

[Phase 6: Archiving, Security & Memory Governance] (Completed & Maintained)
  ├── 🟢 Batch Timestamped Preservation (`processed/Case_{ID}/Batch_{TS}/`)
  ├── 🟢 Non-Destructive Orphan Cleanup (`_archive/orphaned_cleanup_20260913/`)
  ├── 🟢 Strict Zero-Guessing Honesty Rule in Constitutional Governance (`AGENTS.md`)
  └── 🟢 Persistent Agent Memory & Mistakes Tracking (`memory/behavior.json`, `memory/mistakes.md`)
```

---

## 📂 3. 🌲 Directory Structure Blueprint

```text
d:/Project/DIGITAL_EVIDENCE/
├── 📄 AGENTS.md                                # Hub Agent Constitutional Governance (Strict Honesty Rule)
├── 📄 README.md                                # [SSOT] Project System Blueprint
├── 📄 PROJECT_STATUS.md                        # Reverse Engineering Feature Audit & Health Report
├── 📄 CHAT_HISTORY.md                          # ASCII Art Architecture Dual-Bubble Chat Archive
├── 📄 PROJECT_FLOW.md                          # 100% English Technical Pipeline Specification
├── 📄 extract_stress_test.py                   # 40-Slip Benchmark & Stress Testing Script
├── 📂 tessdata/                                # Local OCR Traineddata (tha.traineddata, eng, osd)
├── 📂 _skills/                                 # Specialized Agent Skills
│   ├── 📂 List_names/                          # Prefix Grouping & PDF Assembly Pipeline
│   ├── 📂 Dicut_Chat/                          # Chat Slicing & Slip-Block-Fit Background Normalizer
│   ├── 📂 Search_Slip/                         # Post-PDF Slip Locator & Page Indexer
│   ├── 📂 OCR_Slip/                            # Universal 18-Bank Slip Engine with Duplicate Auditor
│   └── 📂 SAVE/                                # System State Preservation Protocol (SAVE.md)
├── 📂 _engines/                                # Production Ready Mirrored Engines
│   ├── 📂 Search_Slip/                         # Search_Slip Mirrored Engine
│   └── 📂 OCR_Slip/                            # OCR_Slip Mirrored Engine (13-Column + Auditor)
├── 📂 Folder_Out/                              # Production Output Artifacts
│   ├── 📄 Evidence_Chat_V1.pdf                 # Golden Standard Chat Evidence (107 Pages)
│   ├── 📄 Evidence_Chat_V1_Slip_Index.xlsx     # Forensic Slip Page Index (Pages 64, 65, 97)
│   ├── 📄 Evidence_Chat_V1_Slip_Index.json     # Structured JSON Slip Page Index
│   ├── 📄 Test_Extraction_KTB_TTB_40Slips.xlsx # 40-Slip 13-Column Excel Ledger (100.0% Validated)
│   └── 📄 Test_Extraction_KTB_TTB_40Slips.json # 40-Slip Extraction Structured JSON
├── 📂 memory/                                  # Persistent Agent Memory & Constitutional Learning
│   ├── 📄 behavior.json                        # Learned Preferences & Workflow Automation Counters
│   ├── 📄 mistakes.md                          # Immutable Mistakes Log & Anti-Hallucination Safeguards
│   └── 📄 printed_slips.log                    # Historical Printed Slips Archive for Audit
└── 📂 state/                                   # Redundant Backup Mirror of Core Documents
```

---

## ⚡ 4. 🚀 Quick Start & Execution Commands

### 4.1 รันระบบจัดกลุ่มภาพและต่อแชทอัตโนมัติ (`List_names` + `Dicut_Chat`)
```powershell
python _skills/List_names/scripts/list_names.py
```

### 4.2 รันค้นหาตำแหน่งหน้าสลิปในเล่ม PDF (`Search_Slip`)
```powershell
python _skills/Search_Slip/scripts/search_slip.py --pdf Folder_Out/Evidence_Chat_V1.pdf
```

### 4.3 รันสกัดข้อมูลสลิป 13 คอลัมน์พร้อมระบบตรวจสลิปซ้ำ (`OCR_Slip`)
```powershell
python _skills/OCR_Slip/scripts/ocr_slip.py --input "path/to/slip.jpg" --out Folder_Out/result.xlsx
```

### 4.4 รันชุดทดสอบความแม่นยำ 40 สลิป (`extract_stress_test.py`)
```powershell
python extract_stress_test.py
```

<!-- ============================================================================== -->
<!-- 🏁 END OF README.md                                                            -->
<!-- ============================================================================== -->
