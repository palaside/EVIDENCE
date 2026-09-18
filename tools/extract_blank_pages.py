import fitz
import sys

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

pdf_path = r"d:\Project\DIGITAL_EVIDENCE\Folder_Out\Evidence_Chat_Master_Combined_Vol1_to_3.pdf"
doc = fitz.open(pdf_path)

pages_to_check = [75, 408, 933, 1071, 1074, 1309, 1379, 2048, 2273]

for pno in pages_to_check:
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=150)
    out_img = f"Folder_Out/check_p{pno}.png"
    pix.save(out_img)
    print(f"Saved {out_img}")
