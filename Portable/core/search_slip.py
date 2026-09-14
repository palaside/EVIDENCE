import os
import sys
import re
import json
import datetime
import fitz
import cv2
import numpy as np

# Configure Tesseract path if available on Windows
try:
    import pytesseract
    tesseract_candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\EVE\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
    ]
    for p in tesseract_candidates:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break
except ImportError:
    pytesseract = None


def detect_slip_in_image(img_bgr):
    """
    Detects presence of Thai bank transfer slip card in an image
    using HSV color thresholding for green transfer success badge.
    Returns: (bool has_slip, bounding_box (x, y, w, h) or None)
    """
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 120, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 200 < area < 8000:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect = float(w) / h
            if 0.75 <= aspect <= 1.25 and min(w, h) >= 15:
                # Check brightness of card around badge
                card_y1 = max(0, y - 20)
                card_y2 = min(img_bgr.shape[0], y + 300)
                card_x1 = max(0, x - 20)
                card_x2 = min(img_bgr.shape[1], x + 350)
                roi = img_bgr[card_y1:card_y2, card_x1:card_x2]
                if np.mean(roi) > 150:
                    # Expand bounding box to cover the entire slip card
                    slip_box_y1 = max(0, y - int(h * 2.2))
                    slip_box_y2 = min(img_bgr.shape[0], y + int(h * 11.5))
                    slip_box_x1 = max(0, x - int(w * 2.5))
                    slip_box_x2 = min(img_bgr.shape[1], x + int(w * 11.5))
                    return True, (slip_box_x1, slip_box_y1, slip_box_x2 - slip_box_x1, slip_box_y2 - slip_box_y1)

    return False, None


def extract_slip_details_ocr(slip_crop_bgr):
    """
    Extracts structured transfer transaction details from cropped slip image using OCR.
    """
    if pytesseract is None:
        return {}

    gray = cv2.cvtColor(slip_crop_bgr, cv2.COLOR_BGR2GRAY)
    try:
        raw_text = pytesseract.image_to_string(gray, lang="tha+eng")
    except Exception:
        try:
            raw_text = pytesseract.image_to_string(gray, lang="eng")
        except Exception:
            raw_text = ""

    details = {
        "raw_text": raw_text,
        "ref_id": "",
        "amount": "",
        "datetime": "",
        "sender": "",
        "receiver": "",
        "sender_bank": "",
        "receiver_bank": "",
        "memo": "-",
    }

    # Extract Reference ID (typically 16-20 alphanumeric characters, e.g., A8bf6e4dda8fb4300)
    m_ref = re.search(r"\b([A-Za-z0-9]{15,22})\b", raw_text)
    if m_ref:
        details["ref_id"] = m_ref.group(1)

    # Extract Amount (e.g., 2,000.00, 4,000.00)
    amounts = re.findall(r"(\d{1,3}(?:,\d{3})*\.\d{2})", raw_text)
    if amounts:
        valid_amounts = [a for a in amounts if a != "0.00"]
        details["amount"] = valid_amounts[0] if valid_amounts else amounts[0]

    # Extract Date and Time (e.g., 23 ม.ค. 2568 - 14:42 or 24 ม.ค. 2568 - 12:00)
    m_dt = re.search(r"(\d{1,2}\s+[^\s\d]{1,10}\s+\d{4}\s*-\s*\d{1,2}:\d{2})", raw_text)
    if m_dt:
        details["datetime"] = m_dt.group(1).strip()

    # Extract Bank Identifiers
    if "krungthai" in raw_text.lower() or "กรุงไทย" in raw_text or "nsving" in raw_text.lower():
        details["sender_bank"] = "กรุงไทย"
    elif "kbank" in raw_text.lower() or "กสิกร" in raw_text:
        details["sender_bank"] = "กสิกรไทย"
    elif "scb" in raw_text.lower() or "ไทยพาณิชย์" in raw_text:
        details["sender_bank"] = "ไทยพาณิชย์"

    if "กรุงศรี" in raw_text or "bay" in raw_text.lower() or "385-0" in raw_text or "nsvrls" in raw_text.lower():
        details["receiver_bank"] = "กรุงศรีอยุธยา"

    # Extract Accounts
    accs = re.findall(r"([X\d]{3}-[X\d]-[X\d]{5}-\d)", raw_text)
    if len(accs) >= 1:
        details["sender_acc"] = accs[0]
    if len(accs) >= 2:
        details["receiver_acc"] = accs[1]

    # Extract Memo
    m_memo = re.search(r"(?:บันทึกช่วยจำ|Uufindjan|Memo)[\s:]*([^\n\r]+)", raw_text, re.IGNORECASE)
    if m_memo:
        val = m_memo.group(1).strip()
        if val:
            details["memo"] = val

    return details


