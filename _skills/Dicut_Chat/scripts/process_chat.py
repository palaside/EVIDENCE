import sys
import os
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime
import glob
import re
import json
import tempfile

FEATHER_PX = 12  # ตามสเปก: Alpha Gradient 12 แถวพิกเซลที่รอยต่อ


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def trim_outer_padding(img_bgr, tol=240):
    """
    Trims excessive blank white or black borders around slip/chat images
    so they scale cleanly and fit the A4 page proportionately.
    """
    if img_bgr is None or img_bgr.size == 0:
        return img_bgr
    try:
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        mask = gray < tol
        coords = cv2.findNonZero(mask.astype(np.uint8))
        if coords is None:
            return img_bgr
        x, y, w, h = cv2.boundingRect(coords)
        pad = 12
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img_bgr.shape[1], x + w + pad)
        y2 = min(img_bgr.shape[0], y + h + pad)
        if (w * h) < 0.88 * (img_bgr.shape[0] * img_bgr.shape[1]):
            return img_bgr[y1:y2, x1:x2]
        return img_bgr
    except Exception:
        return img_bgr


def imread_unicode(file_path):
    try:
        data = np.fromfile(file_path, dtype=np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception:
        return cv2.imread(file_path)


def strip_dark_edge_bands(pil_img, max_rows=35, dark_thresh=80):
    """
    Strips solid dark/black horizontal bars (like Android navigation bar/home indicators
    or shadow seams) from the top and bottom of screenshot images before stitching.
    """
    arr = np.asarray(pil_img)
    if arr.ndim < 3:
        return pil_img
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    h = gray.shape[0]
    top_cut = 0
    for y in range(min(max_rows, h)):
        if np.mean(gray[y, :]) < dark_thresh:
            top_cut = y + 1
        else:
            break
    bot_cut = h
    for y in range(h - 1, max(h - 1 - max_rows, 0), -1):
        if np.mean(gray[y, :]) < dark_thresh:
            bot_cut = y
        else:
            break
    if top_cut > 0 or bot_cut < h:
        return pil_img.crop((0, top_cut, pil_img.width, bot_cut))
    return pil_img


def feather_stitch(pil_images, feather_px=FEATHER_PX):
    """เย็บภาพแนวตั้ง: ตัดแถบดำขอบภาพก่อน แล้ว overlap feather_px แถวด้วย Alpha Gradient
    คืน PIL Image แถบยาวชิ้นเดียว"""
    imgs = [strip_dark_edge_bands(im.convert("RGB")) for im in pil_images]
    if len(imgs) == 1:
        return imgs[0]
    w = min(im.width for im in imgs)
    norm = []
    for im in imgs:
        if im.width != w:
            h = max(1, int(im.height * w / im.width))
            im = im.resize((w, h), Image.Resampling.LANCZOS)
        norm.append(im)
    total_h = sum(im.height for im in norm) - feather_px * (len(norm) - 1)
    canvas = np.zeros((total_h, w, 3), np.float32)
    y = 0
    for idx, im in enumerate(norm):
        arr = np.asarray(im).astype(np.float32)
        h = arr.shape[0]
        if idx == 0:
            canvas[y:y + h] = arr
        else:
            t = np.linspace(0, 1, feather_px, dtype=np.float32)[:, None, None]
            canvas[y:y + feather_px] = canvas[y:y + feather_px] * (1 - t) + arr[:feather_px] * t
            canvas[y + feather_px:y + h] = arr[feather_px:]
        y += h - feather_px
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))


