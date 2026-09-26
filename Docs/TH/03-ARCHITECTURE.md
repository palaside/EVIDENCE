# 03 · ARCHITECTURE — System Architecture Document
# โครงการ DIGITAL_EVIDENCE (To-Be)

> ตำแหน่ง: `Docs/TH/03-ARCHITECTURE.md` (สร้างใหม่) | ห้ามแก้ `README.md/AGENTS.md/tools/_skills/_engines`

## 1. Technology Stack (ยึดของเดิม ห้าม Drift)

- Runtime: Python 3.x (`requirements.txt`), Windows 10/11 (`\` separator, `.bat` Pure ASCII + `launcher.py` UTF-8)
- PDF: PyMuPDF (`fitz`) C-Binding มาตรฐานหลัก (100 หน้า ~0.15s)
- OCR: Tesseract (`tessdata/tha.traineddata, eng, osd`) Multi-Pass `tha+eng` + CLAHE + Morph Filter
- QR: EMVCo Parser (Tag00 → Sub-tag01 = BOT Code 3 หลัก)
- Excel: openpyxl (Sarabun, Center H+V, Border thin 4 ด้าน, Landscape A4, 20 แถว/หน้า)
- Vision (Fallback): Typhoon OCR v1.5 + Typhoon 2.5 30B audit
- Automation: `tick.py` + `run-silent.vbs` + `install_startup.bat`/`uninstall_startup.bat`
- VCS: Git `https://github.com/palaside/EVIDENCE.git` + PDPA `.gitignore`
- ห้ามเพิ่ม: Next.js / Spring / NestJS / DB Server หนักในเฟสนี้ (YAGNI)

## 2. Frontend / Backend / Database

- **Frontend (Local):** ไม่มีเว็บ SPA — ใช้ `.bat` Launcher เมนูไทย + Windows Explorer (`Folder_Out`, `Portable/OUTPUT`) + Excel/PDF เป็น UI หลัก; Dashboard To-Be เป็นหน้า static read-only อ่าน JSON/XLSX (ไม่ต้องมี server)
- **Backend (Local Pipeline):** `tools/` = orchestrator (`process_real_chat_evidence.py`, `slip_hotfolder_watcher.py`, `quality_agent.py`, `open_project_state.py`, `pre_delivery_quality_gate.py`); `_skills/` = source skills (List_names, Dicut_Chat, Search_Slip, OCR_Slip, Typhoon_OCR, Only, Consistent, SAVE); `_engines/` = mirrored production engines; `memory/` = behavior/mistakes/printed log
- **Database:** ไม่มี RDBMS — ใช้ไฟล์เป็น DB: `Folder_Out/*.xlsx|*.json` (ledger/index), `memory/printed_slips.log`, `LATEST_CHECKPOINT.md`, `state/` mirror; Dashboard อ่านไฟล์เหล่านี้ตรง (To-Be ค่อย map เป็น tables ตาม `04-DATA-MODEL.md`)

## 3. Module & Component Architecture

```text
INBOX (EVIDENCE_IN / EVIDENCE_CHAT_IN / Portable/INBOX_*)
  → List_names [group+sort]
  → Dicut_Chat [slice+stitch+block-fit+zoom] → PDF Chat (2,387 หน้า)
  → Search_Slip [scan PDF → 10-col index] → Excel/JSON
  → OCR_Slip 3-Tier [QR→CV/OCR→Vision] → 13-col ledger + audit highlight
  → Only/Consistent [target filter + corroboration]
  → Assembly [Cover+Index 6p + Chat + Hash Cert]
  → Folder_Out / Portable/OUTPUT
  → Dashboard (To-Be, read-only)
  ↘ SAVE/Immortal [checkpoint + memory]
```

## 4. API Architecture

- ไม่มี HTTP API ภายนอกในเฟสนี้; การเชื่อมต่อเป็น CLI/File-contract:
- `list_names.py` → stdout กลุ่มเคส (JSON)
- `search_slip.py --pdf <path>` → `<name>_Slip_Index.{xlsx,json}`
- `ocr_slip.py --input <img|dir> --out <xlsx>` (+ `--mask-pii`)
- `typhoon_ocr.py` CLI (schema `schema.json`)
- `open_project_state.py` → สรุป checkpoint 0.1s
- `pre_delivery_quality_gate.py` → ALL GREEN / FAIL 10 มิติ
- Dashboard To-Be: `GET file://Folder_Out/*.json` (อ่านไฟล์ตรง, ไม่มี POST/เขียนกลับ)

## 5. Authentication & Authorization

- Local single-user: ไม่ต้อง login; สิทธิ์ตามบทบาทกระดาษ (ดู `02-SRS.md` §4)
- Secrets: รับผ่านช่องกรอก → `.env` ผ่าน allowlist เท่านั้น; โค้ดอ่านจาก env; อ่าน `.env` เฉพาะชื่อ Key ห้ามโชว์ค่า; สแกน `scan-secrets.py --strict` ก่อน commit
- PDPA: mask PII ตอน export; `.gitkeep` + `.gitignore` กัน `Portable/INBOX_*`, `EVIDENCE_IN`, คดีจริงหลุดขึ้น Git

## 6. Project Folder Structure (To-Be เสนอเพิ่มแค่ Docs/)

```text
D:/Project/DIGITAL_EVIDENCE/
├── Docs/TH|EN/01-PRD..05-SYSTEM-FLOW.md  # ใหม่ (ชุดนี้)
├── AGENTS.md, README.md, PROJECT_STATUS.md  # ห้ามแก้
├── EVIDENCE_IN/, EVIDENCE_CHAT_IN/, Folder_Out/, Portable/
├── _skills/, _engines/, tools/, memory/, state/
├── tessdata/, tesseract.exe, *.bat, *.vbs
```

## 7. การเชื่อมต่อระหว่างส่วนประกอบ

| จาก → ไป | ช่องทาง | สัญญา |
|---|---|---|
| Watcher → OCR_Slip | เรียก function/CLI | path รูป → ledger rows |
| Chat PDF → Search_Slip | hook อัตโนมัติหลัง gen PDF | PDF path → index rows |
| OCR/Search → Excel | openpyxl template Sarabun Center | 13/10 คอลัมน์ + สีเตือน |
| ทุกขั้น → SAVE | `save-state.py --quiet` | backup 4 ไฟล์ลง `state/` |
| OUTPUT → Dashboard | อ่านไฟล์ | JSON==Excel==PDF |
| ทุกขั้น → Quality Gate | CLI | ALL GREEN จึงส่งมอบ |

## ผลลัพธ์
รู้ว่าต้องสร้างโฟลเดอร์อะไร (เพิ่มแค่ `Docs/`) ไฟล์อยู่ตรงไหน แต่ละส่วนรับผิดชอบอะไร และห้ามเพิ่ม stack ใด
