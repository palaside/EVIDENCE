# Unified Evidence SSOT Theme & Strict Slip Isolation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Centralize Header Evidence Ribbon & Footer Legal Disclaimer into an authoritative Single Source of Truth (`core/evidence_theme.py`), enforce strict 1-slip-card = 1-A4-page pure isolation (cutting out surrounding chat bubbles), and establish the mandatory interactive pre-export prompt ("Sample (1 page)" vs "All").

**Architecture:** Create `core/evidence_theme.py` (and mirror to `tools/` and `Portable/core/`) providing unified methods: `load_evidence_fonts()`, `load_evidence_logo()`, `apply_header_ribbon()`, `apply_footer_disclaimer()`, and `render_evidence_page()`. Refactor `_skills/Dicut_Chat/scripts/process_chat.py`, `tools/generate_slip_evidence_dossier.py`, and `tools/name_filter.py` to import and call this SSOT exclusively. Refine slip isolation so that SLIP mode crops pure transfer slip cards without chat conversation backgrounds.

**Tech Stack:** Python 3.10+, PIL (Pillow), PyMuPDF (fitz), OpenCV (cv2), openpyxl.

## Global Constraints
- Every page rendered must use Sarabun fonts: `Sarabun-ExtraLight.ttf` (17pt/16pt), `Sarabun-Thin.ttf` (17pt), `Sarabun-Bold.ttf` (18pt).
- Header Evidence Ribbon must have Logo (h=75px), `MODE : ...`, `CORROBORATED : ...` with dynamic auto-fit, and `PAGE : X / Total`.
- Footer Disclaimer must be 3 lines in Sarabun ExtraLight 16pt, color `#333333`, 22px spacing, centered.
- Zero Blue Underline (`draw_line`) and zero grey divider bars on headers across the entire repository.
- In SLIP mode: exactly 1 slip card = 1 A4 page. Must crop purely to the transfer slip boundary, removing chat bubbles and conversation context 100%.
- Before exporting any document, prompt the user: "สร้างตัวอย่าง (1 หน้าจริง) หรือทั้งหมด".

---

### Task 1: Create Central SSOT Theme Module (`core/evidence_theme.py`)

**Files:**
- Create: `core/evidence_theme.py`
- Create: `tests/test_evidence_theme.py`

**Interfaces:**
- Produces:
  - `load_evidence_fonts() -> Dict[str, ImageFont]`
  - `load_evidence_logo(target_h: int = 75) -> Optional[Image.Image]`
  - `apply_header_ribbon(canvas: Image.Image, mode: str, corroborated: str, page_str: str, fonts: dict, logo_img: Image.Image, is_landscape: bool = False) -> None`
  - `apply_footer_disclaimer(canvas: Image.Image, fonts: dict, is_landscape: bool = False) -> None`
  - `create_evidence_canvas(width: int = 993, height: int = 1406, bg_color: tuple = (255, 255, 255)) -> Image.Image`

- [ ] **Step 1: Write the failing unit test for `core/evidence_theme.py`**

```python
# tests/test_evidence_theme.py
import pytest
from PIL import Image

def test_theme_imports_and_renders():
    from core.evidence_theme import (
        load_evidence_fonts,
        load_evidence_logo,
        apply_header_ribbon,
        apply_footer_disclaimer,
        create_evidence_canvas
    )
    fonts = load_evidence_fonts()
    assert "header_lbl" in fonts
    assert "header_val" in fonts
    assert "footer" in fonts

    canvas = create_evidence_canvas(993, 1406)
    logo = load_evidence_logo(75)
    apply_header_ribbon(canvas, mode="TARGET EVIDENCE", corroborated="บุคคลเป้าหมาย: จิณห์นิภา", page_str="1 / 10", fonts=fonts, logo_img=logo)
    apply_footer_disclaimer(canvas, fonts=fonts)
    assert canvas.size == (993, 1406)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `& 'C:\Users\EVE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest tests/test_evidence_theme.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'core.evidence_theme'`

