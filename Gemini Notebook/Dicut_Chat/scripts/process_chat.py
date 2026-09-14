import sys
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime
import glob
import re
import json


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

    def add_single_page_image(self, img_bgr):
        """
        Renders exactly 1 slip / image centered on its OWN dedicated Portrait A4 page.
        """
        img_rgb = img_bgr[:, :, ::-1]
        pil_img = Image.fromarray(img_rgb)

        scale_w = self.block_width / pil_img.width
        scale_h = self.block_height / pil_img.height
        scale = min(scale_w, scale_h)

        new_w = max(1, int(pil_img.width * scale))
        new_h = max(1, int(pil_img.height * scale))

        resized_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        a4_canvas = Image.new('RGB', (self.portrait_w, self.portrait_h), 'white')

        paste_x = self.margin_left + (self.block_width - new_w) // 2
        paste_y = self.margin_top + (self.block_height - new_h) // 2

        a4_canvas.paste(resized_img, (paste_x, paste_y))

        draw = ImageDraw.Draw(a4_canvas)
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y : %H.%M")
        draw.text((self.margin_left, 45),  "EVIDENCE",              fill="black",   font=self.fonts["header"])
        draw.text((self.margin_left, 72),  f"PAGE: {len(self.pdf_pages)+1}", fill="black", font=self.fonts["body"])
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

        # Draw up to 20 Rows (Sarabun Light Font, Centered in each cell)
        row_y = tbl_top + 34
        row_h = 32
        total_rows = max(len(item_names), 10)
        display_rows = min(total_rows, 16)

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
        sum_text = f"รวมรายการเอกสารหลักฐานทั้งหมด: {len(item_names)} รายการ | สรุปรายงานทางการเงินด้วยระบบดิจิทัลถูกต้องสมบูรณ์ 100%"
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


def process_chat_pipeline(input_path, output_pdf, slip_data_list=None):
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

    print(f"Found {len(images_to_process)} unique slip(s). Processing 1-slip-per-page (Sarabun Light)...")

    assembler = PDFAssembler(output_path=output_pdf)

    # 1. Add Each Slip on its own Dedicated Portrait Page (Center X, Center Y)
    for idx, img_p in enumerate(images_to_process):
        img = imread_unicode(img_p)
        if img is None:
            print(f"Warning: Could not read {img_p}")
            continue

        trimmed_img = trim_outer_padding(img)
        assembler.add_single_page_image(trimmed_img)

    # 2. Add the 10-Column Summary Statement Table in LANDSCAPE
    assembler.add_10col_landscape_summary_page(item_names, slip_data_list=slip_data_list)

    assembler.save()
    return len(assembler.pdf_pages)


def main():
    if len(sys.argv) < 3:
        print("Usage: python process_chat.py <input_image_or_folder> <output_pdf>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_pdf = sys.argv[2]
    process_chat_pipeline(input_path, output_pdf)


if __name__ == "__main__":
    main()
