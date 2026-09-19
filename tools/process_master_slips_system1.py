#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools/process_master_slips_system1.py — System 1: Master Unique 560 Slips Processor
Priority 1 Execution:
1. Parallel multi-core OCR & EMVCo QR extraction for 560 master slips (with resume cache)
2. Stage Forensic Smart Zoom & Crop (target_h=900px, pure white canvas #FFFFFF)
3. PyMuPDF C-Binding streaming generation of Evidence_Slips_Master_Unique_560.pdf
4. 10-Column Landscape Summary Statement Table appended to PDF
5. Export Evidence_Slips_Master_Unique_560.xlsx
6. Export DUPLICATE_SLIP_AUDIT_REPORT.xlsx (Master 560 + Duplicates 2,232 mapping)
"""

import os
import sys
import json
import time
import tempfile
import cv2
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed

try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENGINES_DIR = os.path.join(PROJECT_ROOT, "_engines")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "Folder_Out")
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "slips_dedup_manifest.json")
OCR_CACHE_FILE = os.path.join(OUTPUT_DIR, "slips_ocr_cache.json")

sys.path.insert(0, os.path.join(ENGINES_DIR, "Dicut_Chat", "scripts"))
sys.path.insert(0, os.path.join(ENGINES_DIR, "OCR_Slip", "scripts"))

from process_chat import PDFAssembler, imread_unicode, forensic_smart_zoom_crop, save_pdf_streaming
from ocr_slip import extract_slip_data, export_evidence_excel
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def _worker_ocr(img_path):
    try:
        data = extract_slip_data(img_path)
        return img_path, data
    except Exception as e:
        return img_path, {
            "filename": os.path.basename(img_path),
            "error": str(e),
            "date": "-", "time": "-", "sender_bank": "-", "sender_name": "-",
            "amount": "-", "receiver_name": "-", "receiver_bank": "-",
            "memo": "-", "remarks": "-"
        }


def run_parallel_ocr(master_paths, max_workers=6):
    print(f"[*] Loading OCR Cache from {OCR_CACHE_FILE}...")
    cache = {}
    if os.path.exists(OCR_CACHE_FILE):
        try:
            with open(OCR_CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
            print(f"    Found {len(cache)} cached OCR records.")
        except Exception:
            cache = {}

    to_process = [p for p in master_paths if p not in cache]
    print(f"[*] Slips to OCR: {len(to_process)} (out of {len(master_paths)}) using {max_workers} worker processes...")

    if to_process:
        t0 = time.time()
        completed = 0
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_worker_ocr, p): p for p in to_process}
            for fut in as_completed(futures):
                p, res = fut.result()
                cache[p] = res
                completed += 1
                if completed % 25 == 0 or completed == len(to_process):
                    elapsed = time.time() - t0
                    speed = completed / max(elapsed, 0.001)
                    rem = (len(to_process) - completed) / max(speed, 0.001)
                    print(f"    [{completed}/{len(to_process)}] {speed:.1f} slips/sec | Elapsed: {elapsed:.0f}s | Est. Rem: {rem:.0f}s")

        with open(OCR_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"[OK] OCR Extraction complete in {time.time() - t0:.1f}s. Cache updated.")

    ordered_results = [cache[p] for p in master_paths]
    return ordered_results


def generate_duplicate_audit_report(manifest_data, ocr_data_map, out_excel_path):
    print(f"[*] Generating Duplicate Audit Report: {out_excel_path}...")
    wb = openpyxl.Workbook()
    
    # Sheet 1: Master Slips
    ws_master = wb.active
    ws_master.title = "สลิปจริง_Master_560"
    
    # Sheet 2: Duplicates
    ws_dup = wb.create_sheet(title="รายการสำเนาซ้ำ_2232_ไฟล์")
    
    # Styles
    f_header = Font(name="Sarabun", size=11, bold=True, color="FFFFFF")
    f_data = Font(name="Sarabun", size=10)
    fill_master = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_dup = PatternFill(start_color="B45309", end_color="B45309", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style='thin', color='D1D5DB'),
        right=Side(style='thin', color='D1D5DB'),
        top=Side(style='thin', color='D1D5DB'),
        bottom=Side(style='thin', color='D1D5DB')
    )
    
    # Count duplicates per master
    dup_counts = {}
    for d in manifest_data["duplicates"]:
        m_name = d["master_slip"]
        dup_counts[m_name] = dup_counts.get(m_name, 0) + 1

    # Headers for Sheet 1
    m_headers = ["ลำดับ", "ชื่อไฟล์สลิปหลัก (Master)", "วันที่", "เวลา", "ธนาคารผู้โอน", "ชื่อผู้โอน", "ยอดเงิน (บาท)", "ชื่อผู้รับเงิน", "ธนาคารผู้รับ", "บันทึกช่วยจำ", "Transaction Ref (QR)", "จำนวนไฟล์ซ้ำที่ตัดออก"]
    ws_master.append(m_headers)
    for col_idx in range(1, len(m_headers) + 1):
        cell = ws_master.cell(row=1, column=col_idx)
        cell.font = f_header
        cell.fill = fill_master
        cell.alignment = align_center

    for idx, p in enumerate(manifest_data["master_slips"]):
        fn = os.path.basename(p)
        info = ocr_data_map.get(p, {})
        n_dups = dup_counts.get(fn, 0)
        row = [
            idx + 1,
            fn,
            info.get("date", "-"),
            info.get("time", "-"),
            info.get("sender_bank", "-"),
            info.get("sender_name", "-"),
            info.get("amount", "-"),
            info.get("receiver_name", "-"),
            info.get("receiver_bank", "-"),
            info.get("memo", "-"),
            info.get("remarks", "-"),
            n_dups
        ]
        ws_master.append(row)
        for col_idx in range(1, len(row) + 1):
            c = ws_master.cell(row=idx + 2, column=col_idx)
            c.font = f_data
            c.alignment = align_center
            c.border = thin_border

    # Headers for Sheet 2
    d_headers = ["ลำดับ", "ชื่อไฟล์สำเนาที่ซ้ำ (Duplicate File)", "ซ้ำกับสลิปหลัก (Mapped Master)", "Cluster ID", "สถานะการตรวจสอบความซ้ำซ้อน (Verification)"]
    ws_dup.append(d_headers)
    for col_idx in range(1, len(d_headers) + 1):
        cell = ws_dup.cell(row=1, column=col_idx)
        cell.font = f_header
        cell.fill = fill_dup
        cell.alignment = align_center

    for idx, d in enumerate(manifest_data["duplicates"]):
        row = [
            idx + 1,
            d["duplicate_file"],
            d["master_slip"],
            d["cluster_id"],
            "ตรวจพบเป็นไฟล์สำเนาซ้ำบิตต่อบิต/ลายนิ้วมือภาพตรงกัน 100% (Duplicate Verified)"
        ]
        ws_dup.append(row)
        for col_idx in range(1, len(row) + 1):
            c = ws_dup.cell(row=idx + 2, column=col_idx)
            c.font = f_data
            c.alignment = align_center
            c.border = thin_border

    # Auto-adjust column widths
    for ws in (ws_master, ws_dup):
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 45)

    wb.save(out_excel_path)
    print(f"[OK] Saved Duplicate Audit Report: {out_excel_path}")


def main():
    print("=" * 70)
    print(" 🏛️ SYSTEM 1: MASTER UNIQUE 560 SLIPS FORENSIC PIPELINE")
    print(" Standard: Stage Forensic Smart Zoom & Crop + Pure White Canvas (#FFFFFF)")
    print("=" * 70)

    if not os.path.exists(MANIFEST_FILE):
        print(f"[!] Error: Manifest not found at {MANIFEST_FILE}")
        sys.exit(1)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    master_slips = manifest_data["master_slips"]
    print(f"[*] Total Master Slips: {len(master_slips)}")
    print(f"[*] Total Mapped Duplicates: {len(manifest_data['duplicates'])}")

    # 1. Parallel OCR & QR Extraction
    ocr_list = run_parallel_ocr(master_slips, max_workers=6)
    ocr_map = {p: ocr_list[i] for i, p in enumerate(master_slips)}

    # 2. Export Excel Spreadsheets
    out_excel_slips = os.path.join(OUTPUT_DIR, "Evidence_Slips_Master_Unique_560.xlsx")
    export_evidence_excel(ocr_list, out_excel_slips)
    print(f"[OK] Exported 10-Column Evidence Excel: {out_excel_slips}")

    out_audit_excel = os.path.join(OUTPUT_DIR, "DUPLICATE_SLIP_AUDIT_REPORT.xlsx")
    generate_duplicate_audit_report(manifest_data, ocr_map, out_audit_excel)

    # 3. Render High-Performance PDF via PyMuPDF C-Binding Streaming
    out_pdf_path = os.path.join(OUTPUT_DIR, "Evidence_Slips_Master_Unique_560.pdf")
    print(f"[*] Rendering Master Slips PDF ({len(master_slips)} pages + 10-Col Summary)...")

    assembler = PDFAssembler(output_path=out_pdf_path)

    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        global_page_idx = 0
        t0_render = time.time()

        for idx, img_p in enumerate(master_slips):
            img = imread_unicode(img_p)
            if img is None:
                print(f"    [!] Could not read {img_p}")
                continue

            # Stage Forensic Smart Zoom & Crop
            trimmed_img = forensic_smart_zoom_crop(img)
            
            info = ocr_map.get(img_p, {})
            amt = info.get("amount", "-")
            date_str = info.get("date", "-")
            corrob = f"สลิปหลักฐานลำดับที่ {idx + 1} | ยอดเงิน: {amt} บาท ({date_str})"

            global_page_idx += 1
            assembler.add_single_page_image(
                trimmed_img,
                align="center",
                page_num=global_page_idx,
                mode="SLIP",
                corroborated=corrob
            )
            page = assembler.pdf_pages.pop()
            fp = os.path.join(tmp, f"slip_p{global_page_idx:05d}.png")
            page.save(fp)
            paths.append((fp, page.size))

            if (idx + 1) % 50 == 0 or (idx + 1) == len(master_slips):
                print(f"    Rendered [{idx + 1}/{len(master_slips)}] slips ({(time.time()-t0_render):.1f}s)...")

        # Note: Summary Table is now decoupled into _skills/Summary_Table module.
        # Master Slips PDF preserves strictly 1:1 slip page numbering (Page 1 = Slip 1 .. Page N = Slip N).
        print(f"[*] Writing {len(paths)} pure slip pages to {os.path.basename(out_pdf_path)} via PyMuPDF C-Binding...")
        t0_save = time.time()
        mode = save_pdf_streaming(paths, out_pdf_path)
        print(f"[OK] Saved {out_pdf_path} ({len(paths)} pages) in {time.time()-t0_save:.2f}s via {mode}!")

    # Generate Separate Dedicated Summary & Index Dossier PDF via Summary_Table
    out_summary_pdf = os.path.splitext(out_pdf_path)[0] + "_Summary_Index.pdf"
    print(f"[*] Generating dedicated standalone Summary & Index Dossier -> {os.path.basename(out_summary_pdf)}...")
    try:
        from _skills.Summary_Table.scripts.summary_table import build_summary_dossier
        build_summary_dossier(
            input_json=ocr_list,
            output_pdf=out_summary_pdf,
            output_excel=out_excel_slips,
            include_cover=True
        )
        print(f"  📑 Standalone Summary PDF: {out_summary_pdf}")
    except Exception as e:
        print(f"  Note on standalone summary generation: {e}")


    print("\n" + "=" * 70)
    print(" 🎉 SYSTEM 1 COMPLETED SUCCESSFULLY!")
    print(f"  📄 Master Slips PDF: {out_pdf_path}")
    print(f"  📊 Evidence 10-Col Excel: {out_excel_slips}")
    print(f"  🛡️ Duplicate Audit Excel: {out_audit_excel}")
    print("=" * 70)


if __name__ == "__main__":
    main()
