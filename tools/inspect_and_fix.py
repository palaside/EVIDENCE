import json
import sys
import fitz

def main():
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    with open('Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Total items in index: {len(data)}")
    for i, item in enumerate(data):
        if i >= 80:
            print(f"Item {i+1}: page_no={item.get('page_no')}, amount={item.get('amount')}, sender={item.get('sender_name')}, receiver={item.get('receiver_name')}")

    pdf_path = 'Folder_Out/Evidence_Chat_Master_Combined_Vol1_to_3.pdf'
    doc = fitz.open(pdf_path)
    print(f"Master PDF total pages: {len(doc)}")
    doc.close()

if __name__ == '__main__':
    main()
