import json
import sys

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

with open("Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    amt = item.get("amount", "").strip()
    if not amt or amt == "-" or amt == "0.00":
        print(f"idx={item['index']} pg={item['page_no']} amt='{amt}' dt='{item.get('date_time')}' ref='{item.get('ref_id')}' s_b='{item.get('sender_bank')}' r_b='{item.get('receiver_bank')}'")