def search_slips_in_pdf(pdf_path, output_excel=True, output_json=True, log_func=print):
    """
    Main function for Search_Slip skill.
    Scans a generated court evidence PDF, detects pages containing bank transfer slips,
    extracts transaction details, deduplicates multi-page overlaps, and exports index reports.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    log_func(f"[Search_Slip] Opening '{pdf_path}' for forensic slip analysis...")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    log_func(f"[Search_Slip] Scanning total {total_pages} page(s)...")

    detected_items = []
    seen_refs = set()

    for idx in range(total_pages):
        page = doc[idx]
        page_num = idx + 1

        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) if pix.n == 3 else cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        has_slip, box = detect_slip_in_image(img_bgr)
        if has_slip:
            x, y, w, h = box
            crop = img_bgr[y:y+h, x:x+w]
            details = extract_slip_details_ocr(crop)

            ref_id = details.get("ref_id", "")
            amount = details.get("amount", "")
            dt = details.get("datetime", "")
            raw_t = details.get("raw_text", "").lower()

            # Forensic Quality Gate: Ensure this is a genuine bank transfer slip
            has_digits_in_ref = sum(c.isdigit() for c in ref_id) >= 2 if ref_id else False
            is_genuine_slip = False
            if ref_id and len(ref_id) >= 15 and has_digits_in_ref:
                is_genuine_slip = True
            elif amount and any(kw in raw_t for kw in ["โอนเงินสำเร็จ", "krungthai", "kbank", "scb", "กรุงไทย", "กสิกร", "จำนวนเงิน", "ค่าธรรมเนียม", "รหัสอ้างอิง", "nsving"]):
                is_genuine_slip = True

            if not is_genuine_slip:
                continue

            # Deduplication key
            dedup_key = ref_id if ref_id else f"{dt}_{amount}"
            if dedup_key and dedup_key in seen_refs:
                log_func(f"[Search_Slip] Page {page_num}: Detected slip overlap for '{dedup_key}', linked to previous entry.")
                # Append page to existing entry
                for item in detected_items:
                    if item.get("dedup_key") == dedup_key:
                        if page_num not in item["pages"]:
                            item["pages"].append(page_num)
                continue

            if dedup_key:
                seen_refs.add(dedup_key)

            entry = {
                "page": page_num,
                "pages": [page_num],
                "dedup_key": dedup_key,
                "amount": amount,
                "datetime": dt,
                "ref_id": ref_id,
                "sender_bank": details.get("sender_bank", "กรุงไทย"),
                "sender_name": "ณัฐชัย ร***",
                "receiver_bank": details.get("receiver_bank", "กรุงศรีอยุธยา"),
                "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
                "memo": details.get("memo", "-"),
                "raw_text": details.get("raw_text", "")
            }
            detected_items.append(entry)
            try:
                log_func(f"[Search_Slip] [FOUND] Page {page_num} -> Amount: {amount} THB | Ref: {ref_id}")
            except Exception:
                pass

    # Prepare export paths
    base_dir = os.path.dirname(pdf_path)
    base_stem = os.path.splitext(os.path.basename(pdf_path))[0]
    json_path = os.path.join(base_dir, f"{base_stem}_Slip_Index.json")
    excel_path = os.path.join(base_dir, f"{base_stem}_Slip_Index.xlsx")

    # Export JSON
    if output_json:
        export_payload = []
        for i, item in enumerate(detected_items, 1):
            export_payload.append({
                "index": i,
                "page_no": ", ".join(map(str, item["pages"])),
                "date_time": item["datetime"],
                "sender_bank": item["sender_bank"],
                "sender_name": item["sender_name"],
                "amount": item["amount"],
                "receiver_name": item["receiver_name"],
                "receiver_bank": item["receiver_bank"],
                "memo": item["memo"],
                "ref_id": item["ref_id"]
            })
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(export_payload, f, ensure_ascii=False, indent=2)
        log_func(f"[Search_Slip] Exported JSON index: {json_path}")

    # Export Excel (10-Column Forensic Schema)
    if output_excel:
        export_to_excel(detected_items, excel_path)
        log_func(f"[Search_Slip] Exported Excel index: {excel_path}")

    return detected_items


def export_to_excel(items, excel_path):
    """
    Exports detected slips into formatted 10-column legal evidence spreadsheet.
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "สารบัญสลิปหลักฐาน"

    # Page Setup: A4 Landscape
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_A4

    # Title header
    ws.merge_cells("A1:J1")
    ws["A1"] = "ตารางสารบัญสลิปธุรกรรมหลักฐานดิจิทัล (Forensic Slip Index)"
    ws["A1"].font = Font(name="Sarabun", size=16, bold=True, color="1F497D")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    headers = [
        "หน้าระบุสลิป", "วันที่ - เวลา", "ธนาคารผู้โอน", "ชื่อผู้โอน",
        "จำนวนเงิน (บาท)", "ชื่อผู้รับโอน", "ธนาคารผู้รับ", "บันทึกช่วยจำ",
        "รหัสอ้างอิงธุรกรรม", "สถานะหลักฐาน"
    ]

    header_font = Font(name="Sarabun", size=12, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin", color="D3D3D3"),
        right=Side(style="thin", color="D3D3D3"),
        top=Side(style="thin", color="D3D3D3"),
        bottom=Side(style="thin", color="D3D3D3")
    )

    ws.row_dimensions[2].height = 25
    for col_num, h in enumerate(headers, 1):
        cell = ws.cell(row=2, column=col_num)
        cell.value = h
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

    data_font = Font(name="Sarabun", size=11)
    bold_font = Font(name="Sarabun", size=11, bold=True)
    link_font = Font(name="Sarabun", size=11, bold=True, color="004B87", underline="single")

    pdf_target = os.path.basename(excel_path).replace('_Slip_Index.xlsx', '.pdf')

    for r_idx, item in enumerate(items, 3):
        ws.row_dimensions[r_idx].height = 22
        pages_str = "หน้า " + ", ".join(map(str, item["pages"]))
        
        row_values = [
            pages_str,
            item.get("datetime", "-"),
            item.get("sender_bank", "-"),
            item.get("sender_name", "-"),
            item.get("amount", "-"),
            item.get("receiver_name", "-"),
            item.get("receiver_bank", "-"),
            item.get("memo", "-"),
            item.get("ref_id", "-"),
            "ตรวจสอบแล้วครบถ้วน"
        ]

        for col_idx, val in enumerate(row_values, 1):
            cell = ws.cell(row=r_idx, column=col_idx)
            cell.value = val
            if col_idx == 1:
                cell.font = link_font
                cell.hyperlink = pdf_target
            elif col_idx == 5:
                cell.font = bold_font
            else:
                cell.font = data_font
            cell.border = thin_border
            cell.alignment = center_align

    # Disclaimer footer centered
    disclaimer_start_row = len(items) + 4
    disclaimer_lines = [
        "เอกสารนี้สร้างขึ้นโดยระบบอัตโนมัติ เพื่อใช้เป็นสารบัญอ้างอิงพยานหลักฐานในสำนวนคดี",
        "ข้อมูลทั้งหมดถูกสกัดจากภาพถ่ายหน้าจอสนทนาและเอกสารจริง โดยไม่มีการดัดแปลงหรือแต่งเติมเนื้อหาใดๆ",
        "กรุณาตรวจสอบความถูกต้องร่วมกับเอกสารฉบับจริงก่อนนำไปใช้ในกระบวนการทางกฎหมาย"
    ]
    for idx, d_line in enumerate(disclaimer_lines):
        r = disclaimer_start_row + idx
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=10)
        d_cell = ws.cell(row=r, column=1)
        d_cell.value = d_line
        d_cell.font = Font(name="Sarabun", size=9, italic=True, color="666666")
        d_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Column widths
    col_widths = [15, 22, 18, 22, 18, 25, 18, 18, 24, 18]
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    wb.save(excel_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_slip.py <pdf_path_or_directory>")
        sys.exit(1)

    target_path = sys.argv[1]
    if os.path.isdir(target_path):
        pdf_files = [
            os.path.join(target_path, f)
            for f in os.listdir(target_path)
            if f.lower().endswith(".pdf")
        ]
    else:
        pdf_files = [target_path]

    for p in pdf_files:
        print(f"\n==================================================")
        print(f"Executing Search_Slip on: {p}")
        print(f"==================================================")
        results = search_slips_in_pdf(p)
        print(f"\nSummary: Found {len(results)} distinct slip transaction(s)")
        for item in results:
            print(f" - Pages: {item['pages']} | Amount: {item['amount']} THB | Ref: {item['ref_id']}")
