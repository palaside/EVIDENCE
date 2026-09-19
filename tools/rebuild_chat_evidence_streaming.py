#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/rebuild_chat_evidence_streaming.py
========================================
Executes full rebuild of Real Case Chat Evidence using the new
Continuous Streaming Canvas Pipeline (ต่อสายพานยาวต่อเนื่องแล้วหั่น) + Post-Slice Dedup Rule.

Workflow:
1. Re-processes Volume 1, Volume 2, Volume 3 with Streaming Canvas Pipeline.
2. Combines into Evidence_Chat_Master_Combined_Vol1_to_3.pdf with continuous 1:1 page numbering.
3. Re-indexes all 89 verified slips, mapping them to exact new physical page numbers.
4. Preserves Option 1 Verified Account Binding (Names & Banks).
5. Generates Decoupled Standalone Cover & 10-Column Index PDF and Excel.
6. Renders verification preview images.
"""

import os
import sys
import time
import json
import re
import shutil
import fitz
import datetime

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
        except Exception:
            pass

BASE_DIR = r"d:\Project\DIGITAL_EVIDENCE"
OUT_DIR = os.path.join(BASE_DIR, "Folder_Out")
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Dicut_Chat", "scripts"))
sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Search_Slip", "scripts"))
sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Summary_Table", "scripts"))

from process_chat import process_chat_pipeline
from search_slip import search_slips_in_pdf
from summary_table import build_summary_dossier

CHATS = [
    {
        "vol": 1,
        "name": "แชทที่ 1",
        "path": r"F:\Project\EDOK\แชทที่ 1",
        "pdf": os.path.join(OUT_DIR, "Evidence_Chat_Volume_1.pdf"),
    },
    {
        "vol": 2,
        "name": "แชทที่ 2",
        "path": r"F:\Project\EDOK\แชทที่ 2",
        "pdf": os.path.join(OUT_DIR, "Evidence_Chat_Volume_2.pdf"),
    },
    {
        "vol": 3,
        "name": "แชทที่ 3",
        "path": r"F:\Project\EDOK\แชทที่ 3",
        "pdf": os.path.join(OUT_DIR, "Evidence_Chat_Volume_3.pdf"),
    }
]

def log(msg):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] {msg}", flush=True)

def main():
    log("=" * 80)
    log("🚀 DIGITAL EVIDENCE: REBUILDING MASTER EVIDENCE VIA STREAMING CANVAS PIPELINE")
    log("=" * 80)
    t_start = time.time()

    # Load existing verified 89 slips database to preserve Option 1 account bindings
    ref_json_path = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")
    verified_slips_db = {}
    if os.path.exists(ref_json_path):
        with open(ref_json_path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                ref_id = item.get("ref_id")
                if ref_id and ref_id != "-":
                    verified_slips_db[ref_id] = item
                amt_key = f"{item.get('amount')}_{item.get('date_time')}"
                verified_slips_db[amt_key] = item

    generated_pdfs = []
    current_page = 1

    # 1. Process Volumes sequentially with continuous global page indexing
    for item in CHATS:
        vol = item["vol"]
        name = item["name"]
        src = item["path"]
        pdf_out = item["pdf"]

        log(f"\n📂 [Volume {vol}/3] กำลังประมวลผล: {name}")
        log(f"   ต้นทาง: {src}")
        log(f"   ไฟล์ PDF: {pdf_out}")
        log(f"   เลขหน้าเริ่มต้น: หน้า {current_page}")

        # Smart Session Resumption: If volume 1 or 2 was already successfully built in this streaming run
        if os.path.exists(pdf_out) and vol in [1, 2] and "--force-all" not in sys.argv:
            try:
                sub_d = fitz.open(pdf_out)
                page_count = len(sub_d)
                sub_d.close()
                mtime_age = time.time() - os.path.getmtime(pdf_out)
                if page_count > 0 and mtime_age < 7200:  # Built within last 2 hours
                    log(f"⚡ [Volume {vol}] ตรวจพบไฟล์ที่เพิ่งประมวลผลเสร็จในเซสชันนี้: {page_count} หน้า (หน้า {current_page} - {current_page + page_count - 1}) -> นำมาใช้ต่อทันที")
                    current_page += page_count
                    generated_pdfs.append(pdf_out)
                    continue
            except Exception as e:
                log(f"⚠️ ไม่สามารถเปิด {pdf_out} ได้ ({e}) -> กำลังสร้างใหม่...")

        t0 = time.time()
        page_count = process_chat_pipeline(src, pdf_out, chat_mode=True, start_page_num=current_page)
        elap = time.time() - t0
        log(f"✅ [Volume {vol}] เสร็จสมบูรณ์: {page_count} หน้า (หน้า {current_page} - {current_page + page_count - 1}) ใช้เวลา {elap:.1f} วินาที")
        current_page += page_count
        generated_pdfs.append(pdf_out)

    # 2. Merge into Master Combined PDF
    combined_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3.pdf")
    combined_xlsx = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx")
    combined_json = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")

    log(f"\n📑 กำลังรวมเอกสารทั้ง 3 เล่มเป็นชุดหลักฐานรวม (Master Dossier)...")
    doc_master = fitz.open()
    for p in generated_pdfs:
        sub_doc = fitz.open(p)
        doc_master.insert_pdf(sub_doc)
        sub_doc.close()

    doc_master.save(combined_pdf, garbage=4, deflate=True)
    tot_pages = len(doc_master)
    doc_master.close()
    log(f"✅ รวมเล่มเสร็จสมบูรณ์ -> {combined_pdf} (รวมทั้งหมด {tot_pages} หน้า)")

    # 3. Re-index slips from Master PDF and bind with Verified Account details
    log(f"\n🔍 กำลังสแกนหาตำแหน่งหน้าสลิปใหม่ทั้งหมดในเล่มรวม ({tot_pages} หน้า)...")
    scanned_slips = search_slips_in_pdf(combined_pdf)
    log(f"   สแกนพบสลิปธุรกรรมทั้งหมด: {len(scanned_slips)} รายการ")

    # Map scanned slips to Option 1 verified records
    final_indexed_slips = []
    seen_refs = set()

    for idx, s in enumerate(scanned_slips):
        ref_id = s.get("ref_id")
        amt = s.get("amount")
        dt = s.get("date_time")
        p_no = s.get("page_no")

        matched = None
        if ref_id and ref_id in verified_slips_db:
            matched = verified_slips_db[ref_id]
        else:
            amt_key = f"{amt}_{dt}"
            if amt_key in verified_slips_db:
                matched = verified_slips_db[amt_key]

        entry = dict(s)
        entry["index"] = idx + 1
        if matched:
            entry["sender_name"] = matched.get("sender_name", s.get("sender_name"))
            entry["sender_bank"] = matched.get("sender_bank", s.get("sender_bank"))
            entry["receiver_name"] = matched.get("receiver_name", s.get("receiver_name"))
            entry["receiver_bank"] = matched.get("receiver_bank", s.get("receiver_bank"))
            if matched.get("date_time") and matched.get("date_time") != "-":
                entry["date_time"] = matched.get("date_time")
            if matched.get("amount") and matched.get("amount") != "-":
                entry["amount"] = matched.get("amount")
        
        final_indexed_slips.append(entry)

    # Save JSON index
    with open(combined_json, "w", encoding="utf-8") as f:
        json.dump(final_indexed_slips, f, ensure_ascii=False, indent=2)
    log(f"✅ บันทึกดัชนี JSON สลิปใหม่ ({len(final_indexed_slips)} รายการ) -> {combined_json}")

    # 4. Generate Decoupled Standalone Cover & Summary Table PDF & Excel
    log(f"\n📑 กำลังสร้างชุดเอกสารสารบัญสรุปและหน้าปกแยกเดี่ยว (Decoupled Dossier)...")
    front_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Front_Cover_and_Index.pdf")
    build_summary_dossier(combined_json, front_pdf, output_excel=combined_xlsx, include_cover=True, total_chat_pages=tot_pages)
    log(f"✅ สร้างชุดหน้าปกและสารบัญแยกเดี่ยวสำเร็จ -> {front_pdf}")

    # 5. Render Verification Previews
    log(f"\n🖼️ กำลังเรนเดอร์ภาพตัวอย่างตรวจสอบคุณภาพ...")
    preview_dir = os.path.join(BASE_DIR, "scratch", "streaming_rebuild_previews")
    os.makedirs(preview_dir, exist_ok=True)

    doc_ver = fitz.open(combined_pdf)
    doc_ver[0].get_pixmap(dpi=100).save(os.path.join(preview_dir, "master_page_1.png"))
    doc_ver[min(100, len(doc_ver)-1)].get_pixmap(dpi=100).save(os.path.join(preview_dir, "master_page_sample.png"))
    doc_ver[len(doc_ver)-1].get_pixmap(dpi=100).save(os.path.join(preview_dir, "master_page_last.png"))
    doc_ver.close()

    doc_cov = fitz.open(front_pdf)
    doc_cov[0].get_pixmap(dpi=100).save(os.path.join(preview_dir, "cover_page.png"))
    doc_cov[1].get_pixmap(dpi=100).save(os.path.join(preview_dir, "index_page_1.png"))
    doc_cov.close()

    tot_time = time.time() - t_start
    log("=" * 80)
    log(f"🎉 REBUILD COMPLETED SUCCESSFULLY IN {tot_time:.1f}s!")
    log(f"   Master Chat PDF: {combined_pdf} ({tot_pages} pages)")
    log(f"   Front Dossier: {front_pdf}")
    log(f"   Excel Index: {combined_xlsx}")
    log("=" * 80)

if __name__ == "__main__":
    main()
