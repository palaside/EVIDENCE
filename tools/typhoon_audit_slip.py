#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools/typhoon_audit_slip.py — OpenTyphoon Forensic Slip Audit & Correction Tool
Usage:
  py tools/typhoon_audit_slip.py <image_path>
  py tools/typhoon_audit_slip.py --page <page_num> [--pdf <master_pdf_path>]
"""

import os
import sys
import json
import argparse
import fitz

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "_skills", "OCR_Slip", "scripts"))

from typhoon_slip_engine import extract_slip_with_typhoon, load_typhoon_api_key

try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

OUT_DIR = os.path.join(PROJECT_ROOT, "Folder_Out")
AUDIT_LOG = os.path.join(OUT_DIR, "TYPHOON_AUDIT_REPORT.json")


def audit_slip_image(image_path: str):
    print("=" * 75)
    print(f" 🌪️ OPENTYPHOON FORENSIC AUDIT: {os.path.basename(image_path)}")
    print("=" * 75)

    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return None

    api_key = load_typhoon_api_key()
    if not api_key:
        print("❌ Error: TYPHOON_API_KEY is not set in .env or environment.")
        return None

    print("⏳ Running Stage 1 (typhoon-ocr-v1.5) & Stage 2 (typhoon-v2.5-30b-a3b)...")
    res = extract_slip_with_typhoon(image_path)
    if not res:
        print("❌ Failed to extract data from Typhoon API.")
        return None

    print("\n✅ AUDIT RESULTS (10-Column Standard):")
    print(f"  • จำนวนเงิน (Amount):          {res.get('amount', '-')}")
    print(f"  • วันที่ (Date):               {res.get('date', '-')}")
    print(f"  • เวลา (Time):               {res.get('time', '-')}")
    print(f"  • ธนาคารผู้โอน (Sender Bank):   {res.get('sender_bank', '-')}")
    print(f"  • ชื่อผู้โอน (Sender Name):     {res.get('sender_name', '-')}")
    print(f"  • ธนาคารผู้รับ (Receiver Bank): {res.get('receiver_bank', '-')}")
    print(f"  • ชื่อผู้รับ (Receiver Name):   {res.get('receiver_name', '-')}")
    print(f"  • รหัสอ้างอิง (Remarks/Ref):    {res.get('remarks', '-')}")
    print(f"  • บันทึกช่วยจำ (Memo):         {res.get('memo', '-')}")

    # Append to report
    os.makedirs(OUT_DIR, exist_ok=True)
    report_data = []
    if os.path.exists(AUDIT_LOG):
        try:
            with open(AUDIT_LOG, "r", encoding="utf-8") as f:
                report_data = json.load(f)
        except Exception:
            report_data = []

    res["file"] = os.path.basename(image_path)
    report_data.append(res)
    with open(AUDIT_LOG, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 75)
    print(f"💾 Saved audit record to: {os.path.relpath(AUDIT_LOG, PROJECT_ROOT)}")
    print("=" * 75)
    return res


def audit_pdf_page(page_num: int, pdf_path: str = None):
    if not pdf_path:
        pdf_path = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3.pdf")

    print(f"📄 Extracting Page {page_num} from {os.path.basename(pdf_path)}...")
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return None

    doc = fitz.open(pdf_path)
    if page_num < 1 or page_num > len(doc):
        print(f"❌ Invalid page number. Document has {len(doc)} pages.")
        doc.close()
        return None

    page = doc[page_num - 1]
    pix = page.get_pixmap(dpi=200)
    temp_img = os.path.join(OUT_DIR, f"temp_audit_page_{page_num}.png")
    pix.save(temp_img)
    doc.close()

    result = audit_slip_image(temp_img)
    if os.path.exists(temp_img):
        try:
            os.remove(temp_img)
        except Exception:
            pass
    return result


def main():
    parser = argparse.ArgumentParser(description="OpenTyphoon Forensic Slip Audit & Correction Tool")
    parser.add_argument("image", nargs="?", help="Path to slip image")
    parser.add_argument("--page", type=int, help="Page number from Master PDF")
    parser.add_argument("--pdf", help="Custom PDF path if auditing by page")
    args = parser.parse_args()

    if args.page:
        audit_pdf_page(args.page, args.pdf)
    elif args.image:
        audit_slip_image(args.image)
    else:
        # Default test against perfect_page_slip_13.png
        default_test = os.path.join(PROJECT_ROOT, "perfect_page_slip_13.png")
        if os.path.exists(default_test):
            audit_slip_image(default_test)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
