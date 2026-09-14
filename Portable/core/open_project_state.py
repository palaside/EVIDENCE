#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools/open_project_state.py — Immortal Agent Protocol: Project State Hydration Engine
Role: Reads saved checkpoints, memory rules, mistakes, and project status
to immediately wake up the AI agent in its exact previous mental state.
"""

import os
import sys
import json
import glob
from datetime import datetime

try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE_DIR = os.path.join(PROJECT_ROOT, "state")
MEMORY_DIR = os.path.join(PROJECT_ROOT, "memory")
CHECKPOINT_FILE = os.path.join(PROJECT_ROOT, "LATEST_CHECKPOINT.md")


def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def load_text(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return ""


def get_latest_checkpoint():
    content = load_text(CHECKPOINT_FILE)
    if not content:
        state_cp = os.path.join(STATE_DIR, "LATEST_CHECKPOINT.md")
        content = load_text(state_cp)
    return content


def get_behavior_rules():
    data = load_json(os.path.join(MEMORY_DIR, "behavior.json"))
    if not data:
        data = load_json(os.path.join(STATE_DIR, "behavior.json"))
    return data.get("preferences", {})


def get_recent_mistakes(limit=3):
    content = load_text(os.path.join(MEMORY_DIR, "mistakes.md"))
    if not content:
        content = load_text(os.path.join(STATE_DIR, "mistakes.md"))
    
    mistakes = []
    lines = content.splitlines()
    for line in lines:
        if line.startswith("|") and not line.startswith("| วันที่") and not line.startswith("| :---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4:
                date, problem, cause, fix = parts[0], parts[1], parts[2], parts[3]
                mistakes.append({
                    "date": date,
                    "problem": problem.replace("<br>", " "),
                    "fix": fix.replace("<br>", " ")
                })
    return mistakes[-limit:]


def hydrate_session():
    rules = get_behavior_rules()
    mistakes = get_recent_mistakes()
    checkpoint = get_latest_checkpoint()
    
    out_dir = os.path.join(PROJECT_ROOT, "Folder_Out")
    pdf_files = glob.glob(os.path.join(out_dir, "*.pdf")) if os.path.exists(out_dir) else []
    
    briefing = {
        "project_name": os.path.basename(PROJECT_ROOT),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "checkpoint": checkpoint.strip() if checkpoint else "No LATEST_CHECKPOINT.md found.",
        "key_standards": {
            "slip_mode_standard": rules.get("forensic_smart_zoom_crop_standard", "Stage Forensic Smart Zoom & Crop"),
            "chat_evidence_standard": rules.get("chat_evidence_gold_standard", "Standard Dicut_Chat 13-row strip"),
            "honesty_rule": rules.get("strict_honesty_zero_guessing_rule", "Strict Zero-Guessing"),
            "table_styling": rules.get("table_grid_styling_rules", "Sarabun Center-Aligned Grid"),
            "pdf_engine": rules.get("pymupdf_c_binding_standard", "PyMuPDF C-Binding Engine")
        },
        "recent_mistakes_to_avoid": mistakes,
        "recent_artifacts": [os.path.basename(p) for p in sorted(pdf_files, key=os.path.getmtime, reverse=True)[:5]]
    }
    return briefing


def main():
    briefing = hydrate_session()
    
    if "--json" in sys.argv:
        print(json.dumps(briefing, ensure_ascii=False, indent=2))
        return

    print("=" * 70)
    print(" 🏛️ IMMORTAL AGENT PROTOCOL — PROJECT STATE HYDRATED")
    print(f" Project: {briefing['project_name']} | Time: {briefing['timestamp']}")
    print("=" * 70)
    
    print("\n📌 [1. ACTIVE CHECKPOINT (สถานะงานล่าสุด)]:")
    if briefing['checkpoint'] and briefing['checkpoint'] != "No LATEST_CHECKPOINT.md found.":
        for l in briefing['checkpoint'].splitlines()[:15]:
            print(f"  {l}")
    else:
        print("  พร้อมลุยต่อจากจุดล่าสุด")

    print("\n⚖️ [2. KEY ENFORCED STANDARDS (กฎและมาตรฐานที่ตกลงไว้)]:")
    for k, v in briefing['key_standards'].items():
        summary_val = (v[:90] + "...") if len(v) > 90 else v
        print(f"  • {k}: {summary_val}")

    if briefing['recent_mistakes_to_avoid']:
        print("\n🛡️ [3. HISTORICAL IMMUNITY (ข้อผิดพลาดที่ต้องระวัง)]:")
        for m in briefing['recent_mistakes_to_avoid']:
            print(f"  • [{m['date']}] {m['problem'][:50]}... -> วิธีแก้: {m['fix'][:60]}...")

    if briefing['recent_artifacts']:
        print("\n📂 [4. RECENT ARTIFACTS IN FOLDER_OUT]:")
        for a in briefing['recent_artifacts']:
            print(f"  • {a}")

    print("\n" + "=" * 70)
    print(" 🚀 เอเจนต์ตื่นขึ้นในร่างเดิมสมบูรณ์ 100% — พร้อมรับคำสั่งต่อไปทันที")
    print("=" * 70)


if __name__ == "__main__":
    main()
