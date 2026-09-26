# 03 · ARCHITECTURE — System Architecture Document
# Project DIGITAL_EVIDENCE (To-Be)

> Location: `Docs/EN/03-ARCHITECTURE.md` (new) | Never edit `README.md/AGENTS.md/tools/_skills/_engines`

## 1. Technology Stack (pinned, no drift)

- Runtime: Python 3.x (`requirements.txt`), Windows 10/11 (`\` separator, Pure-ASCII `.bat` + UTF-8 `launcher.py`)
- PDF: PyMuPDF (`fitz`) C-Binding standard (~0.15s per 100 pages)
- OCR: Tesseract (`tessdata/tha.traineddata, eng, osd`) multi-pass `tha+eng` + CLAHE + morph filter
- QR: EMVCo parser (Tag00 → Sub-tag01 = 3-digit BOT code)
- Excel: openpyxl (Sarabun, center H+V, thin 4-side borders, landscape A4, 20 rows/page)
- Vision fallback: Typhoon OCR v1.5 + Typhoon 2.5 30B audit
- Automation: `tick.py` + `run-silent.vbs` + `install_startup.bat`/`uninstall_startup.bat`
- VCS: Git `https://github.com/palaside/EVIDENCE.git` + PDPA `.gitignore`
- Forbidden to add: Next.js / Spring / NestJS / heavy DB servers in this phase (YAGNI)

## 2. Frontend / Backend / Database

- **Frontend (local):** No web SPA — Thai-menu `.bat` launchers + Windows Explorer (`Folder_Out`, `Portable/OUTPUT`) + Excel/PDF as the UI; To-Be Dashboard is a static read-only page over JSON/XLSX (no server)
- **Backend (local pipeline):** `tools/` orchestrators (`process_real_chat_evidence.py`, `slip_hotfolder_watcher.py`, `quality_agent.py`, `open_project_state.py`, `pre_delivery_quality_gate.py`); `_skills/` source skills (List_names, Dicut_Chat, Search_Slip, OCR_Slip, Typhoon_OCR, Only, Consistent, SAVE); `_engines/` mirrored production engines; `memory/` behavior/mistakes/printed log
- **Database:** No RDBMS — file-DB: `Folder_Out/*.xlsx|*.json` (ledgers/indexes), `memory/printed_slips.log`, `LATEST_CHECKPOINT.md`, `state/` mirror; Dashboard reads these files directly (map to tables later per `04-DATA-MODEL.md`)

## 3. Module & Component Architecture

```text
INBOX (EVIDENCE_IN / EVIDENCE_CHAT_IN / Portable/INBOX_*)
  → List_names [group+sort]
  → Dicut_Chat [slice+stitch+block-fit+zoom] → Chat PDF (2,387 pp)
  → Search_Slip [scan PDF → 10-col index] → Excel/JSON
  → OCR_Slip 3-Tier [QR→CV/OCR→Vision] → 13-col ledger + audit highlight
  → Only/Consistent [target filter + corroboration]
  → Assembly [Cover+6p Index + Chat + Hash Cert]
  → Folder_Out / Portable/OUTPUT
  → Dashboard (To-Be, read-only)
  ↘ SAVE/Immortal [checkpoint + memory]
```

## 4. API Architecture

- No external HTTP API in this phase; CLI/file contracts:
- `list_names.py` → case groups (JSON stdout)
- `search_slip.py --pdf <path>` → `<name>_Slip_Index.{xlsx,json}`
- `ocr_slip.py --input <img|dir> --out <xlsx>` (+ `--mask-pii`)
- `typhoon_ocr.py` CLI (`schema.json`)
- `open_project_state.py` → 0.1s checkpoint summary
- `pre_delivery_quality_gate.py` → ALL GREEN / FAIL on 10 dimensions
- To-Be Dashboard: `GET file://Folder_Out/*.json` (direct file read, no POST/write-back)

## 5. Authentication & Authorization

- Local single-user: no login; paper-role rights (see `02-SRS.md` §4)
- Secrets: input box → `.env` via allowlist only; code reads env; read `.env` key-names only, never values; `scan-secrets.py --strict` before commit
- PDPA: mask PII on export; `.gitkeep` + `.gitignore` keep `Portable/INBOX_*`, `EVIDENCE_IN`, real cases off Git

## 6. Project Folder Structure (To-Be adds only Docs/)

```text
D:/Project/DIGITAL_EVIDENCE/
├── Docs/TH|EN/01-PRD..05-SYSTEM-FLOW.md  # new (this set)
├── AGENTS.md, README.md, PROJECT_STATUS.md  # do not edit
├── EVIDENCE_IN/, EVIDENCE_CHAT_IN/, Folder_Out/, Portable/
├── _skills/, _engines/, tools/, memory/, state/
├── tessdata/, tesseract.exe, *.bat, *.vbs
```

## 7. Inter-Component Connections

| From → To | Channel | Contract |
|---|---|---|
| Watcher → OCR_Slip | function/CLI call | image path → ledger rows |
| Chat PDF → Search_Slip | auto-hook after PDF gen | PDF path → index rows |
| OCR/Search → Excel | openpyxl Sarabun-center template | 13/10 cols + warning colors |
| Every step → SAVE | `save-state.py --quiet` | backup 4 files to `state/` |
| OUTPUT → Dashboard | file read | JSON==Excel==PDF |
| Every step → Quality Gate | CLI | ALL GREEN before delivery |

## Outcome
Knows which folders to create (only `Docs/` added), where files live, what each part owns, and which stacks are forbidden.
