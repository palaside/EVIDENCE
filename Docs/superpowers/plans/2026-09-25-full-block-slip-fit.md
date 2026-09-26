# Full-Block Slip Fit & Reference Standard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish and enforce the 100% Reference Measurement Standard across all evidence export pipelines, ensuring that all bank transfer slips proportionally expand to touch the standard evidence block bounds (`TW = 645 px`, `TH = 890 px`), nested chat bubbles are cleanly excised in `SLIP` mode, and the mandatory interactive pre-export confirmation protocol (`--sample` vs `--all`) is strictly followed.

**Architecture:** 
1. Use `core/evidence_theme.py` as the Single Source of Truth (SSOT) for the Header Evidence Ribbon, 3-line Forensic Legal Disclaimer, and `fit_slip_block()` scaling logic (`scale = min(TW / w_orig, TH / h_orig)` via Lanczos).
2. Enhance `extract_pure_slip_card()` to isolate the pure bank slip card boundary from nested chat pages (e.g. Master Combined PDF), removing chat bubbles and wallpaper 100%.
3. Standardize CLI entry points (`tools/name_filter.py`, `tools/generate_slip_evidence_dossier.py`) with the mandatory interactive prompt: ask whether to generate a **"ตัวอย่าง (1 หน้าจริง)"** or **"ทั้งหมด"**.

**Tech Stack:** Python 3.10+, PIL (Pillow), openpyxl, pypdfium2, unittest.

## Global Constraints
- Target Evidence Block dimensions: `TW = 645 px`, `TH = 890 px`.
- Standard A4 Portrait dimensions: `993 x 1406 px`.
- Evidence Block paste coordinates: `paste_x = (993 - 645) // 2 = 174`, `paste_y = 120 + ((1200 - 890) // 2) = 275`. Center is `(322.5, 445)` relative to the block.
- Zero geometric distortion: Aspect ratio of the slip card must be preserved 100%.
- Slips must expand proportionally to touch either 645 px width or 890 px height. No artificial `min(1.0, ...)` downscale-only ceiling.
- SSOT Theme: Header Ribbon (Logo height 75px, Evidence Shield, Mode, Corroborated, Page) and Footer 3-line Legal Disclaimer must remain intact.
- Pre-Export Prompt Protocol: Always offer `[1] ตัวอย่าง (1 หน้าจริง)` vs `[2] ทั้งหมด` before any multi-page generation.

---

### Task 1: SSOT Full-Block Slip Fit Implementation (`core/evidence_theme.py`)

**Files:**
- Modify: `core/evidence_theme.py`
- Modify: `tests/test_evidence_theme.py`
- Mirrors: `tools/evidence_theme.py`, `Portable/core/evidence_theme.py`

**Interfaces:**
- Produces: `fit_slip_block(slip_pil: Image.Image, target_w: int = 645, target_h: int = 890) -> Image.Image`
  - Calculates `scale = min(target_w / float(w_orig), target_h / float(h_orig))`
  - Scales using `Image.Resampling.LANCZOS`
  - Returns `block_canvas` (645x890) centered at `((target_w - w_new) // 2, (target_h - h_new) // 2)`

- [x] **Step 1: Write unit test in `tests/test_evidence_theme.py` verifying small slip expands to touch 645x890 boundary**
- [x] **Step 2: Implement `fit_slip_block` in `core/evidence_theme.py` without downscale-only ceiling**
- [x] **Step 3: Run `py tests/test_evidence_theme.py` to confirm 2/2 tests pass**
- [x] **Step 4: Synchronize mirrors to `tools/evidence_theme.py` and `Portable/core/evidence_theme.py`**

---

### Task 2: Target Evidence Filter Reference Alignment (`tools/name_filter.py`)

**Files:**
- Modify: `tools/name_filter.py`
- Mirrors: `_skills/Only/scripts/name_filter.py`, `Portable/core/name_filter.py`

**Interfaces:**
- Consumes: `fit_slip_block` from `core.evidence_theme`
- Produces: `SAMPLE_Evidence_Target_จิณห์นิภา_ประสาทเขตการ.png` (Confirmed 100% Reference Compliant)

- [x] **Step 1: Update `tools/name_filter.py` to import and apply `fit_slip_block`**
- [x] **Step 2: Add dynamic workspace path resolution for raw images in `Done/`**
- [x] **Step 3: Export 1-page sample preview: `Folder_Out/SAMPLE_Evidence_Target_จิณห์นิภา_ประสาทเขตการ.png`**
- [x] **Step 4: User verified and confirmed: 100% matches reference measurement block standard**

---

### Task 3: Pure Slip Card Isolation for Nested Chat Slips (`core/evidence_theme.py` & `tools/generate_slip_evidence_dossier.py`)

**Files:**
- Modify: `core/evidence_theme.py`
- Modify: `tools/generate_slip_evidence_dossier.py`
- Mirrors: `tools/evidence_theme.py`, `Portable/core/evidence_theme.py`

**Interfaces:**
- Produces: `extract_pure_slip_card(img: Any) -> Image.Image`
  - Detects the bank slip card container inside chat conversation feeds
  - Cuts away preceding chat messages/bubbles (e.g. "เอาเลขอะไรไปให้คิดดู...", "กรุงศรีถูกไหม") and trailing background
  - Preserves bank header badge (Krungthai, KBank, SCB, Krungsri) and white card body
- Consumes: `fit_slip_block(slip_card)` to scale the isolated card to 645 px width or 890 px height

- [ ] **Step 1: Refine `extract_pure_slip_card` in `core/evidence_theme.py` to separate multi-row chat bubbles from the continuous slip card body**
- [ ] **Step 2: Test extraction on page 50 of Master Combined PDF to verify `scratch/pure_krungthai_card.png` isolation**
- [ ] **Step 3: Run `tools/generate_slip_evidence_dossier.py --sample` to update `Folder_Out/SAMPLE_Evidence_Slips_95_Fit_Summary.png`**
- [ ] **Step 4: Verify that the sample slip page displays the isolated card filling the 645x890 block with zero chat bubbles**

---

### Task 4: Interactive Pre-Export Confirmation & Quality Gate Verification

**Files:**
- Inspect: `tools/generate_slip_evidence_dossier.py`
- Inspect: `tools/name_filter.py`
- Verify: `tools/pre_delivery_quality_gate.py`

**Interfaces:**
- Mandatory CLI input: "ต้องการสร้าง 'ตัวอย่าง (1 หน้าจริง)' หรือ 'ทั้งหมด' (sample/all) [default: sample]:"
- Pre-Delivery Forensic Quality Gate checklist passing 100%

- [ ] **Step 1: Ensure interactive prompt default is `sample` across all CLI generation tools**
- [ ] **Step 2: Run `py tools/pre_delivery_quality_gate.py` to verify all 10 forensic quality dimensions**
- [ ] **Step 3: Deliver verified 1-page sample preview images and ask user for confirmation before executing full dossier**
