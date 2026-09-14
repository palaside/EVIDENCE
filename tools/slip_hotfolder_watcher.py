"""
EVIDENCE Hot Folder Background Watcher
--------------------------------------
Monitors EVIDENCE_IN for slip images/folders 24/7.
Automatically runs OCR_Slip extraction, generates legal A4 Landscape Excel into Folder_Out,
and moves processed files to EVIDENCE_IN/processed/.
"""

import sys
import os
import time
import shutil
import datetime
from pathlib import Path

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_IN = os.path.join(BASE_DIR, "EVIDENCE_IN")
FOLDER_OUT = os.path.join(BASE_DIR, "Folder_Out")
LOG_FILE = os.path.join(BASE_DIR, "tools", "watcher.log")
PROCESSED_DIR = os.path.join(EVIDENCE_IN, "processed")

# Also check Desktop inboxes
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "EVIDENCE_IN")
ONEDRIVE_DESKTOP = os.path.join(os.path.expanduser("~"), "OneDrive", "เดสก์ท็อป", "EVIDENCE_IN")

OCR_SCRIPT = os.path.join(BASE_DIR, "_skills", "OCR_Slip", "scripts", "ocr_slip.py")

os.makedirs(EVIDENCE_IN, exist_ok=True)
os.makedirs(FOLDER_OUT, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}

# Force UTF-8 on Windows
if sys.platform == "win32":
    if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if sys.stderr is not None and hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def log(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    if sys.stdout is not None:
        try:
            print(line, flush=True)
        except Exception:
            try:
                print(line.encode("ascii", "replace").decode("ascii"), flush=True)
            except Exception:
                pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
    except Exception:
        pass

def is_file_settled(file_path, wait_seconds=1.0):
    """Ensure file copy is finished before reading."""
    try:
        size1 = os.path.getsize(file_path)
        time.sleep(wait_seconds)
        size2 = os.path.getsize(file_path)
        return size1 == size2 and size1 > 0
    except Exception:
        return False

def get_watch_folders():
    folders = [EVIDENCE_IN]
    try:
        if os.path.exists(DESKTOP_DIR):
            folders.append(DESKTOP_DIR)
    except Exception:
        pass
    try:
        if os.path.exists(ONEDRIVE_DESKTOP):
            folders.append(ONEDRIVE_DESKTOP)
    except Exception:
        pass
    return folders

def process_slip_batch(watch_dir):
    try:
        items = os.listdir(watch_dir)
    except Exception as e:
        return

    # Filter out 'processed' and temporary files
    images = []
    subfolders = []
    
    for item in items:
        if item.lower() in ("processed", "desktop.ini", "thumbs.db") or item.startswith("."):
            continue
        full_path = os.path.join(watch_dir, item)
        if os.path.isfile(full_path):
            ext = os.path.splitext(item)[1].lower()
            if ext in IMAGE_EXTENSIONS:
                images.append(full_path)
        elif os.path.isdir(full_path):
            subfolders.append(full_path)

    # 1. Process Subfolders (e.g. user drops a whole case folder)
    for sub in subfolders:
        sub_name = os.path.basename(sub)
        sub_images = [os.path.join(sub, f) for f in os.listdir(sub) if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
        if not sub_images:
            continue
        # Check if first image is settled
        if not is_file_settled(sub_images[0], 0.5):
            continue

        log(f"📥 [HotFolder] พบโฟลเดอร์เคสสลิป: {sub_name} ({len(sub_images)} รูป)")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_excel = os.path.join(FOLDER_OUT, f"Slip_Case_{sub_name}_{timestamp}.xlsx")

        import subprocess
        python_exe = sys.executable
        cmd = [python_exe, OCR_SCRIPT, "--input", sub, "--output", out_excel]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if res.returncode == 0:
            log(f"✅ [HotFolder] สกัดสำเร็จ -> {out_excel}")
            # Move processed subfolder
            dst = os.path.join(PROCESSED_DIR, f"{sub_name}_{timestamp}")
            try:
                shutil.move(sub, dst)
            except Exception as e:
                log(f"⚠️ ย้ายโฟลเดอร์ไป processed ไม่สำเร็จ: {e}")
        else:
            log(f"❌ [HotFolder] OCR ล้มเหลว: {res.stderr}")

    # 2. Process Loose Images in Watch Folder
    if images:
        # Check if latest image is settled
        if not is_file_settled(images[-1], 0.8):
            return

        log(f"📥 [HotFolder] พบสลิปรูปภาพใหม่ {len(images)} รูป ใน {os.path.basename(watch_dir)}")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_tmp = os.path.join(watch_dir, f"_batch_{timestamp}")
        os.makedirs(batch_tmp, exist_ok=True)

        for img in images:
            try:
                shutil.move(img, os.path.join(batch_tmp, os.path.basename(img)))
            except Exception:
                pass

        out_excel = os.path.join(FOLDER_OUT, f"Slip_Evidence_{timestamp}.xlsx")
        import subprocess
        python_exe = sys.executable
        cmd = [python_exe, OCR_SCRIPT, "--input", batch_tmp, "--output", out_excel]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if res.returncode == 0:
            log(f"✅ [HotFolder] สร้างตารางสลิปสำเร็จ -> {out_excel}")
            # Move batch folder to processed
            dst = os.path.join(PROCESSED_DIR, f"Batch_{timestamp}")
            try:
                shutil.move(batch_tmp, dst)
            except Exception as e:
                pass
        else:
            log(f"❌ [HotFolder] เกิดข้อผิดพลาด: {res.stderr}")

def main_loop():
    log("============================================================")
    log("🚀 DIGITAL EVIDENCE Slip Watcher Service Started (Background)")
    log(f"📁 Monitoring Inbox: {EVIDENCE_IN}")
    log(f"📊 Output Folder:    {FOLDER_OUT}")
    log("============================================================")

    iteration = 0
    while True:
        iteration += 1
        try:
            for w in get_watch_folders():
                if os.path.exists(w):
                    process_slip_batch(w)
        except BaseException as e:
            log(f"Loop error ({type(e).__name__}): {e}")
        
        # Heartbeat every 20 loops (~60s)
        if iteration % 20 == 0:
            log(f"💓 Heartbeat: Watcher is alive and healthy (Loop {iteration})")

        time.sleep(3)

if __name__ == "__main__":
    import traceback
    try:
        main_loop()
    except BaseException as e:
        crash_log = os.path.join(BASE_DIR, "tools", "watcher_crash.log")
        with open(crash_log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now()}] CRASH ({type(e).__name__}): {traceback.format_exc()}\n")
