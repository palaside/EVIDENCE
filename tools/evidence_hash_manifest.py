#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
🏛️ EVIDENCE HASH MANIFEST & INTEGRITY VERIFICATION ENGINE
👤 ROLE: SENIOR DIGITAL FORENSICS & FULL-STACK DEVELOPER AGENT
📦 PROJECT: DIGITAL_EVIDENCE
⚖️ LEGAL REF: พ.ร.บ. ว่าด้วยธุรกรรมทางอิเล็กทรอนิกส์ พ.ศ. 2544 (มาตรา 26, 28) & ISO/IEC 27037
==============================================================================
"""

import os
import sys
import json
import time
import hashlib
import datetime
from PIL import Image, ImageDraw, ImageFont

# Set UTF-8 encoding for standard output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def calculate_file_hash(file_path, chunk_size=65536):
    """
    Computes SHA-256 and MD5 hashes using chunked binary streaming.
    Memory-efficient for multi-gigabyte files.
    """
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    size_bytes = 0

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            sha256.update(chunk)
            md5.update(chunk)
            size_bytes += len(chunk)

    return {
        "sha256": sha256.hexdigest().lower(),
        "md5": md5.hexdigest().lower(),
        "size_bytes": size_bytes,
        "size_human": format_size(size_bytes)
    }


def format_size(size_bytes):
    """Formats bytes into human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_sarabun_fonts():
    """Load official Thai Sarabun fonts with fallback."""
    font_paths = [
        r"C:\Windows\Fonts\THSarabun.ttf",
        r"C:\Windows\Fonts\THSarabunNew.ttf",
        r"C:\Windows\Fonts\cordia.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    font_bold_paths = [
        r"C:\Windows\Fonts\THSarabun Bold.ttf",
        r"C:\Windows\Fonts\THSarabunNew Bold.ttf",
        r"C:\Windows\Fonts\cordiab.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf",
    ]

    regular_path = next((p for p in font_paths if os.path.exists(p)), None)
    bold_path = next((p for p in font_bold_paths if os.path.exists(p)), None)

    try:
        if regular_path and bold_path:
            return {
                "title": ImageFont.truetype(bold_path, 21),
                "subtitle": ImageFont.truetype(regular_path, 18),
                "header_lbl": ImageFont.truetype(bold_path, 18),
                "header_val": ImageFont.truetype(regular_path, 18),
                "tbl_hdr": ImageFont.truetype(bold_path, 15),
                "tbl_body": ImageFont.truetype(regular_path, 15),
                "tbl_hash": ImageFont.truetype(regular_path, 13),
                "footer": ImageFont.truetype(regular_path, 13),
                "disclaimer": ImageFont.truetype(regular_path, 14),
            }
    except Exception as e:
        print(f"Font loading warning: {e}")

    default = ImageFont.load_default()
    return {k: default for k in [
        "title", "subtitle", "header_lbl", "header_val",
        "tbl_hdr", "tbl_body", "tbl_hash", "footer", "disclaimer"
    ]}


def load_evidence_logo():
    """Load DIGITAL EVIDENCE logo image with transparent background support."""
    search_paths = [
        os.path.join(os.path.dirname(__file__), "..", "Portable", "core", "assets", "EVIDENCE.png"),
        os.path.join(os.path.dirname(__file__), "assets", "EVIDENCE.png"),
        os.path.join(os.path.dirname(__file__), "..", "_skills", "Detail_Data", "assets", "EVIDENCE.png"),
        r"C:\Users\EVE\OneDrive\เดสก์ท็อป\EVIDENCE.png",
    ]
    for p in search_paths:
        if os.path.exists(p):
            try:
                img = Image.open(p)
                max_h = 58
                ratio = max_h / float(img.height)
                new_w = int(img.width * ratio)
                return img.resize((new_w, max_h), Image.Resampling.LANCZOS)
            except Exception:
                pass
    return None


