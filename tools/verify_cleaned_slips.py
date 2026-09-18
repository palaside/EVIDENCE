import json
import re
import sys

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

JSON_PATH = "Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total entries currently: {len(data)}")

# Items that are confirmed NOT slips (food, selfie, phone call screenshot with no amount/no bank)
NON_SLIP_PAGES = {"75", "933", "1309", "1379", "2048", "2273"}

cleaned_slips = []
idx_counter = 1

THAI_MONTH_NAMES = {
    1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.",
    5: "พ.ค.", 6: "มิ.ย.", 7: "ก.ค.", 8: "ส.ค.",
    9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
}

def normalize_date(raw_dt, ref_id, page_no):
    # Specific manual overrides for pages we directly verified from high-res image:
    if page_no == "408":
        return "09 ก.พ. 2568 - 14:20"
    if page_no == "1071":
        return "18 มี.ค. 2568 - 14:57"
    if page_no == "1074":
        return "18 มี.ค. 2568 - 15:42"
    if page_no == "1068":
        return "18 มี.ค. 2568 - 11:03"

    raw_dt = raw_dt.strip() if raw_dt else ""
    raw_dt = re.sub(r"\s+", " ", raw_dt.replace("\n", " ")).strip()
    
    # Check ref_id ISO format: 2025MMDDHHMM...
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

    rm = raw_month.strip(".- ,")
    
    if any(rm.lower() == k for k in ["u.a", "ua", "u.a.", "y.a", "h.a", "ม.ค", "มค", "u"]):
        clean_m = "ม.ค."
    elif any(rm.lower() == k for k in ["n.w", "nw", "n.w.", "ก.พ", "กพ"]):
        clean_m = "ก.พ."
    elif any(rm.lower() == k for k in ["gn", "gn.", "&.a", "&a", "g.a", "ga", "i.a", "ia", ".a", "a", "b.a", "ba", "g.a.", "มี.ค", "มีค", "j.a", "d.a"]):
        clean_m = "มี.ค."
    elif any(rm.lower() == k for k in ["w.9", "w9", "tw.u", "tw.ย", "tw.e", "tu.e", "เu.ย", "w.e", "w.g", "ww.8", "ww.g", "u.8", "ww.d", "w.8", "tw.n", "เม.ย", "เมย", "w.g.", "ww.g."]):
        clean_m = "เม.ย."
    elif any(rm.lower() == k for k in ["waa", "waa.", "w.a", "wa", "w.n", "wn", "w.ค", "w.a.", "พ.ค", "พค", "w.fa", "w.fa."]):
        clean_m = "พ.ค."
    elif any(rm.lower() == k for k in ["i.u", "i.u.", "0.8", "o.8", "g.e", "&.e", "u.e", "มิ.ย", "มิย", ".g"]):
        clean_m = "มิ.ย."
    elif any(rm.lower() == k for k in ["n.a", "na", "n.a.", "ก.ค", "กค"]):
        clean_m = "ก.ค."
    elif any(rm.lower() == k for k in ["a.n", "an", "a.n.", "a.a", "aa", "a.a.", "ส.ค", "สค"]):
        clean_m = "ส.ค."
    elif any(rm.lower() == k for k in ["n.e", "ne", "n.9", "ก.ย", "กย"]):
        clean_m = "ก.ย."
    elif any(rm.lower() == k for k in ["m.a", "ma", "ต.ค", "ตค"]):
        clean_m = "ต.ค."
    elif any(rm.lower() == k for k in ["w.e", "พ.ย", "พย"]):
        clean_m = "พ.ย."
    elif any(rm.lower() == k for k in ["s.a", "sa", "ธ.ค", "ธค"]):
        clean_m = "ธ.ค."
    else:
        clean_m = raw_month

    res = f"{day:02d} {clean_m} {year}"
    if time_str:
        res += f" - {time_str}"
    return res

for item in data:
    pg = str(item.get("page_no", "")).split(",")[0].strip()
    if pg in NON_SLIP_PAGES:
        print(f"Skipping non-slip item at page {pg} (food/photo)")
        continue

    # Fix item 32 (page 1071)
    if pg == "1071":
        item["amount"] = "5,000.00"
        item["receiver_bank"] = "ไทยพาณิชย์"
        item["sender_bank"] = "กรุงไทย"
        item["sender_name"] = "น.ส. จิณห์นิภา บุญประเสริฐ (XXX-X-XX764-0)"
        item["receiver_name"] = "นาย พงศ์ภิระ สิงห์เถื่อน (XXX-X-XX630-1)"
        item["ref_id"] = "A37446e6122a34ffa"

    # Fix item 15 (page 408)
    if pg == "408":
        item["sender_name"] = "ณัฐชัย รักษาวงษ์ (XXX-X-XX452-9)"
        item["receiver_name"] = "น.ส. จิณห์นิภา ประสาทเขตการ (XXX-X-XX385-0)"
        item["receiver_bank"] = "กรุงศรีอยุธยา"

    # Fix item 33 (page 1074)
    if pg == "1074":
        item["sender_name"] = "น.ส. ยุวดี ม (xxx-x-x2717-x)"
        item["receiver_name"] = "นาย ณัฐชัย รักษาวงษ์ (xxx-x-x7558-x)"
        item["sender_bank"] = "กสิกรไทย"
        item["receiver_bank"] = "ทีเอ็มบีธนชาต (ttb)"
        item["ref_id"] = "015077154243AOR01083"

    # Fix item 31 (page 1068)
    if pg == "1068":
        item["sender_bank"] = "กรุงไทย"
        item["receiver_bank"] = "กรุงไทย"
        item["sender_name"] = "สิบตรีณัฐชัย รักษาวงษ์ (XXX-X-XX526-6)"
        item["receiver_name"] = "น.ส. จิณห์นิภา บุญประเสริฐ (XXX-X-XX764-0)"
        item["ref_id"] = "N006728239785025333486297"

    item["index"] = idx_counter
    item["date_time"] = normalize_date(item.get("date_time", ""), item.get("ref_id", ""), pg)
    idx_counter += 1
    cleaned_slips.append(item)

print(f"\nRemaining pure financial slips: {len(cleaned_slips)}")

# Check if any slip still has '-' or bad date
bad_dates = [s for s in cleaned_slips if s["date_time"] == "-" or not s["date_time"] or any(c in s["date_time"] for c in ["Gn", "&", "i.A", ".A.", "w.9", "waa"])]
print(f"Any remaining bad/corrupted dates: {len(bad_dates)}")
for b in bad_dates:
    print(f"  idx={b['index']} pg={b['page_no']} dt={b['date_time']}")
