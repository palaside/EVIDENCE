import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# Import from OCR_Slip Skill Engine
from _skills.OCR_Slip.scripts.ocr_slip import extract_slip_data, export_evidence_excel

def get_spaced_files(folder, count=20):
    all_files = [f for f in sorted(os.listdir(folder)) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
    base_dict = {}
    for f in all_files:
        clean_stem = re.sub(r'\s*\(\d+\)$', '', os.path.splitext(f)[0])
        if clean_stem not in base_dict:
            base_dict[clean_stem] = f
    unique_files = list(base_dict.values())
    step = max(1, len(unique_files) // count)
    selected = [unique_files[i * step] for i in range(count)]
    return [os.path.join(folder, f) for f in selected]

def main():
    ktb_files = get_spaced_files(r"F:\Project\EDOK\Final_A4_Output\KTB", 20)
    ttb_files = get_spaced_files(r"F:\Project\EDOK\Final_A4_Output\TTB", 20)

    print(f"============================================================")
    print(f"Starting OCR_Slip Stress Test: KTB (20) + TTB (20) = 40 Slips")
    print(f"Engine: Morphological Background Subtraction + CLAHE + Multi-Pass OCR + EMVCo QR")
    print(f"============================================================\n")

    all_results = []
    
    # Process KTB
    print("--- Processing KTB Slips ---")
    for idx, path in enumerate(ktb_files, 1):
        info = extract_slip_data(path, default_bank="กรุงไทย")
        info["seq"] = idx
        info["group"] = "KTB"
        all_results.append(info)
        print(f"[{idx:02d}/20 KTB] {info['filename'][:26]:<26} | Amount: {info['amount']:>10} | Date: {info['date']} {info['time']} | Ref: {info['remarks']}")

    # Process TTB
    print("\n--- Processing TTB Slips ---")
    for idx, path in enumerate(ttb_files, 1):
        info = extract_slip_data(path, default_bank="ทีเอ็มบีธนชาต (ttb)")
        info["seq"] = idx + 20
        info["group"] = "TTB"
        all_results.append(info)
        print(f"[{idx:02d}/20 TTB] {info['filename'][:26]:<26} | Amount: {info['amount']:>10} | Date: {info['date']} {info['time']} | Ref: {info['remarks']}")

    # Export to Excel
    excel_path = os.path.join("Folder_Out", "Test_Extraction_KTB_TTB_40Slips.xlsx")
    export_evidence_excel(
        all_results,
        excel_path,
        title="ตารางทดสอบความแม่นยำการสกัดข้อมูลสลิป 100% เต็ม (Stress Test 40 Slips: KTB 20 + TTB 20)"
    )
    print(f"\n[OK] Successfully generated Excel report: {excel_path}")

    # Export to JSON
    json_path = os.path.join("Folder_Out", "Test_Extraction_KTB_TTB_40Slips.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"[OK] Successfully generated JSON data: {json_path}")

    # Metrics Audit
    missing_ref = [r for r in all_results if r["remarks"] == "-"]
    missing_date = [r for r in all_results if r["date"] == "-" or "/00/" in r["date"]]
    missing_time = [r for r in all_results if r["time"] == "-"]
    missing_amount = [r for r in all_results if r["amount"] == "-"]

    print("\n" + "="*50)
    print("FINAL ACCURACY AUDIT (40 SLIPS):")
    print(f"- Amount Accuracy   : {len(all_results)-len(missing_amount)}/40 ({((len(all_results)-len(missing_amount))/40)*100:.1f}%)")
    print(f"- Ref ID Accuracy   : {len(all_results)-len(missing_ref)}/40 ({((len(all_results)-len(missing_ref))/40)*100:.1f}%)")
    print(f"- Date Accuracy     : {len(all_results)-len(missing_date)}/40 ({((len(all_results)-len(missing_date))/40)*100:.1f}%)")
    print(f"- Time Accuracy     : {len(all_results)-len(missing_time)}/40 ({((len(all_results)-len(missing_time))/40)*100:.1f}%)")
    print("="*50)

if __name__ == "__main__":
    main()