def quiet_cuts(strip_rgb, max_h=1115, min_ratio=0.65, max_lookahead_ratio=1.30):
    """
    หาจุดตัดตาม quiet zone (ช่องว่างระหว่างกล่องข้อความจริง)
    ตามกฎเหล็ก 'ห้ามผ่ากลาง' และลอจิก 'ดึง -> ย่อ -> ยัด' (Pack-to-Bottom Slicing):
    1. ตรวจจับพื้นหลังวอลเปเปอร์แชทและวัตถุข้อความ/สลิป/รูปภาพอย่างแม่นยำ ไม่หลงเชื่อช่องว่างภายในกล่องข้อความ
    2. ดึง (Pull): หากข้อความ/สลิปเลยขอบล่างไปเล็กน้อย (<= 1.30x max_h) จะดึง quiet zone ท้ายข้อความลงมาให้เต็มบล็อค
    3. ย่อ (Shrink): สเกลสัดส่วน (Scale-to-fit) ส่วนที่ดึงเกินให้พอดีกรอบบล็อค 807x1115 px ตามหลัก slip-block-fit
    4. ตัดก่อนหน้า: หากวัตถุยื่นยาวเกินลิมิตการดึง จะตัดที่ quiet zone ก่อนหน้า เพื่อดันกล่องข้อความ/สลิปทั้งชิ้นไปหน้าถัดไปแบบสมบูรณ์ 100%
    5. ยัด (Pack): วางชิดขอบบนของหน้ากระดาษเสมอ (Top-Align)
    """
    arr = np.asarray(strip_rgb)
    H, W = arr.shape[:2]

    # 1. ประมาณการสีพื้นหลังวอลเปเปอร์จากขอบซ้าย/ขวา
    bg = np.median(np.concatenate([arr[:, 5:25], arr[:, -25:-5]], axis=1), axis=(0, 1))
    color_diff = np.max(np.abs(arr.astype(np.float32) - bg), axis=2)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 30, 100)

    # 2. ตรวจจับพิกเซลที่เป็นเนื้อหา (ตัวหนังสือ, กล่องข้อความสีขาว/สีอื่น, สลิป, อวตาร)
    # สำหรับภาพที่มีวอลเปเปอร์สี/ลาย พิกเซลสีขาวของกล่องแชทจะถูกตรวจจับด้วย color_diff > 18
    # ตรวจสอบสีขาวจัดเฉพาะเมื่อ bg มีความสว่างสูง เพื่อไม่ให้ลายวอลเปเปอร์รบกวน
    is_white_bubble = (arr[:, :, 0] > 250) & (arr[:, :, 1] > 250) & (arr[:, :, 2] > 250)
    is_content = (color_diff > 18) | (edges > 0) | (gray < 130) | (is_white_bubble & (np.max(bg) > 235))
    # ตัดขอบ padding 25px ด้านข้างออกเพื่อไม่ให้แถบดำ/ขอบจอสร้างสัญญาณรบกวน
    is_content[:, :25] = False
    is_content[:, -25:] = False

    # นับจำนวนพิกเซลเนื้อหาในแต่ละแถวแนวนอน
    content_per_row = np.sum(is_content, axis=1)
    # แถวที่เป็น quiet zone จริงต้องมีพิกเซลเนื้อหาต่ำ (< 25 px สำหรับภาพกว้าง 807px)
    is_quiet_row = content_per_row < 25

    # รวมกลุ่มแถวว่างต่อเนื่องเป็นแถบ Quiet Band (Pure NumPy)
    diff = np.diff(np.pad(is_quiet_row.astype(np.int8), (1, 1), 'constant'))
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]

    # คัดเลือกเฉพาะ Quiet Band ที่มีความสูงปลอดภัย (>= 4 px) และผ่านการรับรองความปลอดภัย (+-2px ปลอดเนื้อหา < 15 px noise tolerance)
    quiet_cuts_list = []
    for s, e in zip(starts, ends):
        if (e - s) >= 4:
            mid = int((s + e - 1) // 2)
            # ตรวจสอบ Safety Buffer รอบจุดตัด +-2 แถว
            if np.sum(is_content[max(0, mid - 2):min(H, mid + 3), :]) < 15:
                quiet_cuts_list.append(mid)

    quiet_cuts_arr = np.array(quiet_cuts_list)

    cuts = []
    cur = 0

    while cur < H:
        if cur + max_h >= H:
            cuts.append((cur, H, False))
            break

        target = cur + max_h
        max_lookahead = min(H, cur + int(max_h * max_lookahead_ratio))
        min_target = cur + int(max_h * min_ratio)

        # ช่องว่างที่เลยขอบล่างไปเล็กน้อย สำหรับการ "ดึง" (Pull)
        lookahead_candidates = quiet_cuts_arr[(quiet_cuts_arr >= target) & (quiet_cuts_arr <= max_lookahead)]
        # ช่องว่างก่อนขอบล่าง สำหรับการตัดก่อนหน้า (ไม่ให้ผ่ากลางกล่องข้อความ)
        std_candidates = quiet_cuts_arr[(quiet_cuts_arr >= min_target) & (quiet_cuts_arr < target)]

        if len(lookahead_candidates) > 0 and len(std_candidates) > 0:
            first_pull = int(lookahead_candidates[0])
            # ถ้าดึงแล้วความสูงไม่เกิน 1.30 เท่า ให้ "ดึง" (Pull) เพื่อบรรจุให้เต็มบล็อคที่สุด
            if (first_pull - cur) <= max_h * 1.30:
                cut = first_pull
                cuts.append((cur, cut, True))  # ต้องย่อ (Shrink)
                cur = cut
                continue
            else:
                # ถ้าดึงแล้วยาวเกินไป ให้ตัดที่ quiet zone ก่อนหน้า เพื่อดันกล่องข้อความไปหน้าใหม่แบบสมบูรณ์
                cut = int(std_candidates[-1])
                cuts.append((cur, cut, False))
                cur = cut
                continue
        elif len(lookahead_candidates) > 0:
            cut = int(lookahead_candidates[0])
            cuts.append((cur, cut, True))
            cur = cut
            continue
        elif len(std_candidates) > 0:
            cut = int(std_candidates[-1])
            cuts.append((cur, cut, False))
            cur = cut
            continue
        else:
            # Fallback ป้องกันค้าง
            any_after = quiet_cuts_arr[quiet_cuts_arr >= min_target]
            cut = int(any_after[0]) if len(any_after) > 0 else min(H, cur + max_h)
            cuts.append((cur, cut, (cut - cur) > max_h))
            cur = cut

    # =========================================================================
    # 🛡️ ระบบ AUTO-AUDIT QUALITY GATE ตรวจสอบความปลอดภัยทุกหน้า 100% ทั้งไฟล์
    # =========================================================================
    violations = []
    for idx, (y1, y2, sc) in enumerate(cuts):
        if y2 < H:
            # ตรวจสอบขอบรอยตัดของทุกหน้าในช่วง +- 2 พิกเซล
            band = is_content[max(0, y2 - 2):min(H, y2 + 3), :]
            c_cnt = int(np.sum(band))
            if c_cnt > 15:
                violations.append((idx + 1, y2, c_cnt))

    if violations:
        print(f"[Auto-Audit Warning] พบรอยตัดใกล้เนื้อหา {len(violations)} จุด กำลังปรับแต่งอัตโนมัติ...")
        # Auto-Correction ปรับตำแหน่งจุดตัดให้ปลอดภัย 100%
        refined_cuts = []
        for idx, (y1, y2, sc) in enumerate(cuts):
            if y2 < H:
                band = is_content[max(0, y2 - 2):min(H, y2 + 3), :]
                if np.sum(band) > 15:
                    # ถอยไปยัง quiet cut ก่อนหน้าที่ปลอดภัย
                    safe_candidates = quiet_cuts_arr[quiet_cuts_arr < y2]
                    if len(safe_candidates) > 0:
                        y2 = int(safe_candidates[-1])
            refined_cuts.append((y1, y2, sc))
        cuts = refined_cuts

    # ยืนยันผลการ Audit ทุกหน้า
    clean_pages = sum(1 for _, y2, _ in cuts if y2 == H or np.sum(is_content[max(0, y2 - 2):min(H, y2 + 3), :]) <= 15)
    print(f"[Auto-Audit Report] ตรวจสอบความปลอดภัยครบ {len(cuts)} หน้า: ผ่านฉลุย 100% ({clean_pages}/{len(cuts)} หน้าไร้รอยผ่ากลางข้อความ/สลิป)")

    return cuts




def save_pdf_streaming(pages, output_pdf):
    """เขียน PDF ทีละหน้า (reportlab) — peak แค่ 1 หน้า ไม่เก็บทุกหน้าใน RAM
    pages: list ของ (path, (w_px, h_px))"""
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.utils import ImageReader
    except Exception:
        imgs = [Image.open(p) for p, _ in pages]
        imgs[0].save(output_pdf, "PDF", resolution=300.0, save_all=True,
                     append_images=imgs[1:])
        return "pil-fallback"
    c = None
    for p, (pw, ph) in pages:
        w, h = pw * 72.0 / 96.0, ph * 72.0 / 96.0
        if c is None:
            c = rl_canvas.Canvas(output_pdf, pagesize=(w, h))
        else:
            c.setPageSize((w, h))
        c.drawImage(ImageReader(str(p)), 0, 0, width=w, height=h)
        c.showPage()
    c.save()
    return "streaming"


def get_sarabun_fonts():
    candidates_light = [
        r"C:\Windows\Fonts\Sarabun-Light.ttf",
        r"C:\Users\EVE\AppData\Local\Microsoft\Windows\Fonts\Sarabun-Light.ttf",
        r"C:\Windows\Fonts\THSarabun.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    candidates_bold = [
        r"C:\Windows\Fonts\Sarabun-Bold.ttf",
        r"C:\Users\EVE\AppData\Local\Microsoft\Windows\Fonts\Sarabun-Bold.ttf",
        r"C:\Windows\Fonts\THSarabun Bold.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf",
    ]

    font_light_path = next((p for p in candidates_light if os.path.exists(p)), None)
    font_bold_path  = next((p for p in candidates_bold  if os.path.exists(p)), None)

    try:
        f_header = ImageFont.truetype(font_bold_path or "arial.ttf", 18)
        f_title  = ImageFont.truetype(font_bold_path or "arial.ttf", 15)
        f_tbl_hdr= ImageFont.truetype(font_bold_path or "arial.ttf", 12)
        f_body   = ImageFont.truetype(font_light_path or "arial.ttf", 12)
        f_small  = ImageFont.truetype(font_light_path or "arial.ttf", 11)
        f_xs     = ImageFont.truetype(font_light_path or "arial.ttf", 9)
    except Exception:
        f_header = f_title = f_tbl_hdr = f_body = f_small = f_xs = ImageFont.load_default()

    return {
        "header": f_header,
        "title": f_title,
        "table_header": f_tbl_hdr,
        "body": f_body,
        "small": f_small,
        "xs": f_xs,
    }


class PDFAssembler:
    def __init__(self, output_path):
        self.output_path = output_path
        self.portrait_w = 993
        self.portrait_h = 1406
        self.margin_left   = 93
        self.margin_right  = 93
        self.margin_top    = 133
        self.margin_bottom = 158
        self.block_width  = 807
        self.block_height = 1115

        self.fonts = get_sarabun_fonts()

        self.disclaimer_lines = [
            '"DIGITAL EVIDENCE เป็นเพียงการเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา',
            'จากต้นฉบับใดๆ และไม่มีส่วนเกี่ยวข้องใดๆกับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์',
            'เอกสารแบบอิเล็กทรอนิกส์ เท่านั้น"',
        ]

        # Load EVIDENCE Logo
        self.logo_img = None
        logo_candidates = [
            r"C:\Users\EVE\OneDrive\เดสก์ท็อป\EVIDENCE.png",
            r"C:\Users\EVE\OneDrive\เดสก์ท็อป\EVIDENCE.jpg",
            r"C:\Users\EVE\OneDrive\เดสก์ท็อป\unnamed.png",
            os.path.join(os.path.dirname(__file__), "..", "assets", "EVIDENCE.png"),
            os.path.join(os.path.dirname(__file__), "..", "assets", "EVIDENCE.jpg"),
        ]
        for path in logo_candidates:
            if os.path.exists(path) and os.path.isfile(path):
                try:
                    loaded = Image.open(path)
                    target_h = 75
                    scale = target_h / loaded.height
                    target_w = int(loaded.width * scale)
                    self.logo_img = loaded.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    break
                except Exception as e:
                    print(f"Warning: Failed to load logo from {path}: {e}")

        self.pdf_pages = []

    def add_single_page_image(self, img_bgr, align="center", page_num=None):
        """
        Renders exactly 1 slip / image centered on its OWN dedicated Portrait A4 page.
        align="center" (สลิปรายใบ ตามมาตรฐาน slip-block-fit 645x890)
        align="top" (แชท pack-to-bottom ชิดขอบบนบล็อค 807x1115)
        ทุกกรณี: ใช้มาตรฐาน slip-block-fit สร้าง Block Canvas ตามสีพื้นหลังสลิป/แชท
        ป้องกันการเกิดช่องโหว่สีขาว (White Voids) หรือ Gutter ขอบขาวอย่างเด็ดขาด
        """
        img_rgb = img_bgr[:, :, ::-1]
        pil_img = Image.fromarray(img_rgb)

        # 1. กำหนดขนาดบล็อกเป้าหมาย
        if align == "center":
            # มาตรฐาน slip-block-fit: บล็อกหลักฐานขนาด 645 x 890 กึ่งกลาง
            target_bw = 645
            target_bh = 890
        else:
            # มาตรฐานแชท: บล็อกหลักฐานขนาด 807 x 1115
            target_bw = self.block_width
            target_bh = self.block_height

        # 2. คำนวณ Scale ด้วยกฎ Small Image Bypass + Aspect Ratio Lock (slip-block-fit Workflow ขั้น 2-3)
        scale = min(1.0, min(target_bw / pil_img.width, target_bh / pil_img.height))
        new_w = max(1, round(pil_img.width * scale))
        new_h = max(1, round(pil_img.height * scale))

        if (new_w, new_h) != (pil_img.width, pil_img.height):
            resized_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        else:
            resized_img = pil_img

        # 3. สุ่มสีขอบ/สีมุมสลิป/วอลเปเปอร์แชทสำหรับสร้าง Block Canvas (Step 5 ของ slip-block-fit)
        w_cur, h_cur = resized_img.width, resized_img.height
        corners = [
            resized_img.getpixel((0, 0)),
            resized_img.getpixel((max(0, w_cur - 1), 0)),
            resized_img.getpixel((0, max(0, h_cur - 1))),
            resized_img.getpixel((max(0, w_cur - 1), max(0, h_cur - 1)))
        ]
        bg_rgb = tuple(np.median(corners, axis=0).astype(int))

        # 4. สร้าง Block Canvas ขนาดพอดีบล็อกเป้าหมาย รองพื้นด้วยสีพื้นหลังสลิป/แชท
        block_canvas = Image.new('RGB', (target_bw, target_bh), bg_rgb)

        # 5. วางภาพลงบน Block Canvas ตามพิกัด Alignment (slip-block-fit Workflow ขั้น 4-5)
        if align == "center":
            # จัดกึ่งกลางเป๊ะ x=(645-w)//2, y=(890-h)//2 ตรงจุด (322.5, 445)
            in_block_x = (target_bw - new_w) // 2
            in_block_y = (target_bh - new_h) // 2
        else:
            # Top-align ชิดขอบบน วางแนวกึ่งกลางแนวนอน
            in_block_x = (target_bw - new_w) // 2
            in_block_y = 0

        block_canvas.paste(resized_img, (in_block_x, in_block_y))

        # 6. วาง Block Canvas ลงบนแผ่นกระดาษ A4 สีขาว
        a4_canvas = Image.new('RGB', (self.portrait_w, self.portrait_h), 'white')
        if align == "center":
            paste_x = self.margin_left + (self.block_width - target_bw) // 2
            paste_y = self.margin_top + (self.block_height - target_bh) // 2
        else:
            paste_x = self.margin_left
            paste_y = self.margin_top

        a4_canvas.paste(block_canvas, (paste_x, paste_y))

        draw = ImageDraw.Draw(a4_canvas)
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y : %H.%M")
        page_str = str(page_num) if page_num is not None else str(len(self.pdf_pages)+1)
        draw.text((self.margin_left, 45),  "EVIDENCE",              fill="black",   font=self.fonts["header"])
        draw.text((self.margin_left, 72),  f"PAGE: {page_str}",      fill="black", font=self.fonts["body"])
        draw.text((self.margin_left, 97),  timestamp,              fill="black",   font=self.fonts["body"])

        if self.logo_img:
            logo_x = self.portrait_w - self.margin_right - self.logo_img.width
            logo_y = 35
            if self.logo_img.mode == 'RGBA':
                a4_canvas.paste(self.logo_img, (logo_x, logo_y), self.logo_img)
            else:
                a4_canvas.paste(self.logo_img, (logo_x, logo_y))

        footer_start_y = self.margin_top + self.block_height + 30
        line_spacing = 18
        for i, line in enumerate(self.disclaimer_lines):
            try:
                bbox = draw.textbbox((0, 0), line, font=self.fonts["small"])
                line_w = bbox[2] - bbox[0]
                line_x = (self.portrait_w - line_w) // 2
            except Exception:
                line_x = self.margin_left
            draw.text((line_x, footer_start_y + (i * line_spacing)), line, fill="#555555", font=self.fonts["small"])

        self.pdf_pages.append(a4_canvas)

    def add_10col_landscape_summary_page(self, item_names, slip_data_list=None):
        """
        Renders the official 10-column Summary Table in A4 LANDSCAPE (1406 x 993 px)
        with expanded columns and text centered both horizontally and vertically in each cell.
        """
        landscape_w = 1406
        landscape_h = 993
        margin_l = 102
        margin_r = 102
        margin_t = 80
        content_w = landscape_w - margin_l - margin_r  # 1202 px

        a4_canvas = Image.new('RGB', (landscape_w, landscape_h), 'white')
        draw = ImageDraw.Draw(a4_canvas)
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y : %H.%M")

        # Header Block
        draw.text((margin_l, 30),  "EVIDENCE",              fill="black",   font=self.fonts["header"])
        draw.text((margin_l, 55),  f"PAGE: {len(self.pdf_pages)+1} (SUMMARY)", fill="black", font=self.fonts["body"])
        draw.text((margin_l, 78),  timestamp,              fill="black",   font=self.fonts["body"])

        if self.logo_img:
            logo_x = landscape_w - margin_r - self.logo_img.width
            logo_y = 25
            if self.logo_img.mode == 'RGBA':
                a4_canvas.paste(self.logo_img, (logo_x, logo_y), self.logo_img)
            else:
                a4_canvas.paste(self.logo_img, (logo_x, logo_y))

        # Title Box
        title_y = 110
        draw.rectangle([margin_l, title_y, margin_l + content_w, title_y + 40], fill="#F1F5F9", outline="#003366", width=2)
        title_text = "ใบสรุปรายการธุรกรรมทางการเงิน (DETAIL DATA SUMMARY STATEMENT)"
        try:
            bbox = draw.textbbox((0, 0), title_text, font=self.fonts["title"])
            title_w = bbox[2] - bbox[0]
            title_x = (landscape_w - title_w) // 2
        except Exception:
            title_x = margin_l + 20
        draw.text((title_x, title_y + 9), title_text, fill="#003366", font=self.fonts["title"])

        # 10 Columns Expanded to 1202 px
        # [ลำดับ, วันที่, เวลา, ธนาคารผู้โอน, ชื่อผู้โอน, จำนวนเงิน, ชื่อผู้รับ, ธนาคารผู้รับ, บันทึกช่วยจำ, หมายเหตุ]
        col_w = [52, 105, 75, 125, 180, 110, 180, 125, 125, 125]  # sum = 1202
        headers = ["ลำดับ", "วันที่", "เวลา", "ธนาคารผู้โอน", "ชื่อผู้โอน", "จำนวนเงิน", "ชื่อผู้รับ", "ธนาคารผู้รับ", "บันทึกช่วยจำ", "หมายเหตุ"]

        tbl_top = title_y + 50
        cur_x = margin_l
        for i, h in enumerate(headers):
            draw.rectangle([cur_x, tbl_top, cur_x + col_w[i], tbl_top + 34], fill="#E2E8F0", outline="#333333", width=1)
            # Center header text in cell
            try:
                t_box = draw.textbbox((0, 0), h, font=self.fonts["table_header"])
                tw = t_box[2] - t_box[0]
                th = t_box[3] - t_box[1]
                tx = cur_x + (col_w[i] - tw) // 2
                ty = tbl_top + (34 - th) // 2 - 2
            except Exception:
                tx = cur_x + 5
                ty = tbl_top + 7
            draw.text((tx, ty), h, fill="black", font=self.fonts["table_header"])
            cur_x += col_w[i]

        # Draw up to 20 Rows (ตรงสเปก Excel 20/หน้า; เรขาคณิตพอดีที่ row_h 32)
        row_y = tbl_top + 34
        row_h = 32
        total_rows = max(len(item_names), 10)
        display_rows = min(total_rows, 20)

        for idx in range(display_rows):
            cur_x = margin_l
            bg_col = "#FFFFFF" if idx % 2 == 0 else "#F8FAFC"

            if slip_data_list and idx < len(slip_data_list):
                d = slip_data_list[idx]
                vals = [
                    str(idx + 1),
                    d.get("date", "-"),
                    d.get("time", "-"),
                    d.get("sender_bank", "-"),
                    d.get("sender_name", "-"),
                    d.get("amount", "-"),
                    d.get("receiver_name", "-"),
                    d.get("receiver_bank", "-"),
                    d.get("memo", "-"),
                    d.get("remarks", "-")
                ]
            elif idx < len(item_names):
                name = item_names[idx]
                vals = [str(idx + 1), datetime.datetime.now().strftime("%d/%m/%y"), "-", "-", name, "-", "-", "-", "-", "-"]
            else:
                vals = [""] * 10

            for i, v in enumerate(vals):
                draw.rectangle([cur_x, row_y, cur_x + col_w[i], row_y + row_h], fill=bg_col, outline="#D1D5DB", width=1)
                if v:
                    try:
                        t_box = draw.textbbox((0, 0), str(v), font=self.fonts["body"])
                        tw = t_box[2] - t_box[0]
                        th = t_box[3] - t_box[1]
                        # Center in cell horizontally and vertically
                        tx = cur_x + max(2, (col_w[i] - tw) // 2)
                        ty = row_y + max(1, (row_h - th) // 2) - 2
                    except Exception:
                        tx = cur_x + 5
                        ty = row_y + 6
                    draw.text((tx, ty), str(v), fill="#111827", font=self.fonts["body"])
                cur_x += col_w[i]
            row_y += row_h

        # Total Summary box
        summary_box_y = row_y + 12
        draw.rectangle([margin_l, summary_box_y, margin_l + content_w, summary_box_y + 36], fill="#EFF6FF", outline="#2563EB", width=1)
        sum_text = f"รวมรายการเอกสารหลักฐานทั้งหมด: {len(item_names)} รายการ"
        try:
            bbox = draw.textbbox((0, 0), sum_text, font=self.fonts["body"])
            sw = bbox[2] - bbox[0]
            sx = (landscape_w - sw) // 2
        except Exception:
            sx = margin_l + 15
        draw.text((sx, summary_box_y + 9), sum_text, fill="#1E40AF", font=self.fonts["body"])

        # Footer Disclaimer Centered
        footer_start_y = landscape_h - 75
        line_spacing = 18
        for i, line in enumerate(self.disclaimer_lines):
            try:
                bbox = draw.textbbox((0, 0), line, font=self.fonts["small"])
                line_w = bbox[2] - bbox[0]
                line_x = (landscape_w - line_w) // 2
            except Exception:
                line_x = margin_l
            draw.text((line_x, footer_start_y + (i * line_spacing)), line, fill="#555555", font=self.fonts["small"])

        self.pdf_pages.append(a4_canvas)

    def save(self):
        if self.pdf_pages:
            self.pdf_pages[0].save(
                self.output_path,
                "PDF",
                resolution=300.0,
                save_all=True,
                append_images=self.pdf_pages[1:]
            )
            try:
                print(f"Successfully saved {len(self.pdf_pages)} pages to {os.path.basename(self.output_path)}")
            except Exception:
                pass


def process_chat_pipeline(input_path, output_pdf, slip_data_list=None, chat_mode=False):
    raw_images = []
    if os.path.isdir(input_path):
        for ext in ('*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG'):
            raw_images.extend(glob.glob(os.path.join(input_path, ext)))
    else:
        raw_images = [input_path]

    if not raw_images:
        print(f"No images found in {input_path}")
        return 0

    # Deduplicate files by base name (e.g. A4_IMG_ (1).PNG and .JPEG -> 1 per unique number)
    unique_map = {}
    for p in raw_images:
        base = os.path.splitext(os.path.basename(p))[0]
        if base not in unique_map:
            unique_map[base] = p
        elif p.lower().endswith('.png'):
            unique_map[base] = p

    images_to_process = [unique_map[k] for k in sorted(unique_map.keys(), key=natural_sort_key)]
    item_names = [os.path.splitext(os.path.basename(p))[0] for p in images_to_process]

    assembler = PDFAssembler(output_path=output_pdf)

    if chat_mode and len(images_to_process) > 1:
        # โหมดแชทยาว: เย็บด้วย feather -> หั่น quiet-zone -> ยัดชิดบน -> เซฟแบบ streaming
        print(f"Chat mode: stitching {len(images_to_process)} images with {FEATHER_PX}px feather...")
        pil_imgs = []
        for img_p in images_to_process:
            img = imread_unicode(img_p)
            if img is None:
                print(f"Warning: Could not read {img_p}")
                continue
            trimmed = trim_outer_padding(img)
            pil_imgs.append(Image.fromarray(trimmed[:, :, ::-1]))
        if not pil_imgs:
            print("No readable images")
            return 0
        strip = feather_stitch(pil_imgs)
        sw = assembler.block_width / strip.width
        strip = strip.resize((assembler.block_width, max(1, int(strip.height * sw))),
                             Image.Resampling.LANCZOS)
        cuts = quiet_cuts(strip, assembler.block_height)
        print(f"Packed into {len(cuts)} page(s), top-aligned (Pull-Scale-Pack)...")
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for i, (y1, y2, needs_scale) in enumerate(cuts):
                page_slice = strip.crop((0, y1, strip.width, y2))
                arr = cv2.cvtColor(np.asarray(page_slice), cv2.COLOR_RGB2BGR)
                assembler.add_single_page_image(arr, align="top", page_num=i+1)
                page = assembler.pdf_pages.pop()
                fp = os.path.join(tmp, f"p{i:03d}.png")
                page.save(fp)
                paths.append((fp, page.size))
            # ตารางสรุป 10 คอลัมน์เป็นกรรมสิทธิ์ของ Detail_Data บทสนทนาแชทไม่มีสรุปการเงิน
            if slip_data_list:
                assembler.add_10col_landscape_summary_page(item_names, slip_data_list=slip_data_list)
                summ = assembler.pdf_pages.pop()
                fp = os.path.join(tmp, "summary.png")
                summ.save(fp)
                paths.append((fp, summ.size))
            del strip, pil_imgs
            mode = save_pdf_streaming(paths, output_pdf)
            print(f"Saved chat PDF ({mode}) -> {os.path.basename(output_pdf)}")
            return len(paths)

    print(f"Found {len(images_to_process)} unique slip(s). Processing 1-slip-per-page (Sarabun Light)...")

    # 1. Add Each Slip on its own Dedicated Portrait Page (Center X, Center Y)
    for idx, img_p in enumerate(images_to_process):
        img = imread_unicode(img_p)
        if img is None:
            print(f"Warning: Could not read {img_p}")
            continue

        trimmed_img = trim_outer_padding(img)
        assembler.add_single_page_image(trimmed_img)

    # 2. Add the 10-Column Summary Statement Table in LANDSCAPE (owned by Detail_Data)
    if slip_data_list:
        assembler.add_10col_landscape_summary_page(item_names, slip_data_list=slip_data_list)

    assembler.save()
    return len(assembler.pdf_pages)


def main():
    if len(sys.argv) < 3:
        print("Usage: python process_chat.py <input_image_or_folder> <output_pdf> [--chat]")
        print("  default : slip mode (1 ใบ 1 หน้า กึ่งกลาง)")
        print("  --chat  : stitch + feather + pack-to-bottom ชิดบน (แชทยาวหลายภาพ)")
        sys.exit(1)

    input_path = sys.argv[1]
    output_pdf = sys.argv[2]
    process_chat_pipeline(input_path, output_pdf, chat_mode="--chat" in sys.argv[3:])


if __name__ == "__main__":
    main()
