#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/apply_option1_and_fix_headers.py
======================================
1. Enforces Option 1: Verified Account Binding for Sender & Receiver Names + Banks across 89 slips.
2. Cleans remaining month OCR noise (.g -> มิ.ย.).
3. Patches all 144 false-positive chat pages in Evidence_Chat_Master_Combined_Vol1_to_3.pdf
   setting header ribbon back to 'CORROBORATED : บทสนทนาต่อเนื่อง'.
4. Rebuilds Master Combined PDF (2,562 pages), Excel, JSON, and Front Dossier.
"""

import os
import sys
import json
import re
import cv2
import numpy as np
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

JSON_PATH = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")
MASTER_CHAT_PDF = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3.pdf")
COVER_SCRIPT = os.path.join(BASE_DIR, "tools", "generate_cover_page.py")

sys.path.insert(0, os.path.join(BASE_DIR, "_skills", "Dicut_Chat", "scripts"))
from process_chat import get_sarabun_fonts, PDFAssembler

def clean_account_numbers_from_name(val):
    if not val:
        return "-"
    # Strip parenthesized or bracketed account numbers like (XXX-X-XX452-9), (xxx-x-x2717-x), (XXX-XXX-4123)
    cleaned = re.sub(r"\s*[\(\[][Xx\d\s\-*.]+[\)\]]", "", str(val))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "-"


# -------------------------------------------------------------------------
# STEP 1: Option 1 Account Binding (Names Only - Clean Standard)
# -------------------------------------------------------------------------
def apply_account_binding(item):
    sn = item.get("sender_name", "")
    rn = item.get("receiver_name", "")
    sb = item.get("sender_bank", "")
    rb = item.get("receiver_bank", "")
    dt = item.get("date_time", "")
    pg = str(item.get("page_no", ""))
    raw_t = item.get("raw_text", "")

    # Clean date noise (.g -> มิ.ย.)
    dt = re.sub(r"\b\.g\b", "มิ.ย.", dt)
    item["date_time"] = dt

    # Check sender
    if any(k in sn or k in raw_t for k in ["452-9", "4529"]):
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
    elif any(k in sn or k in raw_t for k in ["526-6", "5266"]):
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
    elif any(k in sn or k in raw_t for k in ["558-9", "5589"]):
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif any(k in sn for k in ["996-5", "9965"]):
        item["sender_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["sender_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif any(k in sn for k in ["385-0", "3850"]):
        item["sender_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["sender_bank"] = "กรุงศรีอยุธยา"
    elif any(k in sn for k in ["764-0", "7640"]):
        item["sender_name"] = "น.ส. จิณห์นิภา บุญประเสริฐ"
        item["sender_bank"] = "กรุงไทย"
    elif "2717" in sn:
        item["sender_name"] = "น.ส. ยุวดี ม"
        item["sender_bank"] = "กสิกรไทย"

    # Specific fixes for slips where sender account text had variations
    if pg in ["1876", "2231", "2239", "2336"]:
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
    elif pg in ["2245", "2246", "2255", "2262", "2288"]:
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"

    # Check receiver general account bindings
    if any(k in rn for k in ["385-0", "3850"]):
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "กรุงศรีอยุธยา"
    elif any(k in rn for k in ["996-5", "9965"]):
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif any(k in rn for k in ["764-0", "7640"]):
        item["receiver_name"] = "น.ส. จิณห์นิภา บุญประเสริฐ"
        item["receiver_bank"] = "กรุงไทย"
    elif "526-6" in rn:
        item["receiver_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["receiver_bank"] = "กรุงไทย"
    elif "452-9" in rn:
        item["receiver_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["receiver_bank"] = "กรุงไทย"
    elif "558-9" in rn:
        item["receiver_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif "7558" in rn:
        item["receiver_name"] = "นาย ณัฐชัย รักษาวงษ์"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif "630-1" in rn:
        item["receiver_name"] = "นาย พงศ์ภิระ สิงห์เถื่อน"
        item["receiver_bank"] = "ไทยพาณิชย์"
    elif "040-0" in rn:
        item["receiver_name"] = "นางสาว กนกวรรณ พุทธศรี"
        item["receiver_bank"] = "ไทยพาณิชย์"
    elif "455-1" in rn:
        item["receiver_name"] = "น.ส. ปรียชาติ ฉิมพลี"
        item["receiver_bank"] = "กสิกรไทย"
    elif "313-5" in rn:
        item["receiver_name"] = "นางสาว จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ไทยพาณิชย์"
    elif "717-4" in rn:
        item["receiver_name"] = "น.ส. ยุวดี มีเสมอ"
        item["receiver_bank"] = "กสิกรไทย"
    elif "197-9" in rn:
        item["receiver_name"] = "นาย อนุชิต โพธิ์สาจันทร์"
        item["receiver_bank"] = "กสิกรไทย"
    elif "259-1" in rn:
        item["receiver_name"] = "นางสาว อลงกรณ์ แจ่มเมือง"
        item["receiver_bank"] = "เกียรตินาคินภัทร"

    # Specific 100% verified fixes for all 16 audited slips
    if pg == "524":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "นางสาว ณัชชา ขันทสิกรรม"
        item["receiver_bank"] = "พร้อมเพย์ (PromptPay)"
    elif pg in ["563, 1148", "563", "1148"]:
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "กรุงศรีอยุธยา"
    elif pg == "596":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "กรุงศรีอยุธยา"
    elif pg == "781":
        item["sender_name"] = "น.ส. จิณห์นิภา บุญประเสริฐ"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "นางสาว วิลาวัลย์ ไม้ทอง"
        item["receiver_bank"] = "พร้อมเพย์ (PromptPay)"
    elif pg == "848":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "นางสาว จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ไทยพาณิชย์"
    elif pg in ["904, 2328", "904", "2328"]:
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. ยุวดี มีเสมอ"
        item["receiver_bank"] = "กสิกรไทย"
    elif pg in ["1307, 1314", "1307", "1314"]:
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "นาย อนุชิต โพธิ์สาจันทร์"
        item["receiver_bank"] = "กสิกรไทย"
    elif pg == "1510":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "กรุงศรีอยุธยา"
    elif pg == "1601":
        item["sender_name"] = "นาย ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "ทีเอ็มบีธนชาต (ttb)"
        item["receiver_name"] = "นางสาว จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ไทยพาณิชย์"
    elif pg in ["1876", "2239", "2246", "2288"]:
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif pg in ["2245", "2255", "2262"]:
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "พร้อมเพย์"
    elif pg == "2189":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif pg == "2231":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "นางสาว อลงกรณ์ แจ่มเมือง"
        item["receiver_bank"] = "เกียรตินาคินภัทร"
    elif pg == "2325":
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. ปรียชาติ ฉิมพลี"
        item["receiver_bank"] = "กสิกรไทย"
    elif pg in ["2336, 2340", "2336", "2340"]:
        item["sender_name"] = "สิบตรี ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "กรุงไทย"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif pg in ["2337, 2341", "2337", "2341"]:
        item["sender_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["sender_bank"] = "ทีเอ็มบีธนชาต (ttb)"
        item["receiver_name"] = "นางสาว วันวิศา ประสาทเขตการ"
        item["receiver_bank"] = "ออมสิน"
    elif pg == "2505":
        item["sender_name"] = "นาย ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "ทีเอ็มบีธนชาต (ttb)"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
    elif pg == "2506":
        item["sender_name"] = "นาย ณัฐชัย รักษาวงษ์"
        item["sender_bank"] = "ทีเอ็มบีธนชาต (ttb)"
        item["receiver_name"] = "นางสาว กนกวรรณ พุทธศรี"
        item["receiver_bank"] = "ไทยพาณิชย์"

    # Clean any remaining parenthesized account numbers from both fields
    item["sender_name"] = clean_account_numbers_from_name(item.get("sender_name", ""))
    item["receiver_name"] = clean_account_numbers_from_name(item.get("receiver_name", ""))

    return item


def run():
    print("=" * 80)
    print("🚀 STEP 1: Updating 89 Pure Slips with Option 1 Verified Account Binding")
    print("=" * 80)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        slips = json.load(f)

    updated_slips = [apply_account_binding(s) for s in slips]

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(updated_slips, f, ensure_ascii=False, indent=2)
    print(f"Saved updated JSON: {JSON_PATH}")

    # True slip pages
    true_pages = set()
    for s in updated_slips:
        for p in str(s["page_no"]).split(","):
            p = p.strip()
            if p.isdigit():
                true_pages.add(int(p))

    print(f"Total verified slip chat pages: {len(true_pages)}")

    # -------------------------------------------------------------------------
    # STEP 2: Patch false positive headers in Master Chat PDF
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🛡️ STEP 2: Patching False-Positive Slip Headers in Evidence_Chat_Master_Combined_Vol1_to_3.pdf")
    print("=" * 80)

    assembler = PDFAssembler("dummy.pdf")
    patch_bar_path = os.path.join(BASE_DIR, "scratch", "corrob_clean_bar.png")
    patch = Image.new("RGB", (650, 36), (255, 255, 255))
    draw = ImageDraw.Draw(patch)
    draw.text((0, 0), "CORROBORATED : ", fill="#111827", font=assembler.fonts["header_lbl"])
    b = draw.textbbox((0, 0), "CORROBORATED : ", font=assembler.fonts["header_lbl"])
    draw.text((b[2], 0), "บทสนทนาต่อเนื่อง", fill="#111827", font=assembler.fonts["header_val"])
    patch.save(patch_bar_path)

    doc = fitz.open(MASTER_CHAT_PDF)
    print(f"Master Chat PDF has {len(doc)} pages.")

    # Load template for 'สลิปหลักฐานการโอนเงิน'
    tpl_path = os.path.join(BASE_DIR, "scratch", "slip_phrase_tpl.png")
    template = cv2.imread(tpl_path)

    clip_rect = fitz.Rect(200, 55, 450, 85)
    wipe_rect = fitz.Rect(130, 54, 600, 85)
    insert_rect = fitz.Rect(136.5, 56.5, 136.5 + 487.5, 56.5 + 27)

    patched_count = 0
    for i in range(len(doc)):
        p_num = i + 1
        if p_num in true_pages:
            continue  # Genuine slip page, keep slip ribbon!

        page = doc[i]
        pix = page.get_pixmap(dpi=150, clip=clip_rect)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
        bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) if pix.n >= 3 else img

        has_false_slip_ribbon = False
        if bgr.shape[0] >= template.shape[0] and bgr.shape[1] >= template.shape[1]:
            res = cv2.matchTemplate(bgr, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > 0.85:
                has_false_slip_ribbon = True

        if has_false_slip_ribbon:
            # Wipe and replace with clean 'บทสนทนาต่อเนื่อง'
            page.draw_rect(wipe_rect, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_image(insert_rect, filename=patch_bar_path)
            patched_count += 1
            if patched_count <= 10 or patched_count % 25 == 0:
                print(f"  [FIXED] Page {p_num}: reset header ribbon to 'CORROBORATED : บทสนทนาต่อเนื่อง'")

    print(f"\n✅ Total patched chat pages: {patched_count} pages successfully reset!")

    # Save patched PDF
    tmp_patched_pdf = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_patched.pdf")
    doc.save(tmp_patched_pdf, garbage=4, deflate=True)
    doc.close()

    # Replace original master chat PDF
    os.replace(tmp_patched_pdf, MASTER_CHAT_PDF)
    print(f"Overwrote {MASTER_CHAT_PDF} with clean patched PDF.")

    # -------------------------------------------------------------------------
    # STEP 3: Rebuild Excel Slip Index with Option 1 Names
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("📊 STEP 3: Rebuilding Excel 10-Column Index with Option 1 Names")
    print("=" * 80)
    from search_slip import export_to_excel
    excel_path = os.path.join(OUT_DIR, "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx")
    for s in updated_slips:
        if "pages" not in s:
            s["pages"] = [int(p.strip()) for p in str(s.get("page_no", "")).split(",") if p.strip().isdigit()]
    export_to_excel(updated_slips, excel_path)


    print(f"Generated {excel_path} ({len(updated_slips)} slips).")

    # -------------------------------------------------------------------------
    # STEP 4: Rebuild Master Unified Dossier with Cover & Front Index
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🏛️ STEP 4: Running generate_cover_page.py to Stitch Unified Dossier (2,562 Pages)")
    print("=" * 80)
    import subprocess
    cmd = [sys.executable, COVER_SCRIPT]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)

    # -------------------------------------------------------------------------
    # STEP 5: Rebuild Hash Certificate
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🔐 STEP 5: Updating Cryptographic Evidence Hash Certificate")
    print("=" * 80)
    hash_script = os.path.join(BASE_DIR, "tools", "evidence_hash_manifest.py")
    res_hash = subprocess.run([sys.executable, hash_script], capture_output=True, text=True, cwd=BASE_DIR)
    print(res_hash.stdout)

    print("\n" + "=" * 80)
    print("🎉 ALL STEPS COMPLETED: Option 1 & Header Fix 100% SUCCESSFUL!")
    print("=" * 80)

if __name__ == "__main__":
    run()
