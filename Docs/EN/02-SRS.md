# 02 · SRS — Software Requirements Specification
# Project DIGITAL_EVIDENCE (To-Be)

> Location: `Docs/EN/02-SRS.md` (new) | Companion: `Docs/EN/01-PRD.md`
> Iron rules: Pixel-Level OCR, never guess (AGENTS.md), 10-dimension Pre-Delivery Gate

## 1. Functional Requirements

### FR-01 List_names (Grouping & Sort)
- Detect prefix from Windows Ctrl+A names: `V1- (1).jpg` → case `V1`
- Natural sort: 1,2,…,9,10,11 (no lexicographic sort)
- Input: `EVIDENCE_CHAT_IN/`, `EVIDENCE_IN/` | Output: ordered case groups

### FR-02 Dicut_Chat (Slice & Stitch)
- Streaming Canvas: one long strip, then slice at Quiet Zone Lookahead 1.30x
- 12px feather stitch, strip 13-row black bands, Slip-Block-Fit canvas (645x890 / 807x1115)
- Smart zoom: vertical slips 900px on Pure White #FFFFFF, 2px micro-trim, 180px Memo breathing room below transaction date
- Post-Slice Dedup Rule 14: SHA-256 + RefID equal to previous page → drop

### FR-03 Search_Slip (Locator & Index)
- Scan finished PDF for badge/slip cards, report page numbers (e.g., 64,65,97)
- Extract: amount, date, sender, receiver, ref
- 10-column index (centered Sarabun Excel + JSON); first column `slip page` gold/amber + PDF-jump hyperlinks
- End-of-dossier summary: 20 rows/page A4 landscape, no banner box

### FR-04 OCR_Slip (13-Column Extraction)
- Preprocess: morphological BG subtraction + CLAHE + multi-pass `tha+eng`
- Tier1: 3-digit BOT code from EMVCo QR Tag00 Sub-tag01 (100% bit-accurate)
- Tier2: local forensic CV/OCR | Tier3: vision fallback (Typhoon) + SHA-256 cache
- 18-bank master dictionary, branch (`สาขา...`) → Memo, broken Thai months → 12 standard months, ISO timestamp decode from Ref
- PII Guard `--mask-pii`: 13-digit ID, 10-digit mobile, 16-digit credit, 10–12 digit accounts (8 banks)

### FR-05 Duplicate & Printed-Log Auditor
- In-batch: same RefID / filename / 16-char SHA-256 fingerprint → `⚠️ duplicate (Ref same as #X)`
- Cross-batch: compare `memory/printed_slips.log` → `⚠️ already printed`
- Highlight: light-orange FFF2CC + dark-red C00000

### FR-06 Assembly & Certification
- Cover (executive dossier, 6-clause box) + 5-page index + 2,387-page Master chat (continuous numbering)
- Decoupled: Cover+Index separate file, chat starts at physical 1 = printed 1
- Header ribbon: left logo + MODE (SLIP/CHAT only) + CORROBORATED + PAGE | Footer: 3-line centered Sarabun Thin certification
- Hash: SHA-256 manifest + certificate PDF (Electronic Transactions Act B.E. 2544)

### FR-07 Automation & Portable
- 24h watcher `tools/slip_hotfolder_watcher.py`: drop → OCR/QR → centered Sarabun Excel → `Folder_Out` + auto-open Explorer
- Portable: `INBOX_SLIPS/INBOX_CHATS/OUTPUT`, Pure-ASCII `.bat` → UTF-8 `launcher.py`, drag & drop, Thai menu [1][2][3][9]
- Startup: `install_startup.bat`/`uninstall_startup.bat` + `run-silent.vbs` + `tick.py`
- Immortal: `open_project_state.py` reads `LATEST_CHECKPOINT.md` in 0.1s

### FR-08 Dashboard (new To-Be)
- Read-only, reads `Folder_Out/*.xlsx|*.json` only, never writes back
- Summary: totals/counts/cases/gate status/duplicates
- Search: RefID, name, date range, bank | click → open that PDF page

## 2. Non-functional Requirements

| Category | Target |
|---|---|
| Performance | Build/merge 100 pages ≤1s (PyMuPDF), 560 slips ≤5 min on 6 cores |
| Accuracy | 40-slip stress 100%, receiver bank 100%, 0 duplicate pages |
| Integrity | Zero-guessing, pixel-level every glyph/tone/account digit |
| Usability | Double-click use, no typing, Thai menu, Sarabun font |
| Typography | Every cell centered (H+V), thin 4-side borders, widths 9.5–32pt, A4 landscape, 3-line centered disclaimer |
| Reliability | 100% page auto-audit, fallback never guesses |
| Security | PDPA masking, `.gitignore` case shield, `.env` key-names only |
| Portability | `Portable/` runs anywhere, fresh Windows needs one `install_startup.bat` run |

## 3. Business Rules & Validation

- BR-01: empty amount = 0, empty date = 0, unnamed = 0 (any excess = FAIL)
- BR-02: no account numbers inside person-name fields (100% cleaned)
- BR-03: MODE is SLIP or CHAT only (no SUMMARY)
- BR-04: normal page CORROBORATED=`continuous dialogue`, slip page=`evidence slip page [X] / financial index [#Y]`
- BR-05: JSON==Excel==PDF 100% (rows/totals/refs match)
- BR-06: centered grid, widened columns, auto font scale 12→10/9pt against overflow

## 4. Access Matrix

| Function | Clerk | Investigator | Reviewer | Admin | Watcher |
|---|---|---|---|---|---|
| Drop to INBOX | ✓ | ✓ | – | ✓ | – |
| Run pipeline | – | ✓ | – | ✓ | auto |
| Read OUTPUT/Dashboard | ✓ | ✓ | ✓ | ✓ | writes |
| Hash verify/approve | – | – | ✓ | ✓ | – |
| Startup install/state recovery | – | – | – | ✓ | – |

## 5. Error Handling

| Case | Behavior |
|---|---|
| Blurry/low-res | Escalate to pixel-level vision, mark `recheck`, never guess |
| Unreadable QR | `QR_N/A` + Tier2/3, never invent bank |
| Duplicate/already printed | Keep row + warning + color, count in dup report |
| Non-slip (food/photos) | Pure-financial gate filters out |
| Corrupt PDF/xref clash | Halt pipeline + log + keep checkpoint, never overwrite good output |
| Busy port/wrong path/encoding | Warn before start, ≤2 retries with changed logic |

## 6. Acceptance Criteria

- 10-dimension gate ALL GREEN (`py tools/pre_delivery_quality_gate.py`)
- `py tools/run-tests.py` all 18 green (if present)
- 4-Tier report: Tier1 Static [PASS] + Tier2 Unit (40-slip) [PASS] + Tier3 Integration [PASS/not-tested] + Tier4 E2E [PASS/not-tested] — never lumped
- 6-point self-review (Scope/Syntax/Verification/Env/Security/Clean) complete

## Outcome
Knows how each function must behave, what verifies it, and what happens on failure.
