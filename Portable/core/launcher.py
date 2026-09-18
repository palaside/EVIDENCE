# -*- coding: utf-8 -*-
import sys
import os
import glob
import datetime
import subprocess

try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

PORTABLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(PORTABLE_DIR, "core")
INBOX_SLIPS = os.path.join(PORTABLE_DIR, "INBOX_SLIPS")
INBOX_CHATS = os.path.join(PORTABLE_DIR, "INBOX_CHATS")
OUTPUT_DIR = os.path.join(PORTABLE_DIR, "OUTPUT")

os.makedirs(INBOX_SLIPS, exist_ok=True)
os.makedirs(INBOX_CHATS, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def count_images(folder):
    exts = ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG")
    count = 0
    for e in exts:
        count += len(glob.glob(os.path.join(folder, e)))
    return count


def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def open_folder(path):
    try:
        os.startfile(path)
    except Exception:
        subprocess.run(["explorer", path])


def open_file_in_explorer(file_path):
    try:
        subprocess.run(["explorer", f"/select,{file_path}"])
    except Exception:
        open_folder(os.path.dirname(file_path))


def run_slip_mode(input_target=None):
    target = input_target or INBOX_SLIPS
    n_imgs = count_images(target) if os.path.isdir(target) else 1
    print("\n" + "=" * 65)
    print("  [*] โหมดสลิป (SLIP EVIDENCE MODE)")
    print(f"  [*] โฟลเดอร์ต้นทาง: {target} (พบ {n_imgs} ภาพ)")
    print("=" * 65)

    if n_imgs == 0:
        print("\n[!] ยังไม่มีรูปภาพในโฟลเดอร์ กรุณานำรูปสลิปไปวางใน:")
        print(f"    {target}")
        input("\nกด Enter เพื่อเปิดโฟลเดอร์นี้...")
        open_folder(target)
        return

    out_file = os.path.join(OUTPUT_DIR, f"Evidence_Slips_{get_timestamp()}.pdf")
    print(f"\n[*] กำลังประมวลผลด้วย PyMuPDF C-Binding...")
    script = os.path.join(CORE_DIR, "process_chat.py")
    res = subprocess.run([sys.executable, script, target, out_file])

    if res.returncode == 0 and os.path.exists(out_file):
        print("\n[OK] เสร็จสิ้นเรียบร้อยแล้ว!")
        print(f"     ไฟล์ผลลัพธ์: {os.path.basename(out_file)}")
        open_file_in_explorer(out_file)
    else:
        print("\n[!] การประมวลผลเกิดข้อผิดพลาด")
    input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")


def run_chat_mode(input_target=None):
    target = input_target or INBOX_CHATS
    n_imgs = count_images(target) if os.path.isdir(target) else 1
    print("\n" + "=" * 65)
    print("  [*] โหมดแชท (CHAT EVIDENCE MODE)")
    print(f"  [*] โฟลเดอร์ต้นทาง: {target} (พบ {n_imgs} ภาพ)")
    print("=" * 65)

    if n_imgs == 0:
        print("\n[!] ยังไม่มีรูปภาพในโฟลเดอร์ กรุณานำรูปแชทไปวางใน:")
        print(f"    {target}")
        input("\nกด Enter เพื่อเปิดโฟลเดอร์นี้...")
        open_folder(target)
        return

    out_file = os.path.join(OUTPUT_DIR, f"Evidence_Chat_{get_timestamp()}.pdf")
    print(f"\n[*] กำลังประมวลผลด้วย Smart Slicing + PyMuPDF C-Binding...")
    script = os.path.join(CORE_DIR, "process_chat.py")
    res = subprocess.run([sys.executable, script, target, out_file, "--chat"])

    if res.returncode == 0 and os.path.exists(out_file):
        print("\n[*] สร้างสารบัญสลิปและใบนำทาง...")
        search_script = os.path.join(CORE_DIR, "search_slip.py")
        subprocess.run([sys.executable, search_script, out_file, OUTPUT_DIR])

        print("\n[OK] เสร็จสิ้นเรียบร้อยแล้ว!")
        print(f"     ไฟล์ผลลัพธ์: {os.path.basename(out_file)}")
        open_file_in_explorer(out_file)
    else:
        print("\n[!] การประมวลผลเกิดข้อผิดพลาด")
    input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")


def run_drag_drop(target_path):
    print("\n" + "=" * 65)
    print("        DIGITAL EVIDENCE - DETECTED DRAG & DROP")
    print("=" * 65)
    print(f" เป้าหมายที่ลากมาวาง: {target_path}")
    print("-" * 65)
    print(" กรุณาเลือกโหมดที่ต้องการ:")
    print("  [1] โหมดสลิป (SLIP MODE) - หน้าละ 1 ใบ กึ่งกลาง A4 + ใบสรุป")
    print("  [2] โหมดแชท  (CHAT MODE) - ต่อเนื่อง Smart Slicing + ใบสรุป")
    print("  [3] สแกนหาและทำสารบัญสลิป (SEARCH & SLIP INDEX)")
    print("  [0] ยกเลิก")
    print("=" * 65)
    choice = input("เลือกโหมด [1-3]: ").strip()
    if choice == "1":
        run_slip_mode(target_path)
    elif choice == "2":
        run_chat_mode(target_path)
    elif choice == "3":
        search_script = os.path.join(CORE_DIR, "search_slip.py")
        subprocess.run([sys.executable, search_script, target_path, OUTPUT_DIR])
        open_folder(OUTPUT_DIR)


def main():
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        run_drag_drop(sys.argv[1])
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        slips_count = count_images(INBOX_SLIPS)
        chats_count = count_images(INBOX_CHATS)

        print("=" * 68)
        print("          DIGITAL EVIDENCE - FORENSIC PROCESSING SUITE")
        print("                   (Portable Standalone Edition)")
        print("=" * 68)
        print("\n [สถานะกล่องรับไฟล์เข้า (INBOX)]")
        print(f"   📥 INBOX_SLIPS : พร้อมประมวลผล {slips_count} ภาพ")
        print(f"   📥 INBOX_CHATS : พร้อมประมวลผล {chats_count} ภาพ")
        print(f"   📤 OUTPUT      : {OUTPUT_DIR}")
        print("\n" + "-" * 68)
        print(" เมนูการทำงาน:")
        print("   [1] ประมวลผลโหมดสลิป (SLIP MODE)  <- ดึงรูปจาก INBOX_SLIPS")
        print("   [2] ประมวลผลโหมดแชท  (CHAT MODE)  <- ดึงรูปจาก INBOX_CHATS")
        print("   [3] ประมวลผลแชทคดีจริงรวม 3 เล่ม (EDOK แชทที่ 1, 2, 3)")
        print("   [4] สแกนหาและทำสารบัญสลิป (Forensic Slip Index จากไฟล์ PDF)")
        print("   [5] สร้างหน้าปกและแทรกสารบัญหน้าแรก (Cover Page & Front Index Merger)")
        print("   [6] คำนวณรหัสรับรองหลักฐานดิจิทัล (Cryptographic Hash Manifest SHA-256)")
        print("   [7] คัดหาหลักฐานเฉพาะบุคคลเป้าหมาย (Target Name Matcher - สกิล Name)")
        print("   [8] เปิดโฟลเดอร์รับไฟล์และผลลัพธ์ (INBOX / OUTPUT FOLDERS)")
        print("   [9] ตรวจสอบสถานะและฟื้นคืนชีพความจำ (Open/Resume Session Checkpoint)")
        print("\n   [0] ออกจากโปรแกรม")
        print("=" * 68)

        choice = input("เลือกคำสั่ง [0-9]: ").strip()

        if choice == "1":
            run_slip_mode()
        elif choice == "2":
            run_chat_mode()
        elif choice == "3":
            master_bat = os.path.join(PORTABLE_DIR, "..", "RUN_CHAT_EVIDENCE_PROCESSOR.bat")
            if os.path.exists(master_bat):
                subprocess.run([master_bat], shell=True)
            else:
                print(f"[!] ไม่พบไฟล์ {master_bat}")
            input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        elif choice == "4":
            pdf_path = input("\nกรุณาระบุที่อยู่ไฟล์ PDF หรือลากไฟล์มาวางที่นี่: ").strip().strip('"')
            if pdf_path and os.path.exists(pdf_path):
                search_script = os.path.join(CORE_DIR, "search_slip.py")
                subprocess.run([sys.executable, search_script, pdf_path, OUTPUT_DIR])
                open_folder(OUTPUT_DIR)
            else:
                print("[!] ไม่พบไฟล์ที่ระบุ")
            input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        elif choice == "5":
            cover_script = os.path.join(CORE_DIR, "generate_cover_page.py")
            if os.path.exists(cover_script):
                subprocess.run([sys.executable, cover_script])
                open_folder(OUTPUT_DIR)
            else:
                print(f"[!] ไม่พบสคริปต์ {cover_script}")
            input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        elif choice == "6":
            hash_script = os.path.join(CORE_DIR, "evidence_hash_manifest.py")
            if os.path.exists(hash_script):
                print(f"\n[*] กำลังคำนวณค่า SHA-256 สำหรับไฟล์ทั้งหมดใน {OUTPUT_DIR}...")
                subprocess.run([sys.executable, hash_script, OUTPUT_DIR])
                open_folder(OUTPUT_DIR)
            else:
                print(f"[!] ไม่พบสคริปต์ {hash_script}")
            input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        elif choice == "7":
            name_script = os.path.join(CORE_DIR, "name_filter.py")
            if os.path.exists(name_script):
                target_q = input("\nระบุชื่อ-นามสกุล บุคคลเป้าหมาย (เช่น 'จิณห์นิภา ประสาทเขตการ'): ").strip()
                if target_q:
                    cache_file = os.path.join(PORTABLE_DIR, "..", "Folder_Out", "slips_ocr_cache.json")
                    cmd = [sys.executable, name_script, "--name", target_q, "--out", OUTPUT_DIR]
                    if os.path.exists(cache_file):
                        cmd.extend(["--cache", cache_file])
                    subprocess.run(cmd)
                    open_folder(OUTPUT_DIR)
            else:
                print(f"[!] ไม่พบสคริปต์ {name_script}")
            input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        elif choice == "8":
            open_folder(INBOX_SLIPS)
            open_folder(INBOX_CHATS)
            open_folder(OUTPUT_DIR)
        elif choice == "9":
            open_script = os.path.join(CORE_DIR, "open_project_state.py")
            if os.path.exists(open_script):
                subprocess.run([sys.executable, open_script])
            else:
                print(f"[!] ไม่พบสคริปต์ {open_script}")
            input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
