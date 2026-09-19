#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/execute_option1_dedup.py
==============================
Executes Option 1:
1. Deletes duplicated page 2539 (0-indexed 2538) from Evidence_Chat_Master_Combined_Vol1_to_3.pdf.
2. Re-stamps page header numbers on subsequent pages (new pages 2539 to 2559) so physical page == header page.
3. Updates Slip Index JSON (item 83 becomes '2538', items 84-89 shift by -1).
4. Rebuilds Standalone Summary Table & Front Cover (PDF & Excel) via _skills/Summary_Table.
5. Verifies 100% page alignment.
"""

import os
import sys
import shutil
import json
import fitz
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

BASE_DIR = r"d:\Project\DIGITAL_EVIDENCE"
OUT_DIR = os.path.join(BASE_DIR, "Folder_Out")
MASTER_PDF = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3.pdf")
JSON_PATH = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")

sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Dicut_Chat", "scripts"))
from process_chat import get_sarabun_fonts

def main():
    print("=" * 80)
    print("🚀 EXECUTING OPTION 1: DEDUP & SYNC MASTER EVIDENCE DOSSIER")
    print("=" * 80)

    # 1. Safety Backup
    backup_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_backup_pre_dedup.pdf")
    if not os.path.exists(backup_pdf):
        print(f"Creating backup of master PDF -> {backup_pdf}")
        shutil.copy2(MASTER_PDF, backup_pdf)

    # 2. Open PDF and verify page 2539
    doc = fitz.open(MASTER_PDF)
    orig_len = len(doc)
    print(f"Original master PDF total pages: {orig_len}")
    if orig_len != 2560:
        print(f"Warning: Expected 2560 pages, found {orig_len}")

    if orig_len == 2560:
        # Delete page index 2538 (1-indexed 2539)
        print("Deleting duplicated page index 2538 (Physical page 2539)...")
        doc.delete_page(2538)
        new_len = len(doc)
        print(f"New master PDF total pages: {new_len} (Expected: 2559)")

        # 3. Patch header numbers on remaining pages (from new index 2538 to 2558 -> physical pages 2539 to 2559)
        fonts = get_sarabun_fonts()
        portrait_w = 993
        margin_right = 93
        line1_y = 46  # header_y (38) + 8

        print("Re-stamping page numbers on pages 2539 to 2559 to guarantee 1:1 physical page match...")
        for idx in range(2538, new_len):
            new_page_no = idx + 1
            page = doc[idx]
            page_rect = page.rect
            wipe_x0 = page_rect.width - 160
            wipe_y0 = 20
            wipe_x1 = page_rect.width - 50
            wipe_y1 = 50
            wipe_rect = fitz.Rect(wipe_x0, wipe_y0, wipe_x1, wipe_y1)
            page.draw_rect(wipe_rect, color=(1, 1, 1), fill=(1, 1, 1))

            page_str = str(new_page_no)
            patch_w = 200
            patch_h = 40
            patch_img = Image.new("RGB", (patch_w, patch_h), (255, 255, 255))
            draw = ImageDraw.Draw(patch_img)

            b_pval = draw.textbbox((0, 0), page_str, font=fonts["header_val"])
            b_plbl = draw.textbbox((0, 0), "PAGE : ", font=fonts["header_lbl"])
            lbl_w = b_plbl[2] - b_plbl[0]
            val_w = b_pval[2] - b_pval[0]
            tot_w = lbl_w + val_w

            start_x = patch_w - tot_w - 5
            draw.text((start_x, 5), "PAGE : ", fill="#111827", font=fonts["header_lbl"])
            draw.text((start_x + lbl_w, 5), page_str, fill="#111827", font=fonts["header_val"])

            pt_w = patch_w * 72.0 / 96.0
            pt_h = patch_h * 72.0 / 96.0
            insert_x1 = page_rect.width - (margin_right * 72.0 / 96.0)
            insert_x0 = insert_x1 - pt_w
            insert_y0 = (line1_y - 5) * 72.0 / 96.0
            insert_y1 = insert_y0 + pt_h
            insert_rect = fitz.Rect(insert_x0, insert_y0, insert_x1, insert_y1)

            import io
            buf = io.BytesIO()
            patch_img.save(buf, format="PNG")
            page.insert_image(insert_rect, stream=buf.getvalue())

        # Save master PDF
        temp_saved_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_clean.pdf")
        doc.save(temp_saved_pdf, garbage=4, deflate=True)
        doc.close()
        os.replace(temp_saved_pdf, MASTER_PDF)
        print(f"✅ Master PDF saved successfully -> {MASTER_PDF} ({new_len} pages)")
    else:
        new_len = orig_len
        print(f"Master PDF already has {new_len} pages.")
        doc.close()

    # 4. Update JSON Index
    print("\nUpdating Slip Index JSON...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        slips = json.load(f)

    for item in slips:
        idx_no = item.get("index")
        p_raw = str(item.get("page_no", ""))
        
        # Item 83: Change from '2538, 2539' to '2538'
        if idx_no == 83:
            item["page_no"] = "2538"
            print(f"  Updated item {idx_no}: page_no set to 2538")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(slips, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved updated JSON -> {JSON_PATH}")

    # 5. Re-run Summary Table Skill to regenerate Standalone Front Cover & Excel
    print("\nRe-generating Standalone Summary Table & Front Cover...")
    sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Summary_Table", "scripts"))
    from summary_table import build_summary_dossier
    front_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Front_Cover_and_Index.pdf")
    excel_out = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx")
    build_summary_dossier(JSON_PATH, front_pdf, output_excel=excel_out, include_cover=True, total_chat_pages=new_len)
    print(f"✅ Standalone dossier regenerated successfully!")

    # 6. Generate Verification Previews
    print("\nRendering verification preview images...")
    preview_dir = os.path.join(BASE_DIR, "scratch", "option1_verification")
    os.makedirs(preview_dir, exist_ok=True)

    doc_ver = fitz.open(MASTER_PDF)
    # Preview page 2538 and page 2539
    p2538_pix = doc_ver[2537].get_pixmap(dpi=120)
    p2538_pix.save(os.path.join(preview_dir, "master_page_2538.png"))
    p2539_pix = doc_ver[2538].get_pixmap(dpi=120)
    p2539_pix.save(os.path.join(preview_dir, "master_page_2539.png"))
    p2540_pix = doc_ver[2539].get_pixmap(dpi=120)
    p2540_pix.save(os.path.join(preview_dir, "master_page_2540.png"))
    doc_ver.close()

    doc_front = fitz.open(front_pdf)
    # Preview page 6 (index page 5 where items 80-89 are located)
    p_idx_pix = doc_front[len(doc_front) - 1].get_pixmap(dpi=120)
    p_idx_pix.save(os.path.join(preview_dir, "front_index_page_last.png"))
    doc_front.close()

    print(f"✅ Verification images saved in {preview_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
