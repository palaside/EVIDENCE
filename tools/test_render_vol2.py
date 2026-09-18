"""
DIGITAL EVIDENCE - Test Renderer for Volume 2 (แชทที่ 2)
Tests Header Evidence Ribbon & Footer 3-Line Disclaimer with preview PNG generation.
"""

import sys
import os
import time

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
import fitz

def main():
    src_dir = r"F:\Project\EDOK\แชทที่ 2"
    out_dir = os.path.join(BASE_DIR, "Folder_Out")
    os.makedirs(out_dir, exist_ok=True)

    out_pdf = os.path.join(out_dir, "Evidence_Chat_Volume_2.pdf")
    preview_png1 = os.path.join(out_dir, "test_vol2_page1_preview.png")
    preview_png2 = os.path.join(out_dir, "test_vol2_page2_preview.png")

    print("================================================================================")
    print("🚀 DIGITAL EVIDENCE: Running Test Render on Volume 2 (แชทที่ 2)")
    print(f"   Source Path : {src_dir}")
    print(f"   Target PDF  : {out_pdf}")
    print("================================================================================")

    if not os.path.exists(src_dir):
        print(f"❌ Error: Folder not found: {src_dir}")
        sys.exit(1)

    t0 = time.time()
    page_count = process_chat_pipeline(src_dir, out_pdf, chat_mode=True)
    elap = time.time() - t0
    print(f"✅ Rendered {page_count} pages in {elap:.2f} seconds -> {out_pdf}")

    # Generate preview PNGs for visual inspection
    doc = fitz.open(out_pdf)
    if len(doc) > 0:
        pix = doc[0].get_pixmap(dpi=150)
        pix.save(preview_png1)
        print(f"📸 Saved Page 1 Preview -> {preview_png1}")
    if len(doc) > 1:
        pix = doc[1].get_pixmap(dpi=150)
        pix.save(preview_png2)
        print(f"📸 Saved Page 2 Preview -> {preview_png2}")
    doc.close()

    print("🎉 Volume 2 Test Render Complete!")

if __name__ == "__main__":
    main()
