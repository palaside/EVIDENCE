# 07 · UI SPEC — Rev02 Dark Gray (Screenshot-Grounded)
# Project DIGITAL_EVIDENCE

> Location: `Docs/EN/07-UI-SPEC-REV02-SCREEN.md` (new, originals untouched)
> Reference: 3-column screenshot (CHAT/SLIP header + DONE 100% + timer + SYNC + totals)
> Code ref: `DIGITAL_EVIDENCE_REV02.html` (200 on :8010), backend `tools/rev02_server.py`

## 1. Locked Tone (from screen)

- Pure warm black `#080A0D` + gray ambient glows (no blue): all 3 panels are matte black rounded cards on black
- Cards: `rgba(255,255,255,.03-.075)` + 26px blur + `rgba(255,255,255,.12)` border + `0 15px 44px rgba(0,0,0,.4)` shadow + top highlight
- Primary buttons (Accept / Generate / Print PDF): silver gradient `linear-gradient(180deg,#E6EBF0,#AEB6BF)`, black text `#0B0E12`, full-width — as in screenshot
- Secondary (active CHAT / PDF tab / plain runs): gray `#747D87` or `#1B2026` surface with `#343B44` border
- Status: green dot + `DONE · 100%` (header), gray `queued` chips, mono log lines; green `#16A34A` / orange `#F59E0B` / red `#DC2626` for real status only, always with text
- Type: Sarabun (TH/EN), JetBrains Mono (numbers/Ref/file sizes/log/timer) — filenames + `1972297 B` and `[01/4]` lines are mono

## 2. Layout (from screen)

- Single header: DE logo + `DIGITAL_EVIDENCE · Rev02 Dark Gray` + `CHAT|SLIP` segmented + status pill (`DONE · 100%…`) + `00:00` timer + `⟳ SYNC` + totals button
- 3 columns 28/44/28, 14px gap/padding, fit-to-screen `100dvh`, no page scroll (in-panel scroll only)
- LEFT eyebrow `LEFT · CONTROLS` / `อัปโหลด & ค้นหา`; CENTER `CENTER · REVIEW` / result title; RIGHT `RIGHT · SUMMARY` / totals title

## 3. LEFT — Controls (from screen)

1. **Upload & File Queue:** dashed dropzone (`JPG · PNG · PDF`) + 4 file rows (`V1- (1..4).jpg` + byte size + queued) + right `queued` chip
2. **Search & Target:** `⌕` search box + empty tags + `0 items — upload first` line (never preload names — zero-state rule)
3. **Corroboration:** switch + filter label + `switch state is not proof` note
4. **✓ Accept — start processing:** full-width silver button between Corroboration and Processing; uploads then runs real OCR
5. **Processing:** `--mask-pii (PDPA)` checkbox + `⚡ Generate` (disabled until 100%) + `progress … 100%` row + full progress bar + `generated · 4 rows · REV02_…xlsx` line + mono log box (`$ …ocr_slip.py`, `[01/4] … Amount: … Ref: …`, `[OK] Saved Excel/JSON ledger: …`)

## 4. CENTER — Review (from screen)

- Toolbar: `PDF | ผลลัพธ์` tabs + `‹ 1 / ? ›` + page box + `Fit` + `⛶ Full` + silver `Print original` + `Download`
- Stage: black dotted; empty before Generate (as in screenshot); after Generate shows real result table `#/file/bank/amount/ref/status` from `/api/result` — never mocked
- Uploaded PDFs preview in PDF tab via object URL (user's real bytes); print/download = same original; no html2canvas

## 5. RIGHT — Summary (from screen)

- 2×2 KPIs (mono numerals, counted from the real run only, 0 at start)
- Evidence PDFs table (`uploaded file | open`, empty until a PDF is uploaded)
- Master Slips card (unique vs dup from this run's auditor)
- Document Actions: silver Print + secondary Download + `SFX/password: placeholder` note

## 6. Flow (from screen)

```text
upload (4 files) → Accept → upload → real OCR (% from [i/n] log) → 100% → Generate unlocked
→ Generate → center table + right KPIs/tags/hits (numbers match log: generated · 4 rows · REV02_….xlsx)
```

## 7. States

- Start: everything 0 (KPIs/tags/tables/bar) — never preload the old 95-row index
- Running: `UPLOADING/RUNNING` status, bar follows real %, live log tail, Accept/Generate disabled
- 100%: `DONE · 100% · press Generate`, Generate enabled
- Failed: `FAILED/ERROR` + reason, bar 0, Accept re-enabled

## 8. Acceptance

- [ ] All panels 0 at start, no leaked names/numbers from old data
- [ ] Accept→100%→Generate ends with real `REV02_*.xlsx/.json` on disk
- [ ] Center table = rows from the real JSON, KPIs = real counts
- [ ] No blue accent, passing contrast, silver focus rings, reduced-motion respected
- [ ] Responsive: ≤1239 two columns, ≤1023 single column (PDF ≥62vh)

## Outcome
This spec = the approved screen + real Accept/Generate behavior; reference for further UI work without touching the legacy pipeline.
