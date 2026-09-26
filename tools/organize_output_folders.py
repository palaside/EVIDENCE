import os
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FOLDER_OUT = PROJECT_ROOT / "Folder_Out"

# Definition of the 7 Structured Group Folders
GROUPS = {
    "01": {
        "dir_name": "01_[ชุดล่าสุด_25กย68]_สลิปการเงิน_95_รายการ",
        "title": "ชุดล่าสุด (25 ก.ย. 2568) — สลิปการเงิน 95 รายการ (Fit Summary & Statement)",
        "desc": "ผลลัพธ์การประมวลผลสลิปการเงินสมบูรณ์แบบล่าสุด 95 ใบ จัดวางกึ่งกลางบล็อก 645x890 พร้อมตารางบัญชี Statement 10 คอลัมน์",
        "files": [
            ("Evidence_Slips_95_Fit_Summary.pdf", "(1) เล่มสลิปเดี่ยวและตารางสรุป_Evidence_Slips_95_Fit_Summary.pdf"),
            ("Evidence_Slips_95_Statement.xlsx", "(2) ตารางบัญชีสารบัญคดี_Evidence_Slips_95_Statement.xlsx")
        ]
    },
    "02": {
        "dir_name": "02_[ชุดหลัก_ส่งศาล]_เล่มแชท_Master_Combined_Vol1-3",
        "title": "ชุดหลักส่งศาล (19 ก.ย. 2568) — เล่มแชท Master Combined Vol 1-3 (2,557 หน้า)",
        "desc": "เล่มพยานหลักฐานบทสนทนาแชทต่อเนื่องครบ 3 เล่ม ผสานหน้าปก สารบัญสลิป 10 คอลัมน์ และใบรับรองดิจิทัลแฮช SHA-256",
        "files": [
            ("Evidence_Chat_Master_Front_Cover_and_Index.pdf", "(1) หน้าปกและสารบัญสลิป_Evidence_Chat_Master_Front_Cover_and_Index.pdf"),
            ("Evidence_Chat_Master_Combined_Vol1_to_3.pdf", "(2) เล่มหลักฐานแชทฉบับสมบูรณ์_Evidence_Chat_Master_Combined_Vol1_to_3.pdf"),
            ("Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx", "(3) บัญชีสารบัญสลิปคดี_Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx"),
            ("Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json", "(4) ดัชนีสลิปข้อมูลดิบ_Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json"),
            ("EVIDENCE_HASH_CERTIFICATE.pdf", "(5) ใบรับรองความถูกต้องดิจิทัลแฮช_EVIDENCE_HASH_CERTIFICATE.pdf"),
            ("EVIDENCE_HASH_MANIFEST.json", "(6) ทะเบียนดิจิทัลแฮช_EVIDENCE_HASH_MANIFEST.json"),
            ("EVIDENCE_HASH_MANIFEST.sha256", "(7) เช็คซัมตรวจสอบไฟล์_EVIDENCE_HASH_MANIFEST.sha256")
        ]
    },
    "03": {
        "dir_name": "03_[ชุดแยกเล่ม_3เล่ม]_เล่มแชท_Volume_1_2_3",
        "title": "ชุดแยกเล่ม (19 ก.ย. 2568) — เล่มแชทแยกรายเล่ม Volume 1, Volume 2, Volume 3",
        "desc": "เล่มพยานหลักฐานแชทแยกตามโฟลเดอร์ต้นทาง 1, 2, 3 พร้อมบัญชีสารบัญสลิปประจำแต่ละเล่ม",
        "files": [
            ("Evidence_Chat_Volume_1.pdf", "(1) เล่มแชทที่ 1_Evidence_Chat_Volume_1.pdf"),
            ("Evidence_Chat_Volume_1_Slip_Index.xlsx", "(2) สารบัญสลิปเล่ม 1_Evidence_Chat_Volume_1_Slip_Index.xlsx"),
            ("Evidence_Chat_Volume_1_Slip_Index.json", "(3) ดัชนีสลิปเล่ม 1_Evidence_Chat_Volume_1_Slip_Index.json"),
            ("Evidence_Chat_Volume_2.pdf", "(4) เล่มแชทที่ 2_Evidence_Chat_Volume_2.pdf"),
            ("Evidence_Chat_Volume_2_Slip_Index.xlsx", "(5) สารบัญสลิปเล่ม 2_Evidence_Chat_Volume_2_Slip_Index.xlsx"),
            ("Evidence_Chat_Volume_2_Slip_Index.json", "(6) ดัชนีสลิปเล่ม 2_Evidence_Chat_Volume_2_Slip_Index.json"),
            ("Evidence_Chat_Volume_3.pdf", "(7) เล่มแชทที่ 3_Evidence_Chat_Volume_3.pdf"),
            ("Evidence_Chat_Volume_3_Slip_Index.xlsx", "(8) สารบัญสลิปเล่ม 3_Evidence_Chat_Volume_3_Slip_Index.xlsx"),
            ("Evidence_Chat_Volume_3_Slip_Index.json", "(9) ดัชนีสลิปเล่ม 3_Evidence_Chat_Volume_3_Slip_Index.json")
        ]
    },
    "04": {
        "dir_name": "04_[ชุดบุคคลเป้าหมาย]_พยานหลักฐาน_จิณห์นิภา_ประสาทเขตการ",
        "title": "ชุดบุคคลเป้าหมาย — น.ส. จิณห์นิภา ประสาทเขตการ",
        "desc": "พยานหลักฐานเฉพาะรายการธุรกรรมที่เชื่อมโยงกับบุคคลเป้าหมายโดยตรง ทั้งในรูปแบบเล่มสลิปและตารางบัญชี",
        "files": [
            ("Evidence_Target_จิณห์นิภา_ประสาทเขตการ.pdf", "(1) เล่มหลักฐานบุคคลเป้าหมาย_Evidence_Target_จิณห์นิภา_ประสาทเขตการ.pdf"),
            ("Evidence_Target_จิณห์นิภา_ประสาทเขตการ.xlsx", "(2) ตารางบัญชีบุคคลเป้าหมาย_Evidence_Target_จิณห์นิภา_ประสาทเขตการ.xlsx")
        ]
    },
    "05": {
        "dir_name": "05_[ชุดรายงานและใบรับรอง]_Audit_and_Certificates",
        "title": "ชุดรายงานการตรวจสอบ — Audit & Quality Inspection Reports",
        "desc": "บันทึกและรายงานสรุปการตรวจสอบคุณภาพความสมบูรณ์ของหลักฐาน ตรวจจับสลิปซ้ำ และผลการตรวจด้วย Typhoon OCR",
        "files": [
            ("QUALITY_INSPECTION_REPORT.md", "(1) รายงานตรวจคุณภาพแชท_QUALITY_INSPECTION_REPORT.md"),
            ("QUALITY_INSPECTION_REPORT_20260919_032912.md", "(2) บันทึกตรวจคุณภาพฉบับสมบูรณ์_QUALITY_INSPECTION_REPORT_20260919_032912.md"),
            ("TYPHOON_AUDIT_REPORT.json", "(3) ผลตรวจสอบสลิปด้วยTyphoon_TYPHOON_AUDIT_REPORT.json"),
            ("DUPLICATE_SLIP_AUDIT_REPORT.xlsx", "(4) รายงานตรวจสอบสลิปซ้ำ_DUPLICATE_SLIP_AUDIT_REPORT.xlsx"),
            ("all_89_slips_details.txt", "(5) รายละเอียดสลิป89รายการ_all_89_slips_details.txt"),
            ("all_slips_summary.txt", "(6) สรุปยอดรวมสลิป_all_slips_summary.txt"),
            ("check_slips.json", "(7) ข้อมูลตรวจสอบสลิป_check_slips.json"),
            ("special_items.json", "(8) รายการสลิปกรณีพิเศษ_special_items.json")
        ]
    },
    "06": {
        "dir_name": "06_[คลังเวอร์ชันเก่าและไฟล์ทดสอบ]_Archive_and_Legacy",
        "title": "คลังเวอร์ชันเก่าและไฟล์ทดสอบ — Archive & Legacy Versions",
        "desc": "เวอร์ชันทดสอบในอดีต (สลิปรอบแรก 6 ก.ย. 68, สลิป 560 ใบ 15 ก.ย. 68, และไฟล์ทดสอบระบบต่างๆ)",
        "files": [
            ("(1) 2026-09-06_Evidence_Slips_Centered.pdf", "(01) 2026-09-06_Evidence_Slips_Centered.pdf"),
            ("(2) 2026-09-06_Evidence_Slips_Complete.pdf", "(02) 2026-09-06_Evidence_Slips_Complete.pdf"),
            ("(3) 2026-09-06_Evidence_Slips_Final_10Col.pdf", "(03) 2026-09-06_Evidence_Slips_Final_10Col.pdf"),
            ("(4) 2026-09-06_Evidence_Slips_Full_Summary.pdf", "(04) 2026-09-06_Evidence_Slips_Full_Summary.pdf"),
            ("(5) 2026-09-06_Evidence_Slips_Landscape_Summary.pdf", "(05) 2026-09-06_Evidence_Slips_Landscape_Summary.pdf"),
            ("(6) 2026-09-06_A4_IMG_Slip_Data.json", "(06) 2026-09-06_A4_IMG_Slip_Data.json"),
            ("(7) 2026-09-15_Evidence_Slips_Master_Unique_560.pdf", "(07) 2026-09-15_Evidence_Slips_Master_Unique_560.pdf"),
            ("(8) 2026-09-15_Evidence_Slips_Master_Unique_560.xlsx", "(08) 2026-09-15_Evidence_Slips_Master_Unique_560.xlsx"),
            ("(9) 2026-09-14_Evidence_Slips_Summary.xlsx", "(09) 2026-09-14_Evidence_Slips_Summary.xlsx"),
            ("(10) 2026-09-14_Slip_Evidence_20260914_134410.xlsx", "(10) 2026-09-14_Slip_Evidence_20260914_134410.xlsx"),
            ("(11) 2026-09-14_Test_Extraction_KTB_TTB_40Slips.json", "(11) 2026-09-14_Test_Extraction_KTB_TTB_40Slips.json"),
            ("(12) 2026-09-14_Test_Extraction_KTB_TTB_40Slips.xlsx", "(12) 2026-09-14_Test_Extraction_KTB_TTB_40Slips.xlsx"),
            ("(13) 2026-09-14_Test_Extraction_KTB_TTB_40Slips_MaskedPII.xlsx", "(13) 2026-09-14_Test_Extraction_KTB_TTB_40Slips_MaskedPII.xlsx"),
            ("(14) 2026-09-14_slips_dedup_manifest.json", "(14) 2026-09-14_slips_dedup_manifest.json"),
            ("(15) 2026-09-12_แชทท__ 1.pdf", "(15) 2026-09-12_แชทท__ 1.pdf"),
            ("(16) 2026-09-18_Pattle_Case_Evidence_Test.exe", "(16) 2026-09-18_Pattle_Case_Evidence_Test.exe"),
            ("(17) 2026-09-18_Pattle_Case_Evidence_Test.exe.sha256", "(17) 2026-09-18_Pattle_Case_Evidence_Test.exe.sha256"),
            ("(18) 2026-09-24_Front_Cover_Index.xlsx", "(18) 2026-09-24_Front_Cover_Index.xlsx"),
            ("(19) 2026-09-24_Front_Cover_Index.json", "(19) 2026-09-24_Front_Cover_Index.json"),
            ("(20) REV02_20260924_022015_d5b4072d.json", "(20) REV02_20260924_022015_d5b4072d.json"),
            ("(21) REV02_20260924_022015_d5b4072d.xlsx", "(21) REV02_20260924_022015_d5b4072d.xlsx"),
            ("(22) REV02_20260924_022221_84b91941.json", "(22) REV02_20260924_022221_84b91941.json"),
            ("(23) REV02_20260924_022221_84b91941.xlsx", "(23) REV02_20260924_022221_84b91941.xlsx"),
            ("(24) REV02_20260924_022330_3c73513e.json", "(24) REV02_20260924_022330_3c73513e.json"),
            ("(25) REV02_20260924_022330_3c73513e.xlsx", "(25) REV02_20260924_022330_3c73513e.xlsx"),
            ("(26) REV02_20260924_023031_64d5521c.json", "(26) REV02_20260924_023031_64d5521c.json"),
            ("(27) REV02_20260924_023031_64d5521c.xlsx", "(27) REV02_20260924_023031_64d5521c.xlsx"),
        ]
    },
    "07": {
        "dir_name": "07_[ระบบและไฟล์แคช]_System_Caches",
        "title": "ระบบและไฟล์แคช — System AI & OCR Caches",
        "desc": "ไฟล์แคชของโมเดล AI (Typhoon, Gemini, EasyOCR) เพื่อความเร็วสูงและประหยัด Token",
        "files": [
            ("typhoon_cache.json", "(1) แคช_typhoon_cache.json"),
            ("gemini_fallback_cache.json", "(2) แคช_gemini_fallback_cache.json"),
            ("slips_ocr_cache.json", "(3) แคช_slips_ocr_cache.json")
        ]
    }
}

