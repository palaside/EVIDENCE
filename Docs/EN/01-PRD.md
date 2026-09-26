# 01 · PRD — Product Requirements Document
# Project DIGITAL_EVIDENCE (To-Be Extension)

> SSOT refs: `README.md`, `PROJECT_STATUS.md`, `AGENTS.md`
> Language: English | Location: `Docs/EN/01-PRD.md` (new file, originals untouched)
> Status: To-Be for continued development (1:1 mirror of TH set)

## 1. Objective & Scope

**Objective:** Extend the digital-evidence pipeline (chat images + transfer slips) from its current state (2,387-page pure A4 chat dossier, 94 slips / 467,218.00 THB, 13-column OCR for 18 banks) toward a Cross-Case Dashboard (Roadmap Phase 7, still open in `PROJECT_STATUS.md:115`), while keeping Zero-Guessing/Zero-Hallucination.

**In-Scope:**
- 24h Hot Folder (`EVIDENCE_IN` → `Folder_Out`), Drag & Drop (`RUN_SLIP_EXTRACTOR.bat`), Portable Suite (`Portable/INBOX_SLIPS`, `INBOX_CHATS`, `OUTPUT`)
- Chat pipeline: Streaming Canvas + Quiet Zone Lookahead 1.30x + 12px Feather + Post-Slice Dedup Rule 14
- Slip pipeline: 3-Tier (EMVCo QR Tier1 + Local CV/OCR Tier2 + Vision Fallback Tier3), Search_Slip 10 columns, OCR_Slip 13 columns, Duplicate Auditor
- SHA-256 Hash Manifest + Evidence Certificate (Electronic Transactions Act)
- Read-only Dashboard aggregating cases (totals/counts/status/search)

**Out-of-Scope:**
- No stack rewrite into a heavy web framework (anti Spec Drift — stay on Python + PyMuPDF + Tesseract)
- No real case data pushed to Git/Remote (PDPA Shield via `.gitignore`)
- No multi-level login system in this phase (stay local single-user)
- No modification of originals (`README.md`, `AGENTS.md`, `PROJECT_STATUS.md`, `tools/`, `_skills/`, `_engines/`)

## 2. User Roles

| Role | Description | Rights |
|---|---|---|
| Investigator | Case owner, reviews PDF/Excel dossiers | Read + run + print |
| Case clerk | Drops files, organizes case folders | Drop to INBOX + read OUTPUT |
| Reviewer/Lead | Completeness check + sign-off | Read + hash verify + approve |
| System admin | Startup install, state recovery | Install/remove + run `open_project_state.py` |
| Watcher (automatic) | `slip_hotfolder_watcher.py` 24h watch | Auto-write OUTPUT |

## 3. Feature List

| ID | Feature | Current | To-Be |
|---|---|---|---|
| F-01 | List_names prefix grouping (V1- (1).jpg → V1) + natural sort | Done | Keep |
| F-02 | Dicut_Chat stitch + Slip-Block-Fit + 900px Smart Zoom on Pure White #FFFFFF | Done | Keep + 180px Memo-safe |
| F-03 | Search_Slip page locator + 10-col index (Excel/JSON) | Done | Add PDF-jump hyperlinks |
| F-04 | OCR_Slip 13 cols + 3-digit BOT code + Branch→Memo | Done | Keep |
| F-05 | Duplicate auditor (in-batch + printed log) orange FFF2CC / red C00000 | Done | Add consolidated report |
| F-06 | Cover + 6-page decoupled Index + Hash cert | Done | Keep |
| F-07 | Portable standalone + silent run + startup | Done | Keep |
| F-08 | Cross-Case Dashboard (totals/counts/status/Ref search) | Missing (Phase 7) | **Build new, read-only** |
| F-09 | Target matcher + Consistency engine (Only/Consistent) | Done | Plug into Dashboard |
| F-10 | Immortal protocol (`LATEST_CHECKPOINT.md` + save/open state) | Done | Keep |

## 4. Problems to Solve

1. Reused/duplicate slips → RefID + SHA-256 fingerprint (16 chars) + printed log
2. Long chat images cut mid-text/batch seams → Streaming Canvas + Quiet Zone + dedup
3. Account numbers mixed in names / Thai month OCR errors (Gn./&.A.) → Pixel-Level OCR + month normalization + name cleaning
4. PDF page numbers vs printed numbers mismatch → Decoupled Cover/Index (chat starts at physical 1)
5. No cross-case overview → Dashboard F-08 (main reason for this doc set)

## 5. Success Criteria

- [ ] Pre-Delivery Gate 10 dimensions ALL GREEN (`AGENTS.md:20`): decoupled 1:1, exact numbering, all slips, empty amount=0, empty date=0, unnamed=0, account-cleaned names, high-contrast Sarabun center grid, JSON==Excel==PDF, no junk files
- [ ] Zero duplicate pages (SHA-256/Xref = 0)
- [ ] 100% receiver-bank hit rate, 40-slip stress test 100%
- [ ] 100 pages in ≤1s (PyMuPDF C-Binding)
- [ ] Dashboard reads real OUTPUT only, never guesses

## Outcome
Knows what the system must do (F-01–F-10) and what is out of scope (no stack rewrite, no original edits, no case data to Git).