def generate_hash_manifest(target_files, output_dir, project_name="DIGITAL_EVIDENCE", case_title="สำนวนพยานหลักฐานดิจิทัล"):
    """
    Generates:
    1. EVIDENCE_HASH_MANIFEST.json
    2. EVIDENCE_HASH_MANIFEST.sha256
    3. EVIDENCE_HASH_CERTIFICATE.pdf
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n🔐 กำลังคำนวณค่า Cryptographic Hashes (SHA-256) สำหรับ {len(target_files)} ไฟล์...")
    manifest_records = []

    for idx, fpath in enumerate(target_files, 1):
        if not os.path.exists(fpath):
            continue
        fname = os.path.basename(fpath)
        print(f"   [{idx}/{len(target_files)}] กำลังแฮช: {fname}...", end="", flush=True)
        h_info = calculate_file_hash(fpath)
        print(f" -> SHA-256: {h_info['sha256'][:16]}... ({h_info['size_human']})")

        rec = {
            "index": idx,
            "filename": fname,
            "path": os.path.relpath(fpath, output_dir).replace("\\", "/"),
            "size_bytes": h_info["size_bytes"],
            "size_human": h_info["size_human"],
            "sha256": h_info["sha256"],
            "md5": h_info["md5"],
            "verified_at": timestamp
        }
        manifest_records.append(rec)

    # 1. Save JSON Manifest
    json_path = os.path.join(output_dir, "EVIDENCE_HASH_MANIFEST.json")
    manifest_payload = {
        "project": project_name,
        "case_title": case_title,
        "generated_at": timestamp,
        "hash_algorithm": "SHA-256 (Primary), MD5 (Secondary)",
        "legal_compliance": "พ.ร.บ. ว่าด้วยธุรกรรมทางอิเล็กทรอนิกส์ พ.ศ. 2544 มาตรา 26, 28",
        "total_files": len(manifest_records),
        "files": manifest_records
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(manifest_payload, f, ensure_ascii=False, indent=2)
    print(f"✅ บันทึก JSON Manifest: {json_path}")

    # 2. Save .sha256 Checksum File (Standard UNIX/GNU format)
    sha256_path = os.path.join(output_dir, "EVIDENCE_HASH_MANIFEST.sha256")
    with open(sha256_path, "w", encoding="utf-8") as f:
        for rec in manifest_records:
            f.write(f"{rec['sha256']} *{rec['filename']}\n")
    print(f"✅ บันทึก SHA256 Checksum File: {sha256_path}")

    # 3. Generate Forensic PDF Certificate
    cert_pdf_path = os.path.join(output_dir, "EVIDENCE_HASH_CERTIFICATE.pdf")
    generate_hash_certificate_pdf(manifest_payload, cert_pdf_path)
    print(f"✅ สร้างใบรับรองความถูกต้องของพยานหลักฐานอิเล็กทรอนิกส์: {cert_pdf_path}")

    return {
        "json": json_path,
        "sha256": sha256_path,
        "certificate_pdf": cert_pdf_path,
        "total_files": len(manifest_records)
    }


def generate_hash_certificate_pdf(manifest_data, output_pdf_path):
    """
    Renders the official Forensic Certificate of Digital Evidence Integrity in A4 Portrait (807 x 1115 px)
    matching the exact typography and legal aesthetics of DIGITAL EVIDENCE.
    """
    fonts = get_sarabun_fonts()
    logo_img = load_evidence_logo()

    page_w = 807
    page_h = 1115
    margin_x = 45
    margin_y = 40
    content_w = page_w - (margin_x * 2)  # 717 px

    files = manifest_data.get("files", [])
    files_per_page = 7  # 7 files per certificate page with clear hash blocks
    chunks = [files[i:i + files_per_page] for i in range(0, max(len(files), 1), files_per_page)]
    total_pages = len(chunks)

    pdf_pages = []

    for page_idx, chunk in enumerate(chunks):
        canvas = Image.new("RGB", (page_w, page_h), "white")
        draw = ImageDraw.Draw(canvas)

        # Header Evidence Ribbon
        cur_y = margin_y
        if logo_img:
            if logo_img.mode == "RGBA":
                canvas.paste(logo_img, (margin_x, cur_y), logo_img)
            else:
                canvas.paste(logo_img, (margin_x, cur_y))
            hdr_text_x = margin_x + logo_img.width + 16
        else:
            hdr_text_x = margin_x

        line1_y = cur_y + 4
        line2_y = cur_y + 32

        draw.text((hdr_text_x, line1_y), "MODE : ", fill="#111827", font=fonts["header_lbl"])
        b_lbl = draw.textbbox((hdr_text_x, line1_y), "MODE : ", font=fonts["header_lbl"])
        draw.text((b_lbl[2], line1_y), "FORENSIC INTEGRITY HASH", fill="#111827", font=fonts["header_val"])

        draw.text((hdr_text_x, line2_y), "CORROBORATED : ", fill="#111827", font=fonts["header_lbl"])
        b_cor = draw.textbbox((hdr_text_x, line2_y), "CORROBORATED : ", font=fonts["header_lbl"])
        draw.text((b_cor[2], line2_y), "ใบรับรองความถูกต้องตาม พ.ร.บ.ธุรกรรมอิเล็กทรอนิกส์", fill="#111827", font=fonts["header_val"])

        # Page number on right
        page_str = f"{page_idx + 1} / {total_pages}"
        b_pval = draw.textbbox((0, 0), page_str, font=fonts["header_val"])
        b_plbl = draw.textbbox((0, 0), "PAGE : ", font=fonts["header_lbl"])
        total_p_w = (b_plbl[2] - b_plbl[0]) + (b_pval[2] - b_pval[0])
        p_x = page_w - margin_x - total_p_w
        draw.text((p_x, line1_y), "PAGE : ", fill="#111827", font=fonts["header_lbl"])
        b_pr = draw.textbbox((p_x, line1_y), "PAGE : ", font=fonts["header_lbl"])
        draw.text((b_pr[2], line1_y), page_str, fill="#111827", font=fonts["header_val"])

        cur_y += 75

        # Title Block (2 Lines)
        draw.rectangle([margin_x, cur_y, margin_x + content_w, cur_y + 70], fill="#0F172A")
        t_text = "ใบรับรองความถูกต้องของพยานหลักฐานดิจิทัล"
        t_sub = "CERTIFICATE OF DIGITAL EVIDENCE INTEGRITY"
        try:
            tb = draw.textbbox((0, 0), t_text, font=fonts["title"])
            tw = tb[2] - tb[0]
            draw.text((margin_x + (content_w - tw) // 2, cur_y + 10), t_text, fill="#F8FAFC", font=fonts["title"])

            tb_s = draw.textbbox((0, 0), t_sub, font=fonts["tbl_hash"])
            tw_s = tb_s[2] - tb_s[0]
            draw.text((margin_x + (content_w - tw_s) // 2, cur_y + 42), t_sub, fill="#94A3B8", font=fonts["tbl_hash"])
        except Exception:
            draw.text((margin_x + 20, cur_y + 12), t_text, fill="#F8FAFC", font=fonts["title"])

        cur_y += 82

        # Metadata Summary Card
        draw.rectangle([margin_x, cur_y, margin_x + content_w, cur_y + 70], fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((margin_x + 16, cur_y + 8), f"ชื่อชุดสำนวน: {manifest_data.get('case_title')}", fill="#0F172A", font=fonts["header_lbl"])
        draw.text((margin_x + 16, cur_y + 28), f"วัน-เวลาที่ตรวจพิสูจน์ (Timestamp): {manifest_data.get('generated_at')}", fill="#334155", font=fonts["tbl_body"])
        draw.text((margin_x + 16, cur_y + 48), f"มาตรฐานการแฮช: SHA-256 (FIPS 180-4) | กฎหมาย: พ.ร.บ.ธุรกรรมทางอิเล็กทรอนิกส์ พ.ศ. 2544", fill="#334155", font=fonts["tbl_body"])
        
        tot_f = manifest_data.get("total_files", 0)
        draw.text((margin_x + content_w - 180, cur_y + 8), f"จำนวนไฟล์ทั้งหมด: {tot_f} ไฟล์", fill="#0F172A", font=fonts["header_lbl"])

        cur_y += 82

        # Hash Table Header
        tbl_top = cur_y
        col_w = [48, 220, 85, 364]  # Total = 717
        headers = ["ลำดับ", "ชื่อไฟล์หลักฐาน", "ขนาด", "รหัสพิมพ์ลายนิ้วมือดิจิทัล (SHA-256 Checksum)"]

        cx = margin_x
        for i, h in enumerate(headers):
            draw.rectangle([cx, tbl_top, cx + col_w[i], tbl_top + 30], fill="#E2E8F0", outline="#94A3B8", width=1)
            try:
                tb = draw.textbbox((0, 0), h, font=fonts["tbl_hdr"])
                tw = tb[2] - tb[0]
                th = tb[3] - tb[1]
                draw.text((cx + (col_w[i] - tw) // 2, tbl_top + (30 - th) // 2 - 2), h, fill="#0F172A", font=fonts["tbl_hdr"])
            except Exception:
                draw.text((cx + 5, tbl_top + 5), h, fill="#0F172A", font=fonts["tbl_hdr"])
            cx += col_w[i]

        row_y = tbl_top + 30
        row_h = 60  # 2 lines per record for hash readability

        for r_idx, rec in enumerate(chunk):
            bg = "#FFFFFF" if r_idx % 2 == 0 else "#F8FAFC"
            cx = margin_x
            
            # Col 0: Index
            draw.rectangle([cx, row_y, cx + col_w[0], row_y + row_h], fill=bg, outline="#CBD5E1", width=1)
            idx_str = str(rec.get("index", r_idx + 1))
            tb = draw.textbbox((0, 0), idx_str, font=fonts["tbl_body"])
            draw.text((cx + (col_w[0] - (tb[2] - tb[0])) // 2, row_y + (row_h - (tb[3] - tb[1])) // 2), idx_str, fill="#0F172A", font=fonts["tbl_body"])
            cx += col_w[0]

            # Col 1: Filename
            draw.rectangle([cx, row_y, cx + col_w[1], row_y + row_h], fill=bg, outline="#CBD5E1", width=1)
            fn = rec.get("filename", "-")
            # Truncate if too long
            if len(fn) > 28:
                fn_disp = fn[:13] + "..." + fn[-12:]
            else:
                fn_disp = fn
            draw.text((cx + 10, row_y + 18), fn_disp, fill="#0F172A", font=fonts["tbl_body"])
            cx += col_w[1]

            # Col 2: Size
            draw.rectangle([cx, row_y, cx + col_w[2], row_y + row_h], fill=bg, outline="#CBD5E1", width=1)
            sz = rec.get("size_human", "-")
            tb = draw.textbbox((0, 0), sz, font=fonts["tbl_body"])
            draw.text((cx + (col_w[2] - (tb[2] - tb[0])) // 2, row_y + (row_h - (tb[3] - tb[1])) // 2), sz, fill="#334155", font=fonts["tbl_body"])
            cx += col_w[2]

            # Col 3: SHA-256 Hash (Formatted in 2 clean rows)
            draw.rectangle([cx, row_y, cx + col_w[3], row_y + row_h], fill=bg, outline="#CBD5E1", width=1)
            raw_hash = rec.get("sha256", "")
            h_part1 = raw_hash[:32]
            h_part2 = raw_hash[32:]
            draw.text((cx + 14, row_y + 10), h_part1, fill="#0284C7", font=fonts["tbl_hash"])
            draw.text((cx + 14, row_y + 32), h_part2, fill="#0284C7", font=fonts["tbl_hash"])

            row_y += row_h

        # Fill blank rows if last page has fewer records
        blank_needed = files_per_page - len(chunk)
        for b_idx in range(blank_needed):
            cx = margin_x
            bg = "#FFFFFF" if (len(chunk) + b_idx) % 2 == 0 else "#F8FAFC"
            for w in col_w:
                draw.rectangle([cx, row_y, cx + w, row_y + row_h], fill=bg, outline="#CBD5E1", width=1)
                cx += w
            row_y += row_h

        # Legal Certification Affirmation Box
        cert_box_y = row_y + 20
        draw.rectangle([margin_x, cert_box_y, margin_x + content_w, cert_box_y + 115], fill="#FEFCE8", outline="#CA8A04", width=1)
        
        draw.text((margin_x + 16, cert_box_y + 8), "[ ข้อความรับรองความสมบูรณ์ของพยานหลักฐานดิจิทัล (Data Integrity Affirmation) ]", fill="#854D0E", font=fonts["header_lbl"])
        legal_lines = [
            "1. ระบบขอรับรองว่าไฟล์เอกสารและพยานหลักฐานตามบัญชีตารางด้านบน ได้รับการสกัดและคำนวณค่าพิมพ์ลายนิ้วมือดิจิทัล (SHA-256 Hash) โดยตรง",
            "2. ไม่มีการตัดต่อ ดัดแปลง แก้ไข หรือเปลี่ยนแปลงข้อมูลโครงสร้างไบนารีใดๆ ทั้งสิ้น นับแต่วินาทีที่ทำการบันทึกค่าแฮช",
            "3. ค่าตรวจสอบความถูกต้อง (Checksum) นี้ สามารถนำไปใช้พิสูจน์ความคงสภาพ (Chain of Custody) ในชั้นศาลตาม พ.ร.บ. ว่าด้วยธุรกรรมทางอิเล็กทรอนิกส์",
            "   พ.ศ. 2544 (มาตรา 26, 28) และข้อบังคับว่าด้วยการรับฟังพยานหลักฐานอิเล็กทรอนิกส์ได้อย่างสมบูรณ์",
        ]
        for l_idx, line in enumerate(legal_lines):
            draw.text((margin_x + 16, cert_box_y + 32 + (l_idx * 19)), line, fill="#713F12", font=fonts["footer"])

        # Bottom Legal Disclaimer
        disclaimer_lines = [
            '"DIGITAL EVIDENCE เป็นเพียงเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา',
            'จากต้นฉบับใดๆ และไม่มีส่วนเกี่ยวข้องใดๆ กับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์',
            'เอกสารแบบอิเล็กทรอนิกส์ เท่านั้น"',
        ]
        footer_y = page_h - margin_y - 45
        for i, line in enumerate(disclaimer_lines):
            try:
                bbox = draw.textbbox((0, 0), line, font=fonts["footer"])
                lw = bbox[2] - bbox[0]
                lx = (page_w - lw) // 2
            except Exception:
                lx = margin_x
            draw.text((lx, footer_y + (i * 15)), line, fill="#64748B", font=fonts["footer"])

        pdf_pages.append(canvas)

    if pdf_pages:
        pdf_pages[0].save(
            output_pdf_path,
            "PDF",
            resolution=150.0,
            save_all=True,
            append_images=pdf_pages[1:],
        )
        return len(pdf_pages)
    return 0


def main():
    """CLI Entry point."""
    if len(sys.argv) < 2:
        print("Usage: python evidence_hash_manifest.py <file1_or_dir> [file2] [file3] ...")
        sys.exit(1)

    target_paths = []
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Folder_Out"))

    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for root, _, files in os.walk(arg):
                for f in files:
                    if f.lower().endswith(('.pdf', '.xlsx', '.json', '.png', '.jpg', '.jpeg')):
                        target_paths.append(os.path.join(root, f))
        elif os.path.isfile(arg):
            target_paths.append(os.path.abspath(arg))

    if not target_paths:
        print("No valid target files found to hash.")
        sys.exit(1)

    res = generate_hash_manifest(target_paths, out_dir)
    print(f"\n🎉 สำเร็จ! สร้าง Hash Manifest {res['total_files']} ไฟล์ เรียบร้อยแล้ว")


if __name__ == "__main__":
    main()
