import os
import sys
import json
import copy
import pandas as pd

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "Folder_Out", "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json")
XLSX_PATH = os.path.join(BASE_DIR, "Folder_Out", "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    slips = json.load(f)

print(f"Loaded {len(slips)} slip records.")

# Pixel-verified updates mapping by Page Number:
# Page -> Dict of verified fields
UPDATES = {
    358: {
        "amount": "5,500.00",
        "datetime": "08 ก.พ. 2568 - 13:09",
        "date_time": "08 ก.พ. 2568 - 13:09",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "กรุงศรีอยุธยา",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "Adc128febf3ac7477d"
    },
    372: {
        "amount": "100.00",
        "datetime": "09 ก.พ. 2568 - 14:20",
        "date_time": "09 ก.พ. 2568 - 14:20",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "กรุงศรีอยุธยา",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "Ac3124bee94824d80"
    },
    729: {
        "amount": "3,000.00",
        "datetime": "01 มี.ค. 2568 - 09:45",
        "date_time": "01 มี.ค. 2568 - 09:45",
        "sender_bank": "กรุงไทย",
        "sender_name": "น.ส. จิณห์นิภา บุญประเสริฐ",
        "receiver_bank": "พร้อมเพย์",
        "receiver_name": "นางสาว วิลาวัลย์ ไม้ทอง",
        "ref_id": "A26ca32bfdcf040b2",
        "memo": "ส่งดอกดา ดัน 15,000"
    },
    795: {
        "amount": "15,000.00",
        "datetime": "03 มี.ค. 2568 - 22:49",
        "date_time": "03 มี.ค. 2568 - 22:49",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ไทยพาณิชย์",
        "receiver_name": "นางสาว จิณห์นิภา ประสาทเขตการ",
        "ref_id": "A5d4dec10dec64dc0"
    },
    850: {
        "amount": "3,000.00",
        "datetime": "08 มี.ค. 2568 - 12:00",
        "date_time": "08 มี.ค. 2568 - 12:00",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "กรุงไทย",
        "receiver_name": "น.ส. ยุวดี มีเสมอ",
        "ref_id": "A79c94519992f4476"
    },
    958: {
        "amount": "1,000.00",
        "datetime": "15 มี.ค. 2568 - 17:27",
        "date_time": "15 มี.ค. 2568 - 17:27",
        "sender_bank": "ไทยพาณิชย์",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ไทยพาณิชย์",
        "receiver_name": "นางสาว จิณห์นิภา ประสาทเขตการ",
        "ref_id": "202503157SX54H23674"
    },
    962: {
        "amount": "300.00",
        "datetime": "15 มี.ค. 2568 - 17:33",
        "date_time": "15 มี.ค. 2568 - 17:33",
        "sender_bank": "ไทยพาณิชย์",
        "sender_name": "นางสาว จิณห์นิภา ประสาทเขตการ",
        "receiver_bank": "พร้อมเพย์",
        "receiver_name": "นางสาว ณิชชา จินตสิกรรม",
        "ref_id": "202503157SX5OZ1I3BBNJE3Zk"
    },
    1014: {
        "amount": "3,000.00",
        "datetime": "18 มี.ค. 2568 - 11:03",
        "date_time": "18 มี.ค. 2568 - 11:03",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "กรุงไทย",
        "receiver_name": "น.ส. จิณห์นิภา บุญประเสริฐ",
        "ref_id": "N006728239785025333486297"
    },
    1020: {
        "amount": "3,900.00",
        "datetime": "18 มี.ค. 2568 - 15:42",
        "date_time": "18 มี.ค. 2568 - 15:42",
        "sender_bank": "กรุงไทย",
        "sender_name": "น.ส. ยุวดี มีเสมอ",
        "receiver_bank": "กรุงไทย",
        "receiver_name": "สิบตรี ณัฐชัย รักษาวงษ์"
    },
    1220: {
        "amount": "158.00",
        "datetime": "30 มี.ค. 2568 - 12:42",
        "date_time": "30 มี.ค. 2568 - 12:42",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ไทยพาณิชย์",
        "receiver_name": "นาย อนุชิต โพธิ์สาจันทร์",
        "ref_id": "Ac30a08e1a5394464"
    },
    1549: {
        "amount": "100.00",
        "datetime": "21 เม.ย. 2568 - 13:46",
        "date_time": "21 เม.ย. 2568 - 13:46",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "กรุงศรีอยุธยา",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "Ab7ea88f7ad9d41d1"
    },
    1795: {
        "amount": "7,000.00",
        "datetime": "07 พ.ค. 2568 - 19:53",
        "date_time": "07 พ.ค. 2568 - 19:53",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ทีเอ็มบีธนชาต (ttb)",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "A4081c7ff16594c7b"
    },
    2008: {
        "amount": "200.00",
        "datetime": "16 พ.ค. 2568 - 10:28",
        "date_time": "16 พ.ค. 2568 - 10:28",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ถอนเงินสด (ATM)",
        "receiver_name": "ถอนเงินสดไม่ใช้บัตร",
        "ref_id": "A3556845723fa431e"
    },
    2111: {
        "amount": "5,600.00",
        "datetime": "26 พ.ค. 2568 - 16:52",
        "date_time": "26 พ.ค. 2568 - 16:52",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "เกียรตินาคินภัทร",
        "receiver_name": "นางสาว อลงกรณ์ แจ่มเมือง",
        "ref_id": "Aa7e0058a52854e5c"
    },
    2113: {
        "amount": "9,000.00",
        "datetime": "26 พ.ค. 2568 - 17:02",
        "date_time": "26 พ.ค. 2568 - 17:02",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ไทยพาณิชย์",
        "receiver_name": "น.ส. ปรียาภัทร อิ่มพลี",
        "ref_id": "A978432b036574f26"
    },
    2119: {
        "amount": "600.00",
        "datetime": "26 พ.ค. 2568 - 20:52",
        "date_time": "26 พ.ค. 2568 - 20:52",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ทีเอ็มบีธนชาต (ttb)",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "A9531551cbefb40fa"
    },
    2152: {
        "amount": "35,000.00",
        "datetime": "30 พ.ค. 2568 - 14:21",
        "date_time": "30 พ.ค. 2568 - 14:21",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ทีเอ็มบีธนชาต (ttb)",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "Af2cfb29c1f9e40ae",
        "memo": "ค่าทอง"
    },
    2171: {
        "amount": "9,000.00",
        "datetime": "02 มิ.ย. 2568 - 16:45",
        "date_time": "02 มิ.ย. 2568 - 16:45",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ไทยพาณิชย์",
        "receiver_name": "น.ส. ปรียาภัทร อิ่มพลี",
        "ref_id": "Adc5625bf93e0452d"
    },
    2276: {
        "amount": "1,000.00",
        "datetime": "27 มิ.ย. 2568 - 10:20",
        "date_time": "27 มิ.ย. 2568 - 10:20",
        "sender_bank": "กรุงไทย",
        "sender_name": "สิบตรี ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ทีเอ็มบีธนชาต (ttb)",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "Ae48eaec5638148c3"
    },
    2338: {
        "amount": "2,700.00",
        "datetime": "10 ก.ค. 2568 - 10:52",
        "date_time": "10 ก.ค. 2568 - 10:52",
        "sender_bank": "ทีเอ็มบีธนชาต (ttb)",
        "sender_name": "นาย ณัฐชัย รักษาวงษ์",
        "receiver_bank": "กสิกรไทย",
        "receiver_name": "นาย พัฒนะ คำไทย",
        "ref_id": "202507101001081709"
    },
    2364: {
        "amount": "5,400.00",
        "datetime": "26 ก.ค. 2568 - 10:50",
        "date_time": "26 ก.ค. 2568 - 10:50",
        "sender_bank": "ทีเอ็มบีธนชาต (ttb)",
        "sender_name": "นาย ณัฐชัย รักษาวงษ์",
        "receiver_bank": "ทีเอ็มบีธนชาต (ttb)",
        "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
        "ref_id": "202507261001111031",
        "memo": "นุ้ย V คืน 27"
    }
}

# Also insert the top slip of page 2338 (1,500 บาท, จิณห์นิภา)
extra_slip_2338_top = {
    "page": 2338,
    "pages": [2338],
    "dedup_key": "202507081903566513",
    "amount": "1,500.00",
    "datetime": "08 ก.ค. 2568 - 19:44",
    "date_time": "08 ก.ค. 2568 - 19:44",
    "ref_id": "202507081903566513",
    "sender_bank": "ทีเอ็มบีธนชาต (ttb)",
    "sender_name": "นาย ณัฐชัย รักษาวงษ์",
    "receiver_bank": "ทีเอ็มบีธนชาต (ttb)",
    "receiver_name": "น.ส. จิณห์นิภา ประสาทเขตการ",
    "memo": "-",
    "raw_text": "ttb โอนเงินสำเร็จ 8 ก.ค. 68 19:44 น. 1,500.00 บาท",
    "index": 0
}

new_slips = []
inserted_top = False

for item in slips:
    p = item.get("page")
    if p == 2338 and not inserted_top:
        # insert top slip right before bottom slip
        top_item = copy.deepcopy(extra_slip_2338_top)
        new_slips.append(top_item)
        inserted_top = True

    if p in UPDATES:
        for k, v in UPDATES[p].items():
            item[k] = v
        print(f"Updated Page {p}: Amount={item.get('amount')}, Recv={item.get('receiver_name')}")
    
    new_slips.append(item)

# Re-index items 1..N
for i, s in enumerate(new_slips, 1):
    s["index"] = i

print(f"Total slips after update: {len(new_slips)}")

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(new_slips, f, ensure_ascii=False, indent=2)

# Also update Excel file
rows = []
for s in new_slips:
    rows.append({
        "ลำดับ": s.get("index"),
        "หน้า": s.get("page"),
        "วันที่-เวลา": s.get("datetime", s.get("date_time", "-")),
        "ยอดเงิน (บาท)": s.get("amount", "-"),
        "ธนาคารผู้โอน": s.get("sender_bank", "-"),
        "ชื่อผู้โอน": s.get("sender_name", "-"),
        "ธนาคารผู้รับ": s.get("receiver_bank", "-"),
        "ชื่อผู้รับโอน": s.get("receiver_name", "-"),
        "รหัสอ้างอิง": s.get("ref_id", "-"),
        "บันทึกช่วยจำ": s.get("memo", "-")
    })

df = pd.DataFrame(rows)
df.to_excel(XLSX_PATH, index=False)
print("Updated Excel at:", XLSX_PATH)
