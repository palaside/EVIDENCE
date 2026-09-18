import json
import re
import os
import sys

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

JSON_PATH = r"d:\Project\DIGITAL_EVIDENCE\Folder_Out\Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json"

THAI_MONTH_NAMES = {
    1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.",
    5: "พ.ค.", 6: "มิ.ย.", 7: "ก.ค.", 8: "ส.ค.",
    9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
}

def clean_and_normalize_datetime(raw_dt, ref_id, page_no):
    raw_dt = raw_dt.strip() if raw_dt else ""
    raw_dt = re.sub(r"\s+", " ", raw_dt.replace("\n", " ")).strip()
    
    # 1. First priority: Check if ref_id contains exact 2025 timestamp (e.g., 202504151902531655)
    m_ref = re.match(r"^2025(0[1-9]|1[0-2])([0-3]\d)([0-2]\d)([0-5]\d)", ref_id or "")
    if m_ref:
        m_num = int(m_ref.group(1))
        d_num = int(m_ref.group(2))
        h_str = m_ref.group(3)
        min_str = m_ref.group(4)
        m_thai = THAI_MONTH_NAMES.get(m_num, "")
        if m_thai and 1 <= d_num <= 31:
            return f"{d_num:02d} {m_thai} 2568 - {h_str}:{min_str}"
            
    if not raw_dt or raw_dt == "-":
        return "-"

    # 2. Extract components: Day, Garbled Month, Year, Time
    # e.g., "01 Gn. 2568 - 09:45" or "03 &.A. 2568 - 22:49" or "20 n.w. 2568 - 11:57"
    m = re.match(r"^(\d{1,2})\s+([^\s]+)\s+(256\d)\s*(?:-\s*(\d{1,2}:\d{2}))?$", raw_dt)
    if not m:
        m = re.match(r"^(\d{1,2})\s+([^\s]+)\s+(?:-\s*(\d{1,2}:\d{2}))?$", raw_dt)
        if m:
            day = int(m.group(1))
            raw_month = m.group(2)
            year = "2568"
            time_str = m.group(3) or ""
        else:
            return raw_dt
    else:
        day = int(m.group(1))
        raw_month = m.group(2)
        year = m.group(3)
        time_str = m.group(4) or ""

    # Clean raw_month token
    rm = raw_month.strip(".- ,")
    
    # Map OCR confusion to correct month
    # Month 1: ม.ค.
    if any(rm.lower() == k for k in ["u.a", "ua", "u.a.", "y.a", "h.a", "ม.ค", "มค", "u"]):
        # Check context: if page > 800 or day/context indicates later month
        clean_m = "ม.ค."
    # Month 2: ก.พ.
    elif any(rm.lower() == k for k in ["n.w", "nw", "n.w.", "n.w", "ก.พ", "กพ", "n.w."]):
        clean_m = "ก.พ."
    # Month 3: มี.ค.
    elif any(rm.lower() == k for k in ["gn", "gn.", "&.a", "&a", "g.a", "ga", "i.a", "ia", ".a", "a", "b.a", "ba", "g.a.", "มี.ค", "มีค", "j.a", "d.a"]):
        clean_m = "มี.ค."
    # Month 4: เม.ย.
    elif any(rm.lower() == k for k in ["w.9", "w9", "tw.u", "tw.ย", "tw.e", "tu.e", "เu.ย", "w.e", "w.g", "ww.8", "ww.g", "u.8", "ww.d", "w.8", "tw.n", "เม.ย", "เมย", "w.g.", "ww.g."]):
        clean_m = "เม.ย."
    # Month 5: พ.ค.
    elif any(rm.lower() == k for k in ["waa", "waa.", "w.a", "wa", "w.n", "wn", "w.ค", "w.a.", "พ.ค", "พค", "w.fa", "w.fa."]):
        clean_m = "พ.ค."
    # Month 6: มิ.ย.
    elif any(rm.lower() == k for k in ["i.u", "i.u.", "0.8", "o.8", "g.e", "&.e", "u.e", "มิ.ย", "มิย", ".g"]):
        clean_m = "มิ.ย."
    # Month 7: ก.ค.
    elif any(rm.lower() == k for k in ["n.a", "na", "n.a.", "ก.ค", "กค"]):
        clean_m = "ก.ค."
    # Month 8: ส.ค.
    elif any(rm.lower() == k for k in ["a.n", "an", "a.n.", "a.a", "aa", "a.a.", "ส.ค", "สค"]):
        clean_m = "ส.ค."
    # Month 9: ก.ย.
    elif any(rm.lower() == k for k in ["n.e", "ne", "n.9", "ก.ย", "กย"]):
        clean_m = "ก.ย."
    # Month 10: ต.ค.
    elif any(rm.lower() == k for k in ["m.a", "ma", "ต.ค", "ตค"]):
        clean_m = "ต.ค."
    # Month 11: พ.ย.
    elif any(rm.lower() == k for k in ["w.e", "พ.ย", "พย"]):
        clean_m = "พ.ย."
    # Month 12: ธ.ค.
    elif any(rm.lower() == k for k in ["s.a", "sa", "ธ.ค", "ธค"]):
        clean_m = "ธ.ค."
    else:
        clean_m = raw_month

    res = f"{day:02d} {clean_m} {year}"
    if time_str:
        res += f" - {time_str}"
    return res

if __name__ == "__main__":
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        old_dt = item.get("date_time", "")
        ref = item.get("ref_id", "")
        pg = item.get("page_no", "")
        new_dt = clean_and_normalize_datetime(old_dt, ref, pg)
        if old_dt != new_dt:
            print(f"[{item['index']:02d}] Pg {pg} | OLD: '{old_dt}' -> NEW: '{new_dt}'")
