"""
DIGITAL EVIDENCE - LINE Chat Chronological Timeline Validator
============================================================
Detects LINE date pill banners (e.g., 'อา. 19 มกราคม 2568') across chat images
to verify strictly monotonic chronological progression across Volume 1, 2, and 3.
"""

import os
import sys
import re
import glob
import cv2
import pytesseract

if sys.platform == "win32":
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

THAI_MONTHS = {
    "มกราคม": 1, "กุมภาพันธ์": 2, "มีนาคม": 3, "เมษายน": 4,
    "พฤษภาคม": 5, "มิถุนายน": 6, "กรกฎาคม": 7, "สิงหาคม": 8,
    "กันยายน": 9, "ตุลาคม": 10, "พฤศจิกายน": 11, "ธันวาคม": 12
}

DATE_PILL_REGEX = re.compile(
    r"(?:อา\.|จ\.|อ\.|พ\.|พฤ\.|ศ\.|ส\.)?\s*(\d{1,2})\s+"
    r"(มกราคม|กุมภาพันธ์|มีนาคม|เมษายน|พฤษภาคม|มิถุนายน|กรกฎาคม|สิงหาคม|กันยายน|ตุลาคม|พฤศจิกายน|ธันวาคม)\s+"
    r"(256\d)",
    re.IGNORECASE
)

def parse_thai_date(text):
    m = DATE_PILL_REGEX.search(text)
    if m:
        day = int(m.group(1))
        month = THAI_MONTHS.get(m.group(2), 0)
        year = int(m.group(3))
        return (year, month, day, f"{day} {m.group(2)} {year}")
    return None

if __name__ == "__main__":
    test_str = "อา. 19 มกราคม 2568"
    parsed = parse_thai_date(test_str)
    print(f"Test parse: '{test_str}' -> {parsed}")
