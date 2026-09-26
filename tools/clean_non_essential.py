# -*- coding: utf-8 -*-
import os
import sys
import shutil
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(r"d:\Project\DIGITAL_EVIDENCE")
TARGET_ARCHIVE = BASE_DIR / "_archive" / "legacy_prototypes"
TARGET_ARCHIVE.mkdir(parents=True, exist_ok=True)

ITEMS_TO_MOVE = [
    "Docs",
    "tests",
    "sandbox",
    "scratch",
    "tessdata",
    "tesseract.exe",
    "AGENTS-UNIVERSAL V.2.md",
    "BRAIN.md",
    "DESIGN_SYSTEM.md",
    "Glassmorphism Visual Contract.md",
    "UI Specification.md",
    "SAMPLE_Evidence_Target_POI.png",
    ".env.example",
]

print("Moving non-essential secondary files to _archive/legacy_prototypes/...")

for item_name in ITEMS_TO_MOVE:
    src = BASE_DIR / item_name
    if src.exists():
        dest = TARGET_ARCHIVE / item_name
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(str(dest), ignore_errors=True)
            shutil.move(str(src), str(dest))
            print(f"✓ Moved folder: {item_name}")
        else:
            if dest.exists():
                dest.unlink(missing_ok=True)
            shutil.move(str(src), str(dest))
            print(f"✓ Moved file: {item_name}")

print("Done! Only pure operational production files and Folder_Out remain.")
