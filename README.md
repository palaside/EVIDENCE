# DIGITAL_EVIDENCE

ระบบประมวลผลหลักฐานดิจิทัลสำหรับงานสลิปโอนเงิน ภาพแชท เอกสารประกอบคดี และรายงานส่งศาล โดยยึดหลัก Zero-Guessing, Pixel-Level Evidence, ตรวจสอบย้อนกลับได้ และสร้างผลลัพธ์ PDF/Excel/JSON ที่สัมพันธ์กัน

อัปเดต snapshot: 2026-09-23 เวลา Asia/Bangkok

---

## สถานะภาพรวม

`DIGITAL_EVIDENCE` เป็น workspace หลักที่รวมหลายชั้นงาน:

- ระบบหลักฐานแชทและสลิป: `EVIDENCE_IN/`, `EVIDENCE_CHAT_IN/`, `Folder_Out/`
- engine/skill เฉพาะทาง: `_skills/`, `_engines/`, `Portable/`
- dashboard / live preview / export: `PROJECT_EVIDENCE_3COL_PROTOTYPE.html`, `tools/data_server.py`
- PDF generator ใหม่: `tools/pdf_export.py`
- PDF.js viewer แบบ local asset: `static/pdfjs/`
- ระบบสำรองฉุกเฉิน: `Standalone_Suite/`

ข้อกำหนดล่าสุดจากผู้ใช้:

- `Standalone_Suite/` เป็นระบบสำรองฉุกเฉิน ไม่ใช่ระบบหลัก
- หากมีการยกระดับเป็นระบบหลัก ผู้ใช้จะสั่งชัดเจนภายหลัง
- ระบบหลักยังอยู่ที่ root workspace `D:\Project\DIGITAL_EVIDENCE`

---

## ฟีเจอร์สำคัญที่ตรวจพบจากไฟล์จริง

| ส่วน | สถานะ | หลักฐาน |
|---|---:|---|
| Hot folders | มี | `EVIDENCE_IN/`, `EVIDENCE_CHAT_IN/` |
| Output หลัก | มี | `Folder_Out/` |
| Python dependency set | มี | `requirements.txt` |
| Node dependency สำหรับ PDF.js | มี | `package.json`, `package-lock.json` |
| PDF generator | มี | `tools/pdf_export.py` |
| HTTP API server | มี | `tools/data_server.py` |
| Dashboard preview/export | มี | `PROJECT_EVIDENCE_3COL_PROTOTYPE.html` |
| Standalone fallback | มี | `Standalone_Suite/` |
| PDF.js local runtime | มี | `static/pdfjs/pdf.min.mjs`, `static/pdfjs/pdf.worker.min.mjs` |
| Quality gate | มี | `tools/pre_delivery_quality_gate.py` |
| `tools/save-state.py` | NOT_FOUND | ตรวจแล้วไม่มีไฟล์ |
| `tools/run-tests.py` | NOT_FOUND | ตรวจแล้วไม่มีไฟล์ |
| `tools/scan-secrets.py` | NOT_FOUND | ตรวจแล้วไม่มีไฟล์ |

---

## โครงสร้างหลัก

```text
D:\Project\DIGITAL_EVIDENCE
|-- AGENTS.md
|-- README.md
|-- PROJECT_STATUS.md
|-- CHAT_HISTORY.md
|-- PROJECT_FLOW.md
|-- requirements.txt
|-- package.json
|-- package-lock.json
|-- PROJECT_EVIDENCE_3COL_PROTOTYPE.html
|-- config.json
|-- EVIDENCE_IN/
|-- EVIDENCE_CHAT_IN/
|-- Folder_Out/
|-- Portable/
|-- Standalone_Suite/
|   |-- index.html
|   |-- tools/data_server.py
|   |-- static/pdfjs/
|   |-- Folder_Out/
|-- static/pdfjs/
|   |-- pdf.min.mjs
|   |-- pdf.worker.min.mjs
|-- tools/
|   |-- data_server.py
|   |-- pdf_export.py
|   |-- pre_delivery_quality_gate.py
|   |-- scaffold_agent.py
|   |-- verify_master_evidence.py
|   |-- ...
|-- _skills/
|-- _engines/
|-- Docs/
|-- memory/
|-- state/
```

---

## PDF Export + PDF.js Viewer

ระบบ PDF production ล่าสุดมี 2 ส่วน:

