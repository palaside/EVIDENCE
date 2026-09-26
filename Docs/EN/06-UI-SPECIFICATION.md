# 06 · UI SPECIFICATION (Rev02 + Glassmorphism + PDF Supplement)
# Project DIGITAL_EVIDENCE

> Location: `Docs/EN/06-UI-SPECIFICATION.md` (new, originals untouched)
> Read-only sources:
> - `D:\Project\DIGITAL_EVIDENCE\UI Specification.md:1-753` (Rev02, 19,007B)
> - `C:\Users\EVE\OneDrive\เดสก์ท็อป\Glassmorphism Visual Contract.md:1-227` (Factory V3, all-components, anchor=live)
> - `D:\Project\DIGITAL_EVIDENCE\PROJECT_EVIDENCE_3COL_PROTOTYPE.html` (56,769B)

## 1. Roles & Boundaries (no drift)

- StackBlitz builds UI only (HTML/CSS/JS): layout, theme, responsive, interaction
- Legacy Python pipeline owns: chat/slip processing, PDF generation, Quality Gate, OUTPUT (`Folder_Out`, `Portable/OUTPUT`)
- Dashboard is local read-only this phase (`Docs/EN/03-ARCHITECTURE.md`): no external HTTP API; never assume StackBlitz web can invoke Python or read Windows `Folder_Out` directly
- Both source files stay intact — no copy-over, no edits

## 2. UI Spec Rev02 — Binding Rules (REQ-01..06)

- REQ-01 Fidelity: latest dashboard image is the layout/header/panel/spacing/typography master
- REQ-02 Black & Gray: bg `#080A0D`, panel `#111418`, surface `#1B2026`, elevated `#252B32`, primary gray `#747D87`, hover `#929AA3`, border `#343B44`, text `#F3F4F6`; every former blue accent → gray (tabs/buttons/borders/focus/progress/selection); green `#16A34A` orange `#F59E0B` red `#DC2626` only for real status + always with text/icon, never color-alone
- REQ-03 Responsive: Desktop ≥1440 (3 cols 28/44/28 of content area after 12px gaps) / Laptop 1024–1439 (expand PDF review) / Tablet 768–1023 (PDF top, controls+summary bottom) / Mobile <768 (single column + switcher nav); never lock PDF viewer width into overflow; big tables scroll-x inside panel; key buttons tappable without zoom; PDF keeps native aspect
- REQ-04 Real PDF review: real PDFs only, no A4 mock images; features PDF-01..09 (open/navigate/zoom/fit-width/fullscreen/print-original/download/page-link/loading-error)
- REQ-05 Brand: original DIGITAL EVIDENCE logo, never redrawn; gray rule excludes logo and PDF internals (PDF shows true colors)
- REQ-06 Compatibility: never change pipeline/OCR/gate/data model without approval
- Type: TH+EN Sarabun, digits/RefID JetBrains Mono; title 20–24 / panel 15–17 / body 13–14 / secondary 12–13; radii panel 10–12 / input-button 6–8; padding 16; gap 12
- Header: logo + TH/EN names + CHAT/SLIP + live system status (never stuck ONLINE) + timer + SYNC + totals
- Left (Controls): upload/drag-drop + queue (name/size/status/pre-run remove) / search-target / corroboration switch (switch state is never proof of match) / processing (run + progress + time + counts + errors/recheck)
- Center (PDF Review): pick PDF → viewer load → read real page count → review → open original for print/download
- Right (Summary): KPIs (evidence/matched slips-chats/names/rows) / evidence table (real export columns + search/filter + audit/dup) / master slips (unique/dup + view + link) / document actions (review + gate + print/download original); password + SFX boxes from the mock stay as UI placeholders only, not wired (outside PRD read-only scope)

## 3. PDF Supplement (added today — system can generate PDFs)

- Content/layout/certification of PDFs stays with the legacy pipeline (PyMuPDF C-Binding), not the viewer
- Viewer may only: open/navigate/zoom/fit/fullscreen/open-original-to-print/download/jump via page-link index
- Forbidden: `html2canvas` or dashboard screenshots as print files — print file must be the same original PDF under review (`UI Specification.md` §6.2)
- Dashboard data layer reads OUTPUT (`*.pdf|*.xlsx|*.json` + hash cert/manifest) only
- SFX/password: not wired yet (UI placeholder per §7 note)

## 4. Glassmorphism Contract — Adapted to Black Theme (conflict resolved)

**Conflict:** Factory V3 ambient `#7dd3fc/#c084fc` on `#0f172a` violates REQ-02 (black `#080A0D` + gray, no blue accent).

**Ruling (REQ-02 wins over factory default):**
- Ambient: dark-gray gradient only (`#080A0D → #111418 → #1B2026`); no bright blue/purple wash (blur must read on black)
- Glass surface: `rgba(255,255,255,0.18)` + `blur(26px) saturate(170%)` + `rgba(255,255,255,0.32)` border + 28px radius + `inset 0 1px 0 rgba(255,255,255,0.38)` highlight + `0 15px 44px rgba(0,0,0,0.24)` shadow allowed as card overlays on black
- Text: separate opacities — translucent surface but `#F3F4F6` text stays legible; never whole-component `opacity` (per Component Rules 6–7)
- Shape mode `all components`: no locked W/H in `.glass-card`; grid context (28/44/28 + breakpoints) sizes components; fluid panels use `minmax()/clamp()/fr`
- Fit-to-screen shell: `html,body{height:100%;overflow:hidden}` + `.app-shell{100vw/100dvh; grid auto minmax(0,1fr)}` + `.workspace{min-height:0; grid minmax(280px,390px) minmax(0,1fr)}` + children `min-height:0` + preview `overflow:hidden`; ≤980px single column, ≤620px hide non-critical; `@supports not backdrop-filter` → `rgba(255,255,255,0.4)` fallback
- `live` anchor: fixed/sticky panel keeps definite space, never squeezed; surrounding fluid panels flex without viewport overflow; no page-level scroll (in-panel scroll only)

## 5. Component States (all interactive)

Default gray / hover brighten / active silver-gray / visible focus ring / muted disabled / loading-empty-error always with message, never color-only

## 6. Acceptance (UI)

- [ ] Matches reference + black-gray + original logo + Sarabun/JetBrains Mono
- [ ] 3 breakpoints, no overlap, no PDF overflow, tables scroll-x
- [ ] Real-file viewer covers PDF-01..09, print/download = same original, no html2canvas
- [ ] Glass: blur visible on black, floating cards, light borders, passing contrast, fallback present
- [ ] Live status, corroboration switch claims nothing
- [ ] Pipeline/gate/data model untouched; SFX/password placeholders

## Outcome
StackBlitz can build the black-gray glass-overlay UI from Rev02 + adapted contract immediately, with printed PDF = original pipeline PDF.