# Critical cache files that should remain accessible at Folder_Out root via hardlink
CRITICAL_CACHE_FILES = [
    "typhoon_cache.json",
    "gemini_fallback_cache.json",
    "slips_ocr_cache.json",
    "Evidence_Chat_Master_Combined_Vol1_to_3.pdf"
]

def organize():
    print("=== เริ่มกระบวนการจัดกลุ่มไฟล์ Folder_Out ===")
    
    # 1. Create Directories
    for gid, ginfo in GROUPS.items():
        target_dir = FOLDER_OUT / ginfo["dir_name"]
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 สร้างโฟลเดอร์: {ginfo['dir_name']}")

    # 2. Move / Hardlink Files
    moved_count = 0
    for gid, ginfo in GROUPS.items():
        target_dir = FOLDER_OUT / ginfo["dir_name"]
        for orig_name, new_name in ginfo["files"]:
            src = FOLDER_OUT / orig_name
            dst = target_dir / new_name
            
            if src.exists() and src.is_file():
                if orig_name in CRITICAL_CACHE_FILES:
                    # Use hardlink for critical files to keep root compatibility
                    try:
                        if dst.exists():
                            dst.unlink()
                        os.link(str(src), str(dst))
                        print(f"   [LINK] {orig_name} -> {ginfo['dir_name']}/{new_name}")
                        moved_count += 1
                    except Exception as e:
                        shutil.copy2(str(src), str(dst))
                        print(f"   [COPY] {orig_name} -> {ginfo['dir_name']}/{new_name}")
                        moved_count += 1
                else:
                    # Move other files directly
                    try:
                        if dst.exists():
                            dst.unlink()
                        shutil.move(str(src), str(dst))
                        print(f"   [MOVE] {orig_name} -> {ginfo['dir_name']}/{new_name}")
                        moved_count += 1
                    except Exception as e:
                        print(f"   ⚠️ ไม่สามารถย้าย {orig_name}: {e}")

    # Move Reference_Archives into Group 06 if exists
    ref_arch_src = FOLDER_OUT / "Reference_Archives"
    ref_arch_dst = FOLDER_OUT / GROUPS["06"]["dir_name"] / "Reference_Archives"
    if ref_arch_src.exists() and not ref_arch_dst.exists():
        try:
            shutil.move(str(ref_arch_src), str(ref_arch_dst))
            print("   [MOVE] Reference_Archives -> Group 06")
        except Exception as e:
            print(f"   ⚠️ Move Reference_Archives error: {e}")

    # 3. Create Clean Guide / Index (TXT & MD)
    catalog_txt = FOLDER_OUT / "00_สารบัญจัดกลุ่มพยานหลักฐาน.txt"
    with open(catalog_txt, "w", encoding="utf-8") as f:
        f.write("========================================================================================\n")
        f.write("  สารบัญและคู่มือจัดกลุ่มพยานหลักฐาน DIGITAL EVIDENCE (ลำดับชุดและเวอร์ชันเอกสาร)\n")
        f.write("========================================================================================\n\n")
        f.write("เอกสารทั้งหมดใน Folder_Out ได้รับการจัดกลุ่มออกเป็นชุดที่ออกพร้อมกัน เรียงตามความสำคัญ\n")
        f.write("และใส่หมายเลขนำหน้า (1), (2), (3)... เพื่อให้เปิดดูได้ตรงตามลำดับขั้นตอนคดี:\n\n")
        
        for gid, ginfo in GROUPS.items():
            f.write(f"----------------------------------------------------------------------------------------\n")
            f.write(f"📁 {ginfo['dir_name']}\n")
            f.write(f"   • หัวข้อ: {ginfo['title']}\n")
            f.write(f"   • คำอธิบาย: {ginfo['desc']}\n")
            f.write(f"   • ไฟล์ในชุด:\n")
            target_dir = FOLDER_OUT / ginfo["dir_name"]
            if target_dir.exists():
                for item in sorted(target_dir.iterdir()):
                    if item.is_file():
                        sz_mb = item.stat().st_size / (1024 * 1024)
                        sz_str = f"{sz_mb:.2f} MB" if sz_mb >= 1.0 else f"{item.stat().st_size / 1024:.1f} KB"
                        f.write(f"      - {item.name:<65} ({sz_str})\n")
            f.write("\n")

    catalog_md = FOLDER_OUT / "00_สารบัญจัดกลุ่มพยานหลักฐาน.md"
    with open(catalog_md, "w", encoding="utf-8") as f:
        f.write("# 📑 สารบัญและคู่มือจัดกลุ่มพยานหลักฐาน DIGITAL EVIDENCE\n\n")
        f.write("> จัดกลุ่มเอกสารที่ประมวลผลออกพร้อมกันเป็น **ชุดเดียวกัน** เรียงลำดับความสำคัญ พร้อมหมายเลขกำกับ `(1)`, `(2)`, `(3)`... ตามลำดับขั้นตอนคดี\n\n")
        for gid, ginfo in GROUPS.items():
            f.write(f"## 📁 {ginfo['title']}\n")
            f.write(f"- **โฟลเดอร์:** `{ginfo['dir_name']}`\n")
            f.write(f"- **คำอธิบาย:** {ginfo['desc']}\n\n")
            f.write("| ลำดับ | ชื่อไฟล์พยานหลักฐาน | ขนาดไฟล์ |\n")
            f.write("| :---: | :--- | :---: |\n")
            target_dir = FOLDER_OUT / ginfo["dir_name"]
            if target_dir.exists():
                for item in sorted(target_dir.iterdir()):
                    if item.is_file():
                        sz_mb = item.stat().st_size / (1024 * 1024)
                        sz_str = f"{sz_mb:.2f} MB" if sz_mb >= 1.0 else f"{item.stat().st_size / 1024:.1f} KB"
                        f.write(f"| {item.name.split()[0]} | [{item.name}]({ginfo['dir_name']}/{item.name}) | {sz_str} |\n")
            f.write("\n---\n\n")

    print(f"\n✅ จัดกลุ่มสำเร็จเรียบร้อยทั้งหมด {moved_count} ไฟล์!")
    print(f"📄 สร้างสารบัญหลักที่: {catalog_txt}")
    print(f"📄 สร้างสารบัญ Markdown ที่: {catalog_md}")

if __name__ == "__main__":
    organize()