- [ ] **Step 3: Implement `core/evidence_theme.py`**

Create `core/evidence_theme.py` with standard font loading (Sarabun ExtraLight, Thin, Bold), logo loader, `apply_header_ribbon` with auto-fit, and `apply_footer_disclaimer`.

- [ ] **Step 4: Run test to verify it passes**

Run: `& 'C:\Users\EVE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest tests/test_evidence_theme.py`
Expected: PASS

- [ ] **Step 5: Mirror `core/evidence_theme.py` to `tools/evidence_theme.py` and `Portable/core/evidence_theme.py`**

---

### Task 2: Refactor `tools/name_filter.py` to Consume `evidence_theme.py`

**Files:**
- Modify: `tools/name_filter.py`
- Modify: `_skills/Only/scripts/name_filter.py`
- Modify: `Portable/core/name_filter.py`

**Interfaces:**
- Consumes: `from evidence_theme import load_evidence_fonts, load_evidence_logo, apply_header_ribbon, apply_footer_disclaimer`
- Produces: `export_target_pdf` using unified theme functions.

- [x] **Step 1: Replace custom font/header/footer code in `name_filter.py` with `evidence_theme`**
- [x] **Step 2: Verify `name_filter.py` compiles and executes with zero regression**
- [x] **Step 3: Verify output PDF matches exact pixel-perfect standard**

---

### Task 3: Refactor `tools/generate_slip_evidence_dossier.py` to Consume `evidence_theme.py`

**Files:**
- Modify: `tools/generate_slip_evidence_dossier.py`

**Interfaces:**
- Consumes: `from evidence_theme import load_evidence_fonts, load_evidence_logo, apply_header_ribbon, apply_footer_disclaimer`
- Produces: `render_portrait_slip_page` and landscape table rendering using unified SSOT theme.

- [x] **Step 1: Replace custom `load_sarabun_fonts` and header/footer drawing in `generate_slip_evidence_dossier.py`**
- [x] **Step 2: Test rendering slip dossier**
- [x] **Step 3: Verify PDF visual appearance**

---

### Task 4: Enforce Strict Slip Card Isolation (1 Slip Card = 1 A4 Page, No Chat Background)

**Files:**
- Modify: `core/evidence_theme.py`
- Modify: `tools/name_filter.py`
- Modify: `tools/generate_slip_evidence_dossier.py`

**Interfaces:**
- Produces: `extract_pure_slip_card(img: Image.Image) -> Image.Image` that detects the transfer slip rectangle (via white card contour / bank badge anchor) and crops strictly to the slip boundary, removing surrounding chat bubbles, background wallpaper, and timestamp text.

- [x] **Step 1: Implement `extract_pure_slip_card` in `evidence_theme.py`**
- [x] **Step 2: Connect pure card extraction into `name_filter.py` and `generate_slip_evidence_dossier.py`**
- [x] **Step 3: Verify that rendering a slip image produces purely the slip card on 1 A4 page (no chat text)**

---

### Task 5: Implement Pre-Export Interactive Prompt Protocol ("Sample" vs "All")

**Files:**
- Modify: `memory/behavior.json`
- Modify: CLI flags in `tools/name_filter.py` (`--sample`)
- Modify: CLI flags in `tools/generate_slip_evidence_dossier.py` (`--sample`)

- [x] **Step 1: Add `--sample` argument to tools (generates exactly 1 page + preview PNG for instant inspection)**
- [x] **Step 2: Record rule in `memory/behavior.json`: "ต่อไปเวลาสั่งออกเอกสาร ให้ถามผมว่าสร้างตัวอย่าง (1 หน้าจริง) หรือทั้งหมด"**
- [x] **Step 3: Test `--sample` execution producing `SAMPLE_...pdf` and `SAMPLE_...png` in <1 second**
