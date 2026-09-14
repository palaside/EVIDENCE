#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools/build_reference_archives.py — Builds System 2 and System 3 Reference Archives
1. System 2 (Stem Dedup): Folder_Out/Reference_Archives/Evidence_Slips_Reference_Stems_1160.pdf
2. System 3 (Full Raw): Folder_Out/Reference_Archives/Evidence_Slips_Reference_Raw_2792.pdf
"""

import os
import sys
import glob
import time
import tempfile
from collections import defaultdict
import fitz

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = r"F:\Project\EDOK\Duplicates\Done"
OUT_ARCHIVE_DIR = os.path.join(PROJECT_ROOT, "Folder_Out", "Reference_Archives")
os.makedirs(OUT_ARCHIVE_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(PROJECT_ROOT, "_engines", "Dicut_Chat", "scripts"))
from process_chat import imread_unicode, forensic_smart_zoom_crop, PDFAssembler, save_pdf_streaming, natural_sort_key


def build_stem_reserve_1160():
    out_pdf = os.path.join(OUT_ARCHIVE_DIR, "Evidence_Slips_Reference_Stems_1160.pdf")
    if os.path.exists(out_pdf):
        print(f"[OK] System 2 already exists: {out_pdf} ({os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
        return out_pdf

    print("\n" + "=" * 70)
    print(" 🏛️ SYSTEM 2: STEM DEDUP 1,160 SLIPS REFERENCE ARCHIVE")
    print("=" * 70)

    exts = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(SRC_DIR, ext)))
    files = sorted(list(set(files)), key=natural_sort_key)

    stem_map = defaultdict(list)
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        clean = stem[4:] if stem.startswith("dup_") else stem
        stem_map[clean].append(f)

    # Pick best candidate for each stem
    chosen_files = []
    for clean in sorted(stem_map.keys(), key=natural_sort_key):
        flist = stem_map[clean]
        non_dup = [x for x in flist if not os.path.basename(x).startswith("dup_")]
        cands = non_dup if non_dup else flist
        pngs = [x for x in cands if x.lower().endswith('.png')]
        chosen_files.append(pngs[0] if pngs else cands[0])

    print(f"[*] Total Stems to render: {len(chosen_files)}")
    assembler = PDFAssembler(output_path=out_pdf)

    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        t0 = time.time()
        for idx, p in enumerate(chosen_files):
            img = imread_unicode(p)
            if img is None:
                continue
            trimmed = forensic_smart_zoom_crop(img)
            corrob = f"สลิปสำรองหมวดไฟล์ (Stem Reserve) ลำดับที่ {idx + 1} / {len(chosen_files)}"
            assembler.add_single_page_image(trimmed, align="center", page_num=idx + 1, mode="SLIP", corroborated=corrob)
            page = assembler.pdf_pages.pop()
            fp = os.path.join(tmp, f"stem_p{idx+1:05d}.png")
            page.save(fp)
            paths.append((fp, page.size))

            if (idx + 1) % 100 == 0 or (idx + 1) == len(chosen_files):
                print(f"    Rendered [{idx + 1}/{len(chosen_files)}] ({time.time()-t0:.1f}s)...")

        print(f"[*] Streaming {len(paths)} pages to {out_pdf} via PyMuPDF C-Binding...")
        save_pdf_streaming(paths, out_pdf)
        print(f"[OK] System 2 complete: {out_pdf} ({len(paths)} pages, {os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
    return out_pdf


def build_raw_reserve_2792():
    out_pdf = os.path.join(OUT_ARCHIVE_DIR, "Evidence_Slips_Reference_Raw_2792.pdf")
    if os.path.exists(out_pdf):
        print(f"[OK] System 3 already exists: {out_pdf} ({os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
        return out_pdf

    print("\n" + "=" * 70)
    print(" 🏛️ SYSTEM 3: FULL RAW 2,792 SLIPS REFERENCE ARCHIVE")
    print("=" * 70)

    exts = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(SRC_DIR, ext)))
    files = sorted(list(set(files)), key=natural_sort_key)
    print(f"[*] Total Raw Files to stream: {len(files)}")

    # Fast direct image insert via PyMuPDF (super-fast, < 30 seconds for 2,792 raw images!)
    t0 = time.time()
    doc = fitz.open()
    portrait_w, portrait_h = 744.75, 1054.5  # A4 in points at 72 dpi (993x1406 at 96 dpi)

    for idx, p in enumerate(files):
        page = doc.new_page(width=portrait_w, height=portrait_h)
        # Directly insert image centered
        try:
            pix = fitz.Pixmap(p)
            # scale to fit height 675 pt (approx 900 px)
            target_pt_h = min(675.0, portrait_h - 120.0)
            target_pt_w = min(portrait_w - 80.0, target_pt_h * (pix.width / max(1, pix.height)))
            paste_x = (portrait_w - target_pt_w) / 2.0
            paste_y = (portrait_h - target_pt_h) / 2.0
            rect = fitz.Rect(paste_x, paste_y, paste_x + target_pt_w, paste_y + target_pt_h)
            page.insert_image(rect, filename=p)
            pix = None
        except Exception:
            pass

        if (idx + 1) % 250 == 0 or (idx + 1) == len(files):
            print(f"    Compiled [{idx + 1}/{len(files)}] pages ({time.time()-t0:.1f}s)...")

    doc.save(out_pdf, garbage=4, deflate=True)
    doc.close()
    print(f"[OK] System 3 complete: {out_pdf} ({len(files)} pages in {time.time()-t0:.1f}s, {os.path.getsize(out_pdf)/(1024*1024):.2f} MB)")
    return out_pdf


if __name__ == "__main__":
    build_stem_reserve_1160()
    build_raw_reserve_2792()
