"""
Single Source of Truth (SSOT) Evidence Theme & Styling Engine
Defines the authoritative standards for:
- Header Evidence Ribbon (MODE, CORROBORATED with Auto-Fit, PAGE stamp, EVIDENCE Logo)
- Footer Legal Disclaimer (3 lines Sarabun ExtraLight 16pt, centered)
- Typography (Sarabun font weights: ExtraLight, Thin, Light, Regular, Bold)
- Canvas geometry (Portrait 993x1406, Landscape 1406x993)
- Slip-Block-Fit standard (645x890 centered on pure white canvas)
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Legal Disclaimer Text (Court-Standard Forensic Protection) ---
DISCLAIMER_LINES = [
    '"DIGITAL EVIDENCE เป็นเพียงเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา',
    'จากต้นฉบับใดๆ และไม่มีส่วนเกี่ยวข้องใดๆ กับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์',
    'เอกสารแบบอิเล็กทรอนิกส์ เท่านั้น"'
]

# --- Font Loader ---
def load_evidence_fonts() -> Dict[str, Any]:
    f_extralight = r"C:\Windows\Fonts\Sarabun-ExtraLight.ttf"
    f_thin = r"C:\Windows\Fonts\Sarabun-Thin.ttf"
    f_reg = r"C:\Windows\Fonts\Sarabun-Regular.ttf"
    f_bold = r"C:\Windows\Fonts\Sarabun-Bold.ttf"
    f_light = r"C:\Windows\Fonts\Sarabun-Light.ttf"
    fallback = r"C:\Windows\Fonts\tahoma.ttf"

    def _f(path, size):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
        if os.path.exists(fallback):
            try:
                return ImageFont.truetype(fallback, size)
            except Exception:
                pass
        return ImageFont.load_default()

    return {
        "header_lbl": _f(f_extralight, 17),
        "header_val": _f(f_thin, 17),
        "header_bold": _f(f_bold, 18),
        "footer": _f(f_extralight, 16),
        "table_hdr": _f(f_bold, 13),
        "table_body": _f(f_light, 12),
        "table_small": _f(f_light, 11),
        "thin_path": f_thin if os.path.exists(f_thin) else (f_light if os.path.exists(f_light) else fallback),
        "light_path": f_light if os.path.exists(f_light) else fallback,
        "bold_path": f_bold if os.path.exists(f_bold) else fallback,
    }


# --- Logo Loader ---
def load_evidence_logo(target_h: int = 75) -> Optional[Image.Image]:
    candidates = [
        PROJECT_ROOT / "EVIDENCE.png",
        PROJECT_ROOT / "EVIDENCE.jpg",
        Path(r"C:\Users\EVE\OneDrive\เดสก์ท็อป\EVIDENCE.png"),
        Path(r"C:\Users\EVE\OneDrive\เดสก์ท็อป\EVIDENCE.jpg"),
        PROJECT_ROOT / "_engines" / "Dicut_Chat" / "assets" / "EVIDENCE.png",
        PROJECT_ROOT / "_skills" / "Dicut_Chat" / "assets" / "EVIDENCE.png",
    ]
    for p in candidates:
        if p.exists() and p.is_file():
            try:
                raw = Image.open(str(p))
                scale = target_h / float(raw.height)
                target_w = max(1, int(raw.width * scale))
                resized = raw.resize((target_w, target_h), Image.Resampling.LANCZOS)
                return resized
            except Exception:
                pass
    return None


# --- Canvas Factory ---
def create_evidence_canvas(width: int = 993, height: int = 1406, bg_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    return Image.new("RGB", (width, height), bg_color)


# --- Header Evidence Ribbon ---
def apply_header_ribbon(
    canvas: Image.Image,
    mode: str,
    corroborated: str,
    page_str: str,
    fonts: Dict[str, Any],
    logo_img: Optional[Image.Image] = None,
    is_landscape: bool = False,
    margin: Optional[int] = None
) -> None:
    draw = ImageDraw.Draw(canvas)
    pw, ph = canvas.size

    margin_x = margin if margin is not None else (102 if is_landscape else 93)
    header_y = 25 if is_landscape else 38

    # 1. Logo
    if logo_img:
        if logo_img.mode == "RGBA":
            canvas.paste(logo_img, (margin_x, header_y), logo_img)
        else:
            canvas.paste(logo_img, (margin_x, header_y))
        text_x = margin_x + logo_img.width + 20
    else:
        text_x = margin_x

    line1_y = header_y + 8
    line2_y = header_y + 40

    # 2. Line 1: MODE
    draw.text((text_x, line1_y), "MODE : ", fill="#111827", font=fonts["header_lbl"])
    b_lbl = draw.textbbox((text_x, line1_y), "MODE : ", font=fonts["header_lbl"])
    draw.text((b_lbl[2], line1_y), str(mode), fill="#111827", font=fonts["header_val"])

    # 3. Line 1: PAGE (Right-Aligned)
    b_pval = draw.textbbox((0, 0), str(page_str), font=fonts["header_val"])
    b_plbl = draw.textbbox((0, 0), "PAGE : ", font=fonts["header_lbl"])
    total_p_w = (b_plbl[2] - b_plbl[0]) + (b_pval[2] - b_pval[0])
    px = pw - margin_x - total_p_w
    draw.text((px, line1_y), "PAGE : ", fill="#111827", font=fonts["header_lbl"])
    b_pr = draw.textbbox((px, line1_y), "PAGE : ", font=fonts["header_lbl"])
    draw.text((b_pr[2], line1_y), str(page_str), fill="#111827", font=fonts["header_val"])

    # 4. Line 2: CORROBORATED with Auto-Fit Scaling
    draw.text((text_x, line2_y), "CORROBORATED : ", fill="#111827", font=fonts["header_lbl"])
    b_cor = draw.textbbox((text_x, line2_y), "CORROBORATED : ", font=fonts["header_lbl"])

    max_w = (pw - margin_x) - b_cor[2]
    f_val = fonts["header_val"]
    cur_sz = 17
    while cur_sz >= 10:
        b_val = draw.textbbox((0, 0), str(corroborated), font=f_val)
        if (b_val[2] - b_val[0]) <= max_w:
            break
        cur_sz -= 1
        try:
            f_val = ImageFont.truetype(fonts["thin_path"], cur_sz)
        except Exception:
            break
    draw.text((b_cor[2], line2_y), str(corroborated), fill="#111827", font=f_val)


# --- Footer Legal Disclaimer ---
def apply_footer_disclaimer(
    canvas: Image.Image,
    fonts: Dict[str, Any],
    is_landscape: bool = False,
    margin: Optional[int] = None
) -> None:
    draw = ImageDraw.Draw(canvas)
    pw, ph = canvas.size
    margin_x = margin if margin is not None else (102 if is_landscape else 93)

    footer_y = ph - 85 if is_landscape else ph - 130
    line_spacing = 18 if is_landscape else 22

    for i, line in enumerate(DISCLAIMER_LINES):
        try:
            bbox = draw.textbbox((0, 0), line, font=fonts["footer"])
            line_w = bbox[2] - bbox[0]
            lx = (pw - line_w) // 2
        except Exception:
            lx = margin_x
        draw.text((lx, footer_y + (i * line_spacing)), line, fill="#333333", font=fonts["footer"])


# --- Pure Slip Card Isolation (1 Slip Image = 1 A4 Page Standard) ---
def extract_pure_slip_card(img: Any) -> Image.Image:
    """
    Extracts strictly the rectangular bank transfer slip card from raw images,
    cutting out surrounding chat conversation bubbles, wallpaper, and mobile UI 100%.
    Works seamlessly with OpenCV (if installed) or 100% pure PIL fallback.
    """
    from PIL import ImageChops

    if isinstance(img, Image.Image):
        pil_img = img.convert("RGB")
    elif hasattr(img, "shape"): # numpy array
        try:
            import cv2
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        except Exception:
            pil_img = Image.fromarray(img)
    else:
        raise TypeError("Input must be a PIL Image or numpy array")

    w, h = pil_img.size
    if h < 100 or w < 100:
        return pil_img

    # 0. Strip Outer A4 / Blank Margins if image is embedded in a large white container
    try:
        bg_white = Image.new("RGB", pil_img.size, (255, 255, 255))
        diff_white = ImageChops.difference(pil_img, bg_white)
        bbox_white = diff_white.getbbox()
        if bbox_white:
            bw = bbox_white[2] - bbox_white[0]
            bh = bbox_white[3] - bbox_white[1]
            if bw < int(w * 0.98) or bh < int(h * 0.98):
                if bw >= 150 and bh >= 150:
                    pil_img = pil_img.crop(bbox_white)
                    w, h = pil_img.size
    except Exception:
        pass
    # 1. Detect nested bank slip card inside chat conversation background
    try:
        import numpy as np
        arr = np.array(pil_img)
        # Thai bank slips have dense white/pale card body
        white_mask = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220)
        y_counts = np.sum(white_mask, axis=1)
        white_rows = np.where(y_counts > (w * 0.35))[0]

        if len(white_rows) > 0:
            y_start = white_rows[0]
            y_end = white_rows[-1]

            # If the white card body is localized (e.g. chat messages exist above it)
            if y_start > int(h * 0.12):
                # Thai bank slips have a bank header badge (Krungthai, KBank, SCB) above white body
                card_top = max(0, y_start - int(h * 0.12))
                card_mask = white_mask[y_start:y_end, :]
                x_counts = np.sum(card_mask, axis=0)
                card_cols = np.where(x_counts > 40)[0]
                if len(card_cols) > 0:
                    card_left = max(0, card_cols[0] - 6)
                    card_right = min(w, card_cols[-1] + 6)
                    card_bottom = min(h, y_end + int(h * 0.04))

                    cw = card_right - card_left
                    ch = card_bottom - card_top
                    if cw >= int(w * 0.35) and ch >= int(h * 0.25):
                        return pil_img.crop((card_left, card_top, card_right, card_bottom))
    except Exception:
        pass

    # 2. PIL-only fallback: detect card bounds by luminance contrast
    try:
        inner = pil_img.crop((int(w * 0.02), int(h * 0.05), int(w * 0.98), int(h * 0.95)))
        bg = Image.new("RGB", inner.size, inner.getpixel((0, 0)))
        diff = ImageChops.difference(inner, bg)
        bbox = diff.getbbox()
        if bbox:
            cw = bbox[2] - bbox[0]
            ch = bbox[3] - bbox[1]
            if cw > (w * 0.40) and ch > (h * 0.25):
                return inner.crop(bbox)
    except Exception:
        pass

    return pil_img


# --- Slip-Block-Fit Protocol (Full-Block Proportional Fill) ---
def fit_slip_block(slip_pil: Image.Image, target_w: int = 645, target_h: int = 890) -> Image.Image:
    """
    Fits any bank transfer slip into the fixed reference evidence block (645 x 890 px),
    scaling proportionally to fully fill the block boundary while strictly locking aspect ratio.
    
    1. Read Worig, Horig
    2. Scale = min(TW / Worig, TH / Horig) -> expands or contracts to touch 645 width or 890 height
    3. Wnew = round(Worig * Scale), Hnew = round(Horig * Scale)
    4. Center coordinates: x = (TW - Wnew) // 2, y = (TH - Hnew) // 2 (center check: (322.5, 445))
    5. Clean background matching slip corner, zero grey lines or artificial borders.
    """
    w_orig, h_orig = slip_pil.size
    if w_orig <= 0 or h_orig <= 0:
        return Image.new("RGB", (target_w, target_h), (255, 255, 255))

    scale = min(float(target_w) / float(w_orig), float(target_h) / float(h_orig))
    w_new = max(1, round(w_orig * scale))
    h_new = max(1, round(h_orig * scale))

    if (w_new, h_new) != (w_orig, h_orig):
        resized = slip_pil.resize((w_new, h_new), Image.Resampling.LANCZOS)
    else:
        resized = slip_pil

    x = (target_w - w_new) // 2
    y = (target_h - h_new) // 2

    corner = resized.getpixel((0, 0))
    if isinstance(corner, int):
        corner = (corner, corner, corner)
    elif len(corner) == 4:
        corner = corner[:3]

    bg_color = (255, 255, 255) if min(corner) > 230 else corner

    block_canvas = Image.new("RGB", (target_w, target_h), bg_color)
    block_canvas.paste(resized, (x, y))
    return block_canvas


# --- Chat-Block-Fit Protocol (Full-Block 807x1115 Top-Aligned) ---
def fit_chat_block(chat_pil: Image.Image, target_w: int = 807, target_h: int = 1115) -> Image.Image:
    """
    Fits any sliced chat evidence page into the fixed reference block (807 x 1115 px),
    scaling proportionally to fill the block boundary while locking aspect ratio.
    Top-aligned (y=0) to ensure continuous reading flow of chat conversations.
    """
    w_orig, h_orig = chat_pil.size
    if w_orig <= 0 or h_orig <= 0:
        return Image.new("RGB", (target_w, target_h), (255, 255, 255))

    scale = min(float(target_w) / float(w_orig), float(target_h) / float(h_orig))
    w_new = max(1, round(w_orig * scale))
    h_new = max(1, round(h_orig * scale))

    if (w_new, h_new) != (w_orig, h_orig):
        resized = chat_pil.resize((w_new, h_new), Image.Resampling.LANCZOS)
    else:
        resized = chat_pil

    x = (target_w - w_new) // 2
    y = 0  # Top-aligned for natural reading flow

    block_canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
    block_canvas.paste(resized, (x, y))
    return block_canvas