1. Generator ฝั่ง Python
   - ไฟล์: `tools/pdf_export.py`
   - ใช้ `pymupdf` เพื่อสร้าง PDF จริงจาก canvas snapshot
   - รับข้อมูลผ่าน endpoint `POST /api/pdf/export`
   - เขียนไฟล์ออกที่ `Folder_Out/`

2. Viewer ฝั่ง browser
   - ใช้ PDF.js local runtime จาก `static/pdfjs/`
   - หน้า root: `PROJECT_EVIDENCE_3COL_PROTOTYPE.html`
   - หน้า standalone: `Standalone_Suite/index.html`
   - กด export แล้ว modal จะแสดง preview จาก PDF จริง

หลักฐานการตรวจ:

- Python compile ผ่าน: `tools/pdf_export.py`, `tools/data_server.py`, `Standalone_Suite/tools/data_server.py`
- JSON parse ผ่าน: `package.json`, `package-lock.json`
- Smoke generator สร้าง PDF 1 หน้าและเปิดอ่านด้วย PyMuPDF ได้
- Browser QA root ผ่าน: export -> API -> PDF -> PDF.js canvas
- Browser QA standalone ผ่าน: export -> API -> PDF -> PDF.js canvas
- ไฟล์ทดสอบ PDF ที่สร้างระหว่าง QA ถูกลบแล้ว

---

## วิธีรันระบบหลัก

หากต้องการเปิด HTTP server หลัก:

```powershell
py tools\data_server.py
```

URL หลักที่ server ชี้ไป:

```text
http://127.0.0.1:8088/
```

หมายเหตุ: ก่อน restart server ต้องตรวจพอร์ต 8088 ก่อนเสมอ เพราะพบว่ามี process อื่นอาจฟังอยู่ เช่น `python antigravity_standalone_builder.py`

```powershell
Get-NetTCPConnection -LocalPort 8088 -ErrorAction SilentlyContinue
```

---

## วิธีรัน Standalone Suite

Standalone ใช้เป็นระบบสำรองฉุกเฉิน ไม่ใช่ระบบหลักในตอนนี้

```powershell
cd Standalone_Suite
py tools\data_server.py
```

หรือใช้ไฟล์ launcher ที่มีอยู่:

```text
Standalone_Suite\run.bat
Standalone_Suite\run.ps1
Standalone_Suite\LocalFlow.vbs
```

ข้อควรจำ:

- ใช้ standalone เมื่อระบบหลักเสีย, ต้องย้ายเครื่อง, ต้องทำงาน offline, หรือต้องกู้ flow ฉุกเฉิน
- อย่าถือ `Standalone_Suite/` เป็น SSOT จนกว่าผู้ใช้สั่งให้ยกระบบนี้ขึ้นเป็นหลัก

---

## คำสั่งตรวจคุณภาพ

ตรวจ quality gate ที่มีอยู่จริง:

```powershell
py tools\pre_delivery_quality_gate.py
```

ผลล่าสุดที่รันในการเซฟรอบนี้:

```text
STATUS: 100% PASS (ALL GREEN)
10/10 checks passed
```

คำสั่งที่ระบุใน AGENTS แต่ไฟล์ไม่พบใน workspace ปัจจุบัน:

```text
tools\understand.py        NOT_FOUND
tools\run-tests.py         NOT_FOUND
tools\scan-secrets.py      NOT_FOUND
tools\save-state.py        NOT_FOUND
```

---

## การพัฒนาต่อที่แนะนำ

1. ทำให้ `tools/data_server.py` เป็น entrypoint เดียวที่ประกาศชัดเจน
2. เพิ่ม regression test สำหรับ `POST /api/pdf/export`
3. เพิ่ม test HTML/browser สำหรับ PDF.js preview โดยไม่ต้องใช้ test PDF ค้างใน output
4. แยก policy ว่าอะไรต้อง mirror ไป `Standalone_Suite/` และอะไรอยู่เฉพาะระบบหลัก
5. สร้าง `tools/save-state.py` หรือปรับ AGENTS ให้ตรงกับไฟล์จริง

---

## Resume Notes

หาก agent ถัดไปเข้ามาทำงานต่อ ให้เริ่มจาก:

```powershell
Get-ChildItem -Force
Get-ChildItem tools
Get-NetTCPConnection -LocalPort 8088 -ErrorAction SilentlyContinue
py -m py_compile tools\pdf_export.py tools\data_server.py Standalone_Suite\tools\data_server.py
py tools\pre_delivery_quality_gate.py
```

ห้ามอ่านหรือ print ค่าใน `.env` ให้รายงานเฉพาะชื่อไฟล์หรือชื่อ key เมื่อจำเป็นเท่านั้น
