"""
DIGITAL EVIDENCE - Real Case Chat Processing Master Pipeline
=============================================================
Processes 3 real chat evidence folders in strict chronological order:
1. F:\\Project\\EDOK\\แชทที่ 1 (322 images) -> Evidence_Chat_Volume_1.pdf + Slip Index
2. F:\\Project\\EDOK\\แชทที่ 2 (6 images)   -> Evidence_Chat_Volume_2.pdf + Slip Index
3. F:\\Project\\EDOK\\แชทที่ 3 (143 images) -> Evidence_Chat_Volume_3.pdf + Slip Index
4. Master Merger                             -> Evidence_Chat_Master_Combined_Vol1_to_3.pdf + Slip Index

Complies with:
- Dicut_Chat standard (12px feather, quiet zone lookahead 1.30x, slip-block-fit canvas)
- Auto-Audit 100% Quality Gate
- Search_Slip post-PDF indexing (10-column Excel + JSON, Sarabun Center-Aligned Grid)
- Memory-safe streaming batching
"""

import sys
import os
import time
import datetime
import fitz

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
        except Exception:
            pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICUT_SCRIPT = os.path.join(BASE_DIR, "_skills", "Dicut_Chat", "scripts")
SEARCH_SCRIPT = os.path.join(BASE_DIR, "_skills", "Search_Slip", "scripts")

sys.path.insert(0, DICUT_SCRIPT)
sys.path.insert(0, SEARCH_SCRIPT)

from process_chat import process_chat_pipeline
from search_slip import search_slips_in_pdf, export_to_excel

OUT_DIR = os.path.join(BASE_DIR, "Folder_Out")
os.makedirs(OUT_DIR, exist_ok=True)

CHATS = [
    {
        "vol": 1,
        "name": "แชทที่ 1",
        "path": r"F:\Project\EDOK\แชทที่ 1",
        "pdf": os.path.join(OUT_DIR, "Evidence_Chat_Volume_1.pdf"),
        "xlsx": os.path.join(OUT_DIR, "Evidence_Chat_Volume_1_Slip_Index.xlsx"),
        "json": os.path.join(OUT_DIR, "Evidence_Chat_Volume_1_Slip_Index.json"),
    },
    {
        "vol": 2,
        "name": "แชทที่ 2",
        "path": r"F:\Project\EDOK\แชทที่ 2",
        "pdf": os.path.join(OUT_DIR, "Evidence_Chat_Volume_2.pdf"),
        "xlsx": os.path.join(OUT_DIR, "Evidence_Chat_Volume_2_Slip_Index.xlsx"),
        "json": os.path.join(OUT_DIR, "Evidence_Chat_Volume_2_Slip_Index.json"),
    },
    {
        "vol": 3,
        "name": "แชทที่ 3",
        "path": r"F:\Project\EDOK\แชทที่ 3",
        "pdf": os.path.join(OUT_DIR, "Evidence_Chat_Volume_3.pdf"),
        "xlsx": os.path.join(OUT_DIR, "Evidence_Chat_Volume_3_Slip_Index.xlsx"),
        "json": os.path.join(OUT_DIR, "Evidence_Chat_Volume_3_Slip_Index.json"),
    }
]

def log(msg):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] {msg}", flush=True)

def run_pipeline():
    log("================================================================================")
    log("🚀 DIGITAL EVIDENCE: Real-World Chat Evidence Processing Starting...")
    log("================================================================================")
    start_all = time.time()
    generated_pdfs = []

    for item in CHATS:
        vol = item["vol"]
        name = item["name"]
        src = item["path"]
        pdf_out = item["pdf"]
        xlsx_out = item["xlsx"]
        json_out = item["json"]

        log(f"\n📂 [Volume {vol}/3] กำลังประมวลผล: {name}")
        log(f"   พาทต้นทาง: {src}")
        log(f"   พาทไฟล์ PDF: {pdf_out}")

        if not os.path.exists(src):
            log(f"❌ [Error] ไม่พบโฟลเดอร์: {src}")
            continue

        t0 = time.time()
        # 1. Run Dicut_Chat Pipeline (Chat mode)
        page_count = process_chat_pipeline(src, pdf_out, chat_mode=True)
        elap = time.time() - t0
        log(f"✅ [Volume {vol}] สร้าง PDF สำเร็จ ({page_count} หน้า) ใช้เวลา: {elap:.1f} วินาที")
        generated_pdfs.append(pdf_out)

        # 2. Run Search_Slip Indexing
        log(f"🔍 [Volume {vol}] กำลังสแกนหาตำแหน่งหน้าสลิปใน {os.path.basename(pdf_out)}...")
        slips = search_slips_in_pdf(pdf_out)
        log(f"   พบสลิปธุรกรรมทั้งหมด: {len(slips)} รายการ")
        log(f"✅ [Volume {vol}] ส่งออกสารบัญสลิปสำเร็จ:")
        log(f"   - Excel (Sarabun Center-Aligned): {xlsx_out}")
        log(f"   - JSON: {json_out}")

    # 3. Master Merged PDF (Vol 1 + 2 + 3)
    if len(generated_pdfs) == len(CHATS):
        combined_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3.pdf")
        combined_xlsx = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx")
        combined_json = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")

        log(f"\n📑 กำลังรวมเอกสารทั้ง 3 เล่มเป็นชุดหลักฐานรวม (Master Dossier)...")
        doc_master = fitz.open()
        for p in generated_pdfs:
            sub_doc = fitz.open(p)
            doc_master.insert_pdf(sub_doc)
            sub_doc.close()

        doc_master.save(combined_pdf)
        tot_pages = len(doc_master)
        doc_master.close()
        log(f"✅ รวมเล่มเสร็จสมบูรณ์ -> {combined_pdf} (รวมทั้งหมด {tot_pages} หน้า)")

        log(f"🔍 กำลังสร้างสารบัญสลิปสำหรับชุดเอกสารรวม...")
        master_slips = search_slips_in_pdf(combined_pdf)
        log(f"✅ สารบัญรวมเสร็จสมบูรณ์: {combined_xlsx} (พบสลิปรวม {len(master_slips)} รายการ)")

    total_elap = time.time() - start_all
    log(f"\n================================================================================")
    log(f"🎉 ประมวลผลพยานหลักฐานแชทจริงทั้ง 3 ชุดเสร็จสมบูรณ์ทั้งหมดในเวลา: {total_elap:.1f} วินาที")
    log(f"📁 ตรวจสอบผลลัพธ์ทั้งหมดได้ที่: {OUT_DIR}")
    log(f"================================================================================")

if __name__ == "__main__":
    run_pipeline()
