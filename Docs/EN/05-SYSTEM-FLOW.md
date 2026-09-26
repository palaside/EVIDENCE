# 05 · SYSTEM-FLOW — System Workflow & User Flow
# Project DIGITAL_EVIDENCE (To-Be)

> Location: `Docs/EN/05-SYSTEM-FLOW.md` (new) | Links `01-PRD` + `02-SRS` + `04-DATA-MODEL`

## 1. User Journey & User Flow

**Clerk:** drop files to `EVIDENCE_IN`/`INBOX_*` → wait for OUTPUT popup → hand to investigator
**Investigator:** run `RUN_*` or drag-drop → review Excel/JSON/PDF → search Ref/page → print dossier
**Reviewer:** open Hash cert + manifest → compare SHA-256 → approve
**Admin:** one-time startup install → recover via menu [9] when stuck

## 2. Two Main Workflows

### Flow A — Slip (single/batch)
```text
[drop images/folder] → watcher picks up → preprocess (Morph+CLAHE)
→ Tier1 QR (3-digit BOT) → miss? Tier2 OCR → still low? Tier3 Vision
→ normalize (Thai month/ISO/branch→Memo/PII mask)
→ dedup (Ref/FP vs batch + printed.log) → orange/red if dup
→ export 13-col centered Sarabun Excel + JSON → Folder_Out/OUTPUT + open Explorer
→ 10-dimension gate → certified
```

### Flow B — Chat (3 sets → Master)
```text
[drop 3 chat folders] → List_names group+sort → streaming-canvas join
→ slice at QuietZone 1.30x (pack-to-bottom) → Rule14 dedup → 2,387 pp
→ block-fit + 900px zoom #FFFFFF → gen PDF (PyMuPDF)
→ hook Search_Slip → 10-col index + hyperlinks + 20-row/page end summary
→ decoupled Cover+6p Index → hash cert → gate → certified
```

### Flow C — Dashboard (To-Be, read-only)
```text
[open dashboard] → read Folder_Out/*.json → totals/counts/status/dups
→ search (Ref/name/date/bank) → click → open that PDF page
```

## 3. Data Flow (Frontend → API/CLI → DB/File)

| Step | IN | PROC | OUT |
|---|---|---|---|
| Intake | JPG/PNG/PDF in INBOX | watcher/launcher | queue + `cases` |
| Process | queue | `_skills/_engines` | `evidence_pages/slips/index` (files) |
| Export | rows | openpyxl/PyMuPDF | XLSX+JSON+PDF (Sarabun center) |
| Certify | artifacts | gate + SHA-256 | cert + manifest + status=certified |
| Summarize | XLSX/JSON | read-only dashboard | tables/charts/search |

## 4. State Transitions

```text
queued → processing (file caught / run pressed)
processing → audited (100% auto-audit + dedup)
audited → indexed (Search_Slip done)
indexed → exported (Excel/JSON/PDF + hyperlinks complete)
exported → certified (gate ALL GREEN + hash match)
any → needs_review (blurry/QR_N/A/dup/non-slip) → back to processing after root-cause fix
```

## 5. Error Paths

| Breakpoint | Action |
|---|---|
| Blurry image | pixel-level vision, mark review, never guess |
| Unreadable QR | `QR_N/A` + Tier2/3, never invent bank |
| Dup/already printed | keep row + warn + FFF2CC/C00000 + `audit_duplicates` |
| Non-slip | pure gate filters out |
| Corrupt PDF/xref | halt, keep checkpoint, never overwrite good output, clear log |
| Busy port/wrong path/encoding | warn before run, ≤2 retries with changed logic |
| Gate not ALL GREEN | loop-fix at root cause, never deliver |

## 6. Per-Role Views

- Clerk sees INBOX/OUTPUT only; investigator sees ledger/index + run buttons; reviewer sees cert/manifest + approve; admin sees logs/state/startup; watcher is headless
- All roles: click page number → open that PDF page at once (slip-index navigation)

## Outcome
Knows what one button press triggers end-to-end (A/B/C), where failures route, and rollback at `LATEST_CHECKPOINT.md` + `state/`.
