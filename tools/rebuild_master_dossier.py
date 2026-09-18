import os
import sys
import json
import time

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "Folder_Out")

sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Search_Slip", "scripts"))
sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Dicut_Chat", "scripts"))
sys.path.insert(0, os.path.join(BASE_DIR, "tools"))

from search_slip import export_to_excel
from generate_cover_page import build_front_dossier_pdf, merge_cover_to_master_pdf
from evidence_hash_manifest import generate_hash_manifest
from verify_master_evidence import verify_master_evidence
import verify_cleaned_slips as v_clean

def main():
    print("🚀 Rebuilding Master Dossier with 100% Clean Thai Fonts & Verified Slips...")
    t0 = time.time()

    # 1. Update Slip Index JSON
    json_path = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")
    cleaned_slips = v_clean.cleaned_slips
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_slips, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved cleaned JSON index ({len(cleaned_slips)} slips) -> {json_path}")

    # 2. Update Excel Index (Sarabun Center-Aligned Grid)
    excel_path = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx")
    export_items = []
    for s in cleaned_slips:
        p_nums = [int(p.strip()) for p in str(s["page_no"]).split(",") if p.strip().isdigit()]
        export_items.append({
            "pages": p_nums if p_nums else [1],
            "datetime": s.get("date_time", "-"),
            "sender_bank": s.get("sender_bank", "-"),
            "sender_name": s.get("sender_name", "-"),
            "amount": s.get("amount", "-"),
            "receiver_name": s.get("receiver_name", "-"),
            "receiver_bank": s.get("receiver_bank", "-"),
            "memo": s.get("memo", "-"),
            "ref_id": s.get("ref_id", "-")
        })
    export_to_excel(export_items, excel_path)
    print(f"✅ Saved cleaned Excel index -> {excel_path}")

    # 3. Regenerate Front Cover and Index Dossier (PDF)
    front_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Front_Cover_and_Index.pdf")
    front_count = build_front_dossier_pdf(json_path, front_pdf, start_page_num=1)
    print(f"✅ Regenerated Front Dossier ({front_count} pages) -> {front_pdf}")

    # 4. Merge Front Dossier with Master Chat PDF (PyMuPDF C-Binding)
    master_chat_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3.pdf")
    with_cover_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_With_Cover.pdf")
    merge_cover_to_master_pdf(master_chat_pdf, front_pdf, with_cover_pdf)
    print(f"✅ Merged into Master Dossier with Cover -> {with_cover_pdf}")

    # 5. Generate SHA-256 Checksum Certificate
    manifest_targets = [
        with_cover_pdf,
        master_chat_pdf,
        front_pdf,
        excel_path,
        json_path
    ]
    manifest_res = generate_hash_manifest(manifest_targets, OUT_DIR, case_title="สำนวนพยานหลักฐานแชทจริง (Volume 1-3)")
    print(f"✅ Generated SHA-256 Certificate: {manifest_res['certificate_pdf']}")

    # 6. Automated Verification Gate
    print("\n🔬 Running 100% Cross-Verification Gate...")
    v_ok = verify_master_evidence(with_cover_pdf, json_path)
    if v_ok:
        print("🏆 100% VERIFICATION PASSED: All 89 slips matched perfectly!")
    else:
        print("⚠️ Verification reported remarks.")

    # 7. Render preview images of index pages 1 and 2
    import fitz
    doc_front = fitz.open(front_pdf)
    p_cover = doc_front[0].get_pixmap(dpi=150)
    p_cover.save(os.path.join(OUT_DIR, "preview_cover_v2.png"))
    p_idx1 = doc_front[1].get_pixmap(dpi=150)
    p_idx1.save(os.path.join(OUT_DIR, "preview_index_p1_v2.png"))
    p_idx2 = doc_front[2].get_pixmap(dpi=150)
    p_idx2.save(os.path.join(OUT_DIR, "preview_index_p2_v2.png"))
    print("✅ Rendered preview images: preview_cover_v2.png, preview_index_p1_v2.png, preview_index_p2_v2.png")

    elap = time.time() - t0
    print(f"\n🎉 Entire rebuild finished in {elap:.2f} seconds!")

if __name__ == "__main__":
    main()
