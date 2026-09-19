#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools/build_sfx_evidence_package.py — WinRAR SFX Archive Automation Builder
Standard: DIGITAL EVIDENCE Court-Grade Protected Archive Protocol
Mission: Creates an encrypted self-extracting (.exe) archive strictly adhering to:
  1. Initial Input Window (Name + Single-entry auto-sync password)
  2. General Tab (RAR format, SFX enabled, Encrypted headers -hp)
  3. Advanced Tab (Title: DIGITAL EVIDENCE, Exact Pattle.pdf 3-line legal disclaimer,
     Navy-blue shield emblem logo scaled to 150x250 BMP, Official app_icon.ico)
  4. Strict Prohibitions Enforcement (Zero unencrypted archives, Zero disclaimer abbreviations)
"""

import os
import sys
import subprocess
import hashlib
from PIL import Image

try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOLDER_OUT = os.path.join(PROJECT_ROOT, "Folder_Out")
SCRATCH_DIR = os.path.join(PROJECT_ROOT, "scratch")
WINRAR_EXE = r"C:\Program Files\WinRAR\WinRAR.exe"

# Official Brand Assets
LOGO_PNG = os.path.join(PROJECT_ROOT, "_skills", "Dicut_Chat", "assets", "logo.png")
ICON_ICO = os.path.join(PROJECT_ROOT, "Portable", "core", "assets", "app_icon.ico")

# Exact legal disclaimer from Pattle.pdf / SKILL.md (Strict Prohibition: Do NOT shorten or alter)
LEGAL_DISCLAIMER = (
    '"DIGITAL EVIDENCE เป็นเพียงการเครื่องมืออำนวยความสะดวกให้กับผู้ว่าจ้าง โดยไม่ได้ดัดแปลง แก้ไข เพิ่ม-ลบ เนื้อหา\n'
    'จากต้นฉบับใดๆ และไม่มีส่วนเกี่ยวข้องใดๆกับเนื้อหาในเอกสาร เป็นเพียงเครื่องมือที่ทำงานเกี่ยวกับระบบไฟล์\n'
    'เอกสารแบบอิเล็กทรอนิกส์ เท่านั้น"'
)

SFX_TITLE = "DIGITAL EVIDENCE"


def prepare_sfx_logo(target_w=150, target_h=250):
    """
    Scales the official navy-blue shield logo symmetrically preserving aspect ratio
    and centers it on a crisp 150x250 RGB canvas saved as Windows BMP.
    """
    os.makedirs(SCRATCH_DIR, exist_ok=True)
    out_bmp = os.path.join(SCRATCH_DIR, "sfx_brand_logo.bmp")
    
    if not os.path.exists(LOGO_PNG):
        raise FileNotFoundError(f"Official logo not found at: {LOGO_PNG}")
        
    img = Image.open(LOGO_PNG)
    scale = min(target_w / img.width, target_h / img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    
    if resized.mode in ("RGBA", "LA") or (resized.mode == "P" and "transparency" in resized.info):
        canvas.paste(resized, (offset_x, offset_y), resized.convert("RGBA"))
    else:
        canvas.paste(resized, (offset_x, offset_y))
        
    canvas.save(out_bmp, "BMP")
    return out_bmp


def generate_sfx_script(extract_folder_name):
    """
    Creates WinRAR SFX Script file encoded in UTF-8.
    """
    os.makedirs(SCRATCH_DIR, exist_ok=True)
    script_path = os.path.join(SCRATCH_DIR, "sfx_script.txt")
    
    content = (
        ";The comment below contains SFX script commands\n"
        f"Title={SFX_TITLE}\n"
        "Text\n"
        "{\n"
        f"{LEGAL_DISCLAIMER}\n"
        "}\n"
        f"Path={extract_folder_name}\n"
        "SavePath\n"
        "Silent=0\n"
        "Overwrite=0\n"
    )
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return script_path


def get_default_evidence_files():
    """
    Selects master deliverables from Folder_Out to bundle into the SFX container.
    """
    candidate_files = [
        "Evidence_Chat_Master_Combined_Vol1_to_3_With_Cover.pdf",
        "Evidence_Chat_Master_Combined_Vol1_to_3.pdf",
        "Evidence_Chat_Master_Front_Cover_and_Index.pdf",
        "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.xlsx",
        "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json",
        "EVIDENCE_HASH_CERTIFICATE.pdf",
        "EVIDENCE_HASH_MANIFEST.json",
        "EVIDENCE_HASH_MANIFEST.sha256"
    ]
    
    selected = []
    for fn in candidate_files:
        fp = os.path.join(FOLDER_OUT, fn)
        if os.path.exists(fp):
            selected.append(fp)
            
    if not selected:
        # Fallback: all files in Folder_Out if specific candidates not present
        for fn in os.listdir(FOLDER_OUT):
            fp = os.path.join(FOLDER_OUT, fn)
            if os.path.isfile(fp):
                selected.append(fp)
                
    return selected


def build_sfx_archive(archive_name, password, files_to_include=None, progress_callback=None):
    """
    Builds the encrypted WinRAR SFX Archive (.exe) strictly enforcing:
      - RAR format
      - Encrypted data and file names (-hp)
      - SFX executable wrapper (-sfx)
      - Custom SFX Title & 3-line legal disclaimer
      - Symmetrical Brand Shield Logo (.bmp)
      - Official App Icon (.ico)
    """
    if not password or not str(password).strip():
        raise ValueError("ข้อห้ามเด็ดขาด: ห้ามสร้างไฟล์ SFX โดยไม่มีรหัสผ่านป้องกัน (No Unencrypted SFX Archive)")
        
    if not os.path.exists(WINRAR_EXE):
        raise FileNotFoundError(f"ไม่พบโปรแกรม WinRAR ที่: {WINRAR_EXE}")
        
    if not archive_name.lower().endswith(".exe"):
        archive_name += ".exe"
        
    out_exe_path = os.path.join(FOLDER_OUT, archive_name)
    extract_folder = os.path.splitext(archive_name)[0]
    
    if files_to_include is None or len(files_to_include) == 0:
        files_to_include = get_default_evidence_files()
        
    if not files_to_include:
        raise ValueError("ไม่พบไฟล์พยานหลักฐานใน Folder_Out ที่จะนำมาบีบอัด")
        
    if progress_callback:
        progress_callback("กำลังเตรียมตราสัญลักษณ์และข้อกำหนดทางกฎหมาย...")
        
    logo_bmp = prepare_sfx_logo(150, 250)
    script_txt = generate_sfx_script(extract_folder)
    
    if progress_callback:
        progress_callback("กำลังประมวลผลการบีบอัดและเข้ารหัสระดับ AES-256 ด้วย WinRAR SFX...")
        
    # Build WinRAR command line
    cmd = [
        WINRAR_EXE,
        "a",                     # Add to archive
        "-sfx",                  # Create SFX archive (.exe)
        f"-hp{password}",        # Encrypt file data and file headers
        "-m3",                   # Standard balanced compression
        "-scuc",                 # Unicode UTF-8 comment switch
        f"-z{script_txt}",       # Read SFX script comment from file
        f"-iicon{ICON_ICO}",     # Set SFX icon
        f"-ilogo{logo_bmp}",     # Set SFX logo bitmap
        "-ep1",                  # Exclude base directory from names
        out_exe_path
    ] + files_to_include

    # If old output exists, remove to avoid appending
    if os.path.exists(out_exe_path):
        try:
            os.remove(out_exe_path)
        except Exception:
            pass

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"WinRAR ทำงานล้มเหลว (Code {proc.returncode}):\n{proc.stderr or proc.stdout}")
        
    if not os.path.exists(out_exe_path):
        raise FileNotFoundError("ไม่พบไฟล์ SFX ที่สร้างขึ้นหลังคำสั่งทำงานเสร็จสิ้น")
        
    # Calculate SHA-256
    hasher = hashlib.sha256()
    with open(out_exe_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    sha256_hex = hasher.hexdigest()
    
    file_size_mb = os.path.getsize(out_exe_path) / (1024 * 1024)
    
    # Save accompanying checksum file
    sha_file = out_exe_path + ".sha256"
    with open(sha_file, "w", encoding="utf-8") as f:
        f.write(f"{sha256_hex} *{os.path.basename(out_exe_path)}\n")
        
    return {
        "output_path": out_exe_path,
        "file_name": os.path.basename(out_exe_path),
        "size_mb": file_size_mb,
        "sha256": sha256_hex,
        "sha_file": sha_file,
        "files_count": len(files_to_include)
    }


# ==============================================================================
# GUI MODE: Initial Input Window & Program Interface Simulator
# ==============================================================================
def launch_gui():
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    root = tk.Tk()
    root.title("DIGITAL EVIDENCE — WinRAR SFX Builder")
    root.geometry("780x680")
    root.minsize(740, 640)
    root.configure(bg="#0F172A")  # Deep Navy
    
    # Setup styles
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except Exception:
        pass
        
    style.configure("TNotebook", background="#0F172A", borderwidth=0)
    style.configure("TNotebook.Tab", background="#1E293B", foreground="#94A3B8", font=("Segoe UI", 10, "bold"), padding=[16, 6])
    style.map("TNotebook.Tab",
              background=[("selected", "#2563EB")],
              foreground=[("selected", "#FFFFFF")])
    
    # --- HEADER ---
    header_frame = tk.Frame(root, bg="#1E293B", pady=12, padx=16)
    header_frame.pack(fill="x")
    
    title_lbl = tk.Label(
        header_frame,
        text="🏛️ DIGITAL EVIDENCE — SFX ARCHIVE PROTOCOL",
        font=("Segoe UI", 14, "bold"),
        fg="#38BDF8",
        bg="#1E293B"
    )
    title_lbl.pack(anchor="w")
    
    subtitle_lbl = tk.Label(
        header_frame,
        text="ระบบจัดทำแฟ้มพยานหลักฐานดิจิทัลคลายตัวเองอัตโนมัติ (WinRAR SFX Encrypted Container)",
        font=("Sarabun", 10),
        fg="#94A3B8",
        bg="#1E293B"
    )
    subtitle_lbl.pack(anchor="w")
    
    # --- MAIN CONTAINER ---
    content_frame = tk.Frame(root, bg="#0F172A", padx=16, pady=12)
    content_frame.pack(fill="both", expand=True)
    
    # --- PART 1: INITIAL INPUT WINDOW (กรอกข้อมูลเริ่มต้น) ---
    p1_frame = tk.LabelFrame(
        content_frame,
        text=" 📥 ส่วนที่ 1: การกรอกข้อมูลความปลอดภัยหลัก (Initial Input Window) ",
        font=("Segoe UI", 10, "bold"),
        fg="#38BDF8",
        bg="#1E293B",
        padx=14,
        pady=10
    )
    p1_frame.pack(fill="x", pady=(0, 10))
    
    # Row 1: Name Input
    tk.Label(
        p1_frame,
        text="1. ชื่อไฟล์คดี / แฟ้มเอกสาร (Name Input):",
        font=("Segoe UI", 9, "bold"),
        fg="#F1F5F9",
        bg="#1E293B"
    ).grid(row=0, column=0, sticky="w", pady=4)
    
    name_var = tk.StringVar(value="Pattle_Case_Evidence")
    name_entry = tk.Entry(
        p1_frame,
        textvariable=name_var,
        font=("Segoe UI", 10),
        bg="#0F172A",
        fg="#38BDF8",
        insertbackground="#FFFFFF",
        relief="solid",
        bd=1,
        width=45
    )
    name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=4)
    
    # Row 2: Password Input (One-entry with auto-sync)
    tk.Label(
        p1_frame,
        text="2. รหัสผ่านความปลอดภัย (Password Input):",
        font=("Segoe UI", 9, "bold"),
        fg="#F1F5F9",
        bg="#1E293B"
    ).grid(row=1, column=0, sticky="w", pady=4)
    
    pwd_frame = tk.Frame(p1_frame, bg="#1E293B")
    pwd_frame.grid(row=1, column=1, sticky="w", padx=10, pady=4)
    
    pwd_var = tk.StringVar(value="")
    pwd_entry = tk.Entry(
        pwd_frame,
        textvariable=pwd_var,
        show="*",
        font=("Segoe UI", 10),
        bg="#0F172A",
        fg="#4ADE80",
        insertbackground="#FFFFFF",
        relief="solid",
        bd=1,
        width=36
    )
    pwd_entry.pack(side="left")
    
    def toggle_pwd():
        if pwd_entry.cget('show') == '':
            pwd_entry.config(show='*')
            eye_btn.config(text="👁️")
        else:
            pwd_entry.config(show='')
            eye_btn.config(text="🙈")
            
    eye_btn = tk.Button(
        pwd_frame,
        text="👁️",
        command=toggle_pwd,
        font=("Segoe UI", 8),
        bg="#334155",
        fg="#FFFFFF",
        relief="flat",
        padx=6
    )
    eye_btn.pack(side="left", padx=6)
    
    sync_lbl = tk.Label(
        p1_frame,
        text="⚡ ระบบหลังบ้านทำการ Auto-Sync ไปยังช่องยืนยันรหัสผ่าน (Confirm Password) ให้โดยอัตโนมัติ",
        font=("Segoe UI", 8),
        fg="#34D399",
        bg="#1E293B"
    )
    sync_lbl.grid(row=2, column=0, columnspan=2, sticky="w", pady=(2, 0))
    
    # --- PART 2: PROGRAM INTERFACE SIMULATOR TABS ---
    nb_frame = tk.Frame(content_frame, bg="#0F172A")
    nb_frame.pack(fill="both", expand=True, pady=(0, 10))
    
    notebook = ttk.Notebook(nb_frame)
    notebook.pack(fill="both", expand=True)
    
    # Tab 1: ทั่วไป (General Tab)
    tab_gen = tk.Frame(notebook, bg="#1E293B", padx=14, pady=12)
    notebook.add(tab_gen, text=" 📁 แถบ ทั่วไป (General) ")
    
    # Tab 1 content
    def update_gen_archive_name(*args):
        base = name_var.get().strip() or "Pattle_Case_Evidence"
        gen_name_lbl.config(text=f"{base}.exe")
        
    name_var.trace_add("write", update_gen_archive_name)
    
    tk.Label(tab_gen, text="ชื่อเอกสาร (Archive Name):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").grid(row=0, column=0, sticky="w", pady=6)
    gen_name_lbl = tk.Label(tab_gen, text="Pattle_Case_Evidence.exe", font=("Segoe UI", 9, "bold"), fg="#38BDF8", bg="#0F172A", padx=8, pady=3, relief="solid", bd=1)
    gen_name_lbl.grid(row=0, column=1, sticky="w", padx=10, pady=6)
    
    tk.Label(tab_gen, text="รูปแบบเอกสาร (Archive Format):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").grid(row=1, column=0, sticky="w", pady=6)
    tk.Label(tab_gen, text="● RAR (ล็อกค่าตามมาตรฐานเพื่อความปลอดภัยสูงสุด)", font=("Segoe UI", 9, "bold"), fg="#A855F7", bg="#1E293B").grid(row=1, column=1, sticky="w", padx=10, pady=6)
    
    tk.Label(tab_gen, text="สร้างเอกสาร SFX (Create SFX):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").grid(row=2, column=0, sticky="w", pady=6)
    tk.Label(tab_gen, text="☑ ติ๊กถูกเลือกใช้งานเสมอ (คลายไฟล์ได้โดยไม่ต้องติดตั้ง WinRAR)", font=("Segoe UI", 9, "bold"), fg="#22C55E", bg="#1E293B").grid(row=2, column=1, sticky="w", padx=10, pady=6)
    
    tk.Label(tab_gen, text="สถานะรหัสผ่าน (Set Password):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").grid(row=3, column=0, sticky="w", pady=6)
    def update_gen_pwd(*args):
        p = pwd_var.get()
        if p:
            gen_pwd_lbl.config(text="🔒 " + ("●" * min(len(p), 16)) + " (เข้ารหัสข้อมูลและชื่อไฟล์ AES-256)", fg="#4ADE80")
        else:
            gen_pwd_lbl.config(text="⚠️ ยังไม่ได้ระบุรหัสผ่าน (ห้ามปล่อยว่างเด็ดขาด)", fg="#EF4444")
            
    gen_pwd_lbl = tk.Label(tab_gen, text="⚠️ ยังไม่ได้ระบุรหัสผ่าน (ห้ามปล่อยว่างเด็ดขาด)", font=("Segoe UI", 9, "bold"), fg="#EF4444", bg="#1E293B")
    gen_pwd_lbl.grid(row=3, column=1, sticky="w", padx=10, pady=6)
    pwd_var.trace_add("write", update_gen_pwd)
    
    # Tab 2: ขั้นสูง (Advanced Tab / SFX Options)
    tab_adv = tk.Frame(notebook, bg="#1E293B", padx=14, pady=10)
    notebook.add(tab_adv, text=" ⚙️ แถบ ขั้นสูง (SFX Options) ")
    
    tk.Label(tab_adv, text="2.1 หัวข้อของวินโดวส์ (Title of SFX window):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").pack(anchor="w")
    tk.Label(tab_adv, text=SFX_TITLE, font=("Segoe UI", 10, "bold"), fg="#38BDF8", bg="#0F172A", padx=8, pady=2, relief="solid", bd=1).pack(anchor="w", pady=(2, 6))
    
    tk.Label(tab_adv, text="2.2 ตัวอักษรที่จะแสดงในวินโดวส์ SFX (Text / Legal Disclaimer จาก Pattle.pdf):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").pack(anchor="w")
    txt_box = tk.Text(tab_adv, height=4, font=("Sarabun", 9), bg="#0F172A", fg="#CBD5E1", relief="solid", bd=1, padx=8, pady=6)
    txt_box.insert("1.0", LEGAL_DISCLAIMER.replace('"', ''))
    txt_box.config(state="disabled")
    txt_box.pack(fill="x", pady=(2, 6))
    
    tk.Label(tab_adv, text="2.3 โลโก้และไอคอน (Logo & Icon):", font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B").pack(anchor="w")
    icons_lbl = tk.Label(
        tab_adv,
        text="🛡️ โลโก้ SFX: ตราโล่สีกรมท่า-ฟ้า (150x250 BMP รักษาอัตราส่วน)  |  🏷️ ไอคอน SFX: app_icon.ico ทางการ",
        font=("Segoe UI", 8, "bold"),
        fg="#60A5FA",
        bg="#1E293B"
    )
    icons_lbl.pack(anchor="w", pady=(2, 0))
    
    # --- FOOTER / EXECUTE BUTTON ---
    footer_frame = tk.Frame(content_frame, bg="#0F172A")
    footer_frame.pack(fill="x")
    
    status_var = tk.StringVar(value="พร้อมดำเนินการสร้างแฟ้มหลักฐาน SFX")
    status_lbl = tk.Label(
        footer_frame,
        textvariable=status_var,
        font=("Segoe UI", 9),
        fg="#94A3B8",
        bg="#0F172A"
    )
    status_lbl.pack(anchor="w", pady=(0, 6))
    
    def on_build_clicked():
        name = name_var.get().strip()
        pwd = pwd_var.get().strip()
        
        if not name:
            messagebox.showerror("ข้อมูลไม่ครบถ้วน", "กรุณาระบุชื่อไฟล์คดี / แฟ้มเอกสาร")
            name_entry.focus()
            return
            
        if not pwd:
            messagebox.showerror(
                "ข้อห้ามเด็ดขาด (Strict Prohibition)",
                "ห้ามสร้างไฟล์ SFX โดยไม่มีรหัสผ่านเด็ดขาด!\n\nเนื่องจากพยานหลักฐานดิจิทัลถือเป็นข้อมูลอ่อนไหวตามกฎหมาย กรุณาระบุรหัสผ่านป้องกัน"
            )
            pwd_entry.focus()
            return
            
        build_btn.config(state="disabled", text="⏳ กำลังสร้างแฟ้ม SFX...")
        root.update()
        
        try:
            res = build_sfx_archive(
                archive_name=name,
                password=pwd,
                progress_callback=lambda msg: status_var.set(msg) or root.update()
            )
            status_var.set(f"✅ สำเร็จ! สร้าง {res['file_name']} ขนาด {res['size_mb']:.2f} MB เรียบร้อยแล้ว")
            
            info_msg = (
                f"🎉 บันทึกแฟ้มพยานหลักฐาน SFX สำเร็จเรียบร้อยแล้ว!\n\n"
                f"📁 ชื่อไฟล์: {res['file_name']}\n"
                f"📦 ขนาด: {res['size_mb']:.2f} MB\n"
                f"🔒 รหัสผ่าน: {pwd}\n"
                f"🔐 SHA-256:\n{res['sha256']}\n\n"
                f"ที่ตั้งไฟล์:\n{res['output_path']}"
            )
            messagebox.showinfo("บันทึกสำเร็จ (Success)", info_msg)
            
        except Exception as e:
            status_var.set("❌ เกิดข้อผิดพลาดในการสร้างไฟล์")
            messagebox.showerror("เกิดข้อผิดพลาด", str(e))
        finally:
            build_btn.config(state="normal", text="🚀 สร้างแฟ้มพยานหลักฐาน WinRAR SFX (Locked Archive) ทันที")
            
    build_btn = tk.Button(
        footer_frame,
        text="🚀 สร้างแฟ้มพยานหลักฐาน WinRAR SFX (Locked Archive) ทันที",
        command=on_build_clicked,
        font=("Segoe UI", 11, "bold"),
        bg="#2563EB",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        pady=10
    )
    build_btn.pack(fill="x")
    
    root.mainloop()


# ==============================================================================
# CLI / STANDALONE ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DIGITAL EVIDENCE WinRAR SFX Builder")
    parser.add_argument("--name", default=None, help="Archive name (e.g. Pattle_Case_Evidence)")
    parser.add_argument("--password", default=None, help="Encryption password")
    parser.add_argument("--cli", action="store_true", help="Run headlessly in CLI mode")
    args = parser.parse_args()
    
    if args.cli or (args.name and args.password):
        name = args.name or "Pattle_Case_Evidence"
        pwd = args.password
        if not pwd:
            print("❌ ข้อผิดพลาด: ต้องระบุ --password เมื่อรันใน CLI mode")
            sys.exit(1)
        print(f"📦 กำลังสร้างแฟ้ม SFX: {name}.exe ...")
        result = build_sfx_archive(name, pwd, progress_callback=print)
        print(f"✅ สร้างแฟ้ม SFX สำเร็จ: {result['output_path']}")
        print(f"📊 ขนาด: {result['size_mb']:.2f} MB")
        print(f"🔐 SHA-256: {result['sha256']}")
    else:
        launch_gui()
