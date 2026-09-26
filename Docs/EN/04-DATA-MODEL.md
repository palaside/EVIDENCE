# 04 · DATA-MODEL — Database Schema & Data Model
# Project DIGITAL_EVIDENCE (To-Be for Dashboard)

> Location: `Docs/EN/04-DATA-MODEL.md` (new)
> Today: file-DB (`Folder_Out/*.xlsx|*.json` + `memory/printed_slips.log`); this doc maps files to tables without changing the pipeline

## 1. Entities & Tables (6)

| Table | Description | Current source |
|---|---|---|
| `cases` | cases/dossiers (V1, …) | List_names prefix |
| `evidence_pages` | every A4 page (2,387) | chat PDF + xref/hash |
| `slips` | financial slips, 13 cols (94) | OCR_Slip ledger |
| `slip_page_index` | 10-col page↔slip map | Search_Slip index |
| `printed_log` | print/process history | `memory/printed_slips.log` |
| `audit_duplicates` | duplicates + color warnings | auditor output |

## 2. Columns & Types

**cases:** `case_id TEXT PK` (e.g., V1), `case_name TEXT`, `owner TEXT`, `created_at TEXT ISO`, `status TEXT` (queued/processing/audited/indexed/exported/certified)

**evidence_pages:** `page_id INTEGER PK`, `case_id FK→cases`, `page_no INTEGER`, `physical_xref TEXT`, `sha256 TEXT UNIQUE`, `mode TEXT CHECK(SLIP,CHAT)`, `corroborated TEXT`, `pdf_path TEXT`

**slips (13 + extras):** `slip_id INTEGER PK`, `case_id FK`, `page_no INTEGER`, `amount REAL`, `txn_date TEXT`, `sender TEXT`, `receiver TEXT`, `sender_bank_code TEXT(3)`, `receiver_bank TEXT`, `ref_id TEXT`, `branch_memo TEXT`, `qr_bot_code TEXT(3)`, `fingerprint TEXT(16)`, `image_path TEXT`, `warn TEXT`

**slip_page_index (10):** `idx INTEGER PK`, `slip_page_no INTEGER` (gold/amber), `case_id FK`, `slip_id FK`, `amount REAL`, `txn_date TEXT`, `counterparty TEXT`, `ref_id TEXT`, `pdf_link TEXT`, `note TEXT`

**printed_log:** `log_id INTEGER PK`, `ref_id TEXT`, `fingerprint TEXT(16)`, `printed_at TEXT`, `batch TEXT`

**audit_duplicates:** `audit_id INTEGER PK`, `slip_id FK`, `dup_with TEXT`, `kind TEXT` (in_batch/cross_batch/printed), `message TEXT`, `color TEXT` (FFF2CC/C00000)

## 3. PK / FK

- PK: single PK per table; `evidence_pages.sha256 UNIQUE`, `slips.(ref_id+fingerprint)` conditional UNIQUE (duplicates allowed but must carry warn)
- FK: `evidence_pages.case_id→cases`, `slips.case_id→cases`, `slip_page_index.case_id→cases + slip_id→slips`, `audit_duplicates.slip_id→slips` (ON DELETE RESTRICT, never delete past audit)

## 4. ERD (Text)

```text
cases 1───* evidence_pages
cases 1───* slips 1───* audit_duplicates
cases 1───* slip_page_index *───1 slips
slips *───* printed_log (via ref_id/fingerprint, soft link not hard FK)
```

## 5. Constraints & Indexes

- `CHECK(mode IN ('SLIP','CHAT'))`, `CHECK(amount>=0)`, empty amount→0 empty date→`''` (counted as FAIL at Gate, not DB)
- No 10–12 digit account numbers in `sender/receiver` (8-bank regex before insert)
- Indexes: `idx_slips_ref(ref_id)`, `idx_slips_fp(fingerprint)`, `idx_pages_case_page(case_id,page_no)`, `idx_index_case(case_id)`, `idx_printed_ref(ref_id)`
- JSON==Excel==PDF: row counts/totals/refs must match before Dashboard promotion (Gate #9)

## 6. Data Access Control

- Clerk/investigator/reviewer: SELECT only via Dashboard
- Watcher/pipeline: INSERT/UPDATE `slips/index/pages/printed_log`
- Admin: approve certified + recover checkpoint; never DELETE `audit_duplicates` (evidence)
- PII: Dashboard shows masked form per `--mask-pii` (partial `***`)

## Outcome
Knows where data comes from (OUTPUT+memory), how it is stored (6 tables), and which columns the Dashboard may use (amount/date/counterparty/ref/slip-page/dup status).
