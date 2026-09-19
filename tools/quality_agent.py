#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality_agent.py — Autonomous Quality Assurance & Inspection Agent
Powered by: ask-senior (qwen2.5-coder:14b on Central Local Brain http://127.0.0.1:11434)
Role: Continuous Quality Gate Inspector across all SDLC Stages & Code Deliverables.

Core Constitution & Enforced Standards:
  1. Inspect Before Act: Scans real physical files, AST, line count, syntax, and test status.
  2. 6 Self-Review Gates: Scope, Syntax, Tests, No Regression, Security, Cleanliness.
  3. 5 Quality Review Dimensions: Spec Conformance, Architecture, TDD Rigor, Performance, Truthfulness.
  4. Anti-AI-Slop & Anti-Technical Debt: Flags lazy placeholders, memory leaks, missing error states.
  5. Gatekeeping Verdict: [APPROVED] vs [CHANGES_REQUIRED] with 2-3 actionable solutions.
"""

from __future__ import annotations

import os
import sys
import io
import json
import re
import ast
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Force UTF-8 on Windows Console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "qwen2.5-coder:14b"
FALLBACK_MODEL = "qwen2.5:latest"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Folder_Out"

QUALITY_PROMPT_SYSTEM = """คุณคือ "Senior Quality Assurance & Quality Gate Agent" (ขับเคลื่อนด้วย qwen2.5-coder:14b)
ตำแหน่ง: ผู้ตรวจวัดและประเมินคุณภาพผลงานระดับ Production-Ready ประจำทีมวิศวกรรมซอฟต์แวร์
ภารกิจ: ตรวจสอบความถูกต้อง สุนทรียภาพ ความปลอดภัย และความสมบูรณ์ของผลงานทุกขั้นตอนอย่างซื่อสัตย์ 100%

กฎเหล็กที่คุณต้องยึดถืออย่างเคร่งครัด:
1. ความซื่อสัตย์ระดับสูงสุด: ห้ามเดา ห้ามอวย ห้ามประจบ ผิดบอกผิด ถูกบอกถูก ทุกข้อสังเกตต้องอ้างอิงบรรทัดหรือไฟล์จริง (file:line)
2. เกณฑ์ตรวจสอบ 6 มิติ (Self-Review Gate):
   - Scope: ตรงตามเป้าหมายและสเปกหรือไม่ มีฟีเจอร์แปลกปลอมหรือขาดหายหรือไม่
   - Syntax & Build: ไวยากรณ์ถูกต้อง ไม่มีข้อผิดพลาด แปลงค่า/คอมไพล์ผ่าน 100%
   - Tests & Verification: มีเทสกำกับตาม TDD หรือไม่ ครอบคลุม Edge Cases และ Error Handling หรือไม่
   - No Regression: ไม่ทำลายฟังก์ชันเดิม ไม่สร้างผลข้างเคียงต่อระบบรอบข้าง
   - Security & Privacy: ไม่ฮาร์ดโค้ดคีย์/ความลับ ปลอดภัยตาม PDPA ป้องกัน Injection / Path Traversal
   - Cleanliness & Anti-Slop: ปราศจากโค้ดขยะ (Dead Code), คอมเมนต์หลอก, Placeholder ทิพย์, หรือ UI Slop
3. การตัดสินผล (Gatekeeping Verdict):
   - ให้คะแนนคุณภาพรวม (Quality Score 0 - 100)
   - ตัดสินชัดเจน: [APPROVED] (คะแนน >= 85 และไม่มีข้อผิดพลาดร้ายแรง) หรือ [CHANGES_REQUIRED]
4. เสนอทางแก้ที่ดีที่สุด: หากพบจุดบกพร่อง ต้องเสนอทางเลือกแก้ไข 2-3 ข้อพร้อมโค้ดตัวอย่างที่นำไปใช้ได้จริงทันที"""


def check_ollama_alive() -> bool:
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as res:
            return res.status == 200
    except Exception:
        return False


def call_senior_brain(prompt: str, system_prompt: str = QUALITY_PROMPT_SYSTEM, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": True,
        "options": {
            "num_ctx": 4096,
            "temperature": 0.2
        }
    }
    
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    
    collected_text = []
    try:
        with urllib.request.urlopen(req, timeout=300) as res:
            for line in res:
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        collected_text.append(token)
                        sys.stdout.write(token)
                        sys.stdout.flush()
                    if chunk.get("done", False):
                        break
        print()
        return "".join(collected_text).strip()
    except Exception as e:
        if model != FALLBACK_MODEL:
            print(f"\n[Warning] {model} ขัดข้อง ({e}) สลับใช้โมเดลสำรอง {FALLBACK_MODEL}...", file=sys.stderr)
            return call_senior_brain(prompt, system_prompt, model=FALLBACK_MODEL)
        raise RuntimeError(f"ไม่สามารถเชื่อมต่อ Local AI Brain ({e}) กรุณาตรวจสอบว่า Ollama รันอยู่หรือไม่")


def inspect_python_file(filepath: Path) -> dict:
    """Performs static code inspection on a Python file."""
    info = {
        "filepath": str(filepath),
        "lines": 0,
        "syntax_ok": True,
        "syntax_error": None,
        "classes": [],
        "functions": [],
        "imports": [],
        "has_tests": False,
        "todo_count": 0
    }
    
    try:
        content = filepath.read_text(encoding="utf-8")
        info["lines"] = len(content.splitlines())
        info["todo_count"] = len(re.findall(r"\b(TODO|FIXME|XXX|HACK)\b", content, re.IGNORECASE))
        
        # Check for test patterns
        if "test_" in filepath.name or "_test" in filepath.name or "unittest" in content or "pytest" in content or "def test_" in content:
            info["has_tests"] = True
            
        tree = ast.parse(content, filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                info["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef):
                info["functions"].append(node.name)
            elif isinstance(node, ast.Import):
                for n in node.names:
                    info["imports"].append(n.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    info["imports"].append(node.module)
    except SyntaxError as se:
        info["syntax_ok"] = False
        info["syntax_error"] = f"บรรทัด {se.lineno}: {se.msg}"
    except Exception as e:
        info["syntax_ok"] = False
        info["syntax_error"] = str(e)
        
    return info


def inspect_stage(stage_num: int, root: Path = PROJECT_ROOT) -> dict:
    """Inspects files and deliverables corresponding to an SDLC stage (0..7)."""
    stage_map = {
        0: {"name": "Idea & Pain Point", "files": ["PROJECT_IDEA.md", "PAIN_POINTS.md"]},
        1: {"name": "Specification (SDD)", "files": ["SPECIFICATION.md", "UI_BLUEPRINT.md"]},
        2: {"name": "System Planning & Architecture", "files": ["ARCHITECTURE.md", "PROJECT_FLOW.md", "tokens.css"]},
        3: {"name": "Task Breakdown", "files": ["TASKS.md", "DEPENDENCY_GRAPH.md"]},
        4: {"name": "Implementation", "files": ["tools/", "Portable/", "_skills/", "_engines/", "src/"]},
        5: {"name": "Test & Review Quality Gate", "files": ["Folder_Out/", "tests/", "memory/mistakes.md"]},
        6: {"name": "Deployment", "files": ["deploy.json", "requirements.txt", "run.bat", "run.ps1"]},
        7: {"name": "Operate & Hotfolder", "files": ["tools/tick.py", "run_silent_watcher.vbs", "install_startup.bat"]}
    }
    
    cfg = stage_map.get(stage_num, {"name": f"Stage {stage_num}", "files": []})
    found_files = []
    missing_files = []
    
    for f in cfg["files"]:
        p = root / f
        if p.exists():
            found_files.append(f)
        else:
            missing_files.append(f)
            
    return {
        "stage_num": stage_num,
        "stage_name": cfg["name"],
        "found_files": found_files,
        "missing_files": missing_files
    }


def run_agent_inspection(target_path: str = None, stage: int = None) -> dict:
    """Autonomous Agent Inspection Loop."""
    print("=" * 70)
    print("🔍 [QUALITY AGENT] เริ่มต้นกระบวนการตรวจวัดคุณภาพในโหมด Autonomous Agent")
    print(f"🧠 เอนจินประมวลผล: ask-senior ({DEFAULT_MODEL} บน Local Brain)")
    print("=" * 70)
    
    if not check_ollama_alive():
        raise SystemError("❌ ตรวจพบว่า Ollama ไม่ได้ทำงาน กรุณาเปิด Ollama บน http://127.0.0.1:11434")
        
    context_data = ""
    target_summary = ""
    
    if stage is not None:
        # Stage mode
        stage_info = inspect_stage(stage)
        target_summary = f"SDLC ขั้นที่ {stage}: {stage_info['stage_name']}"
        context_data += f"### ข้อมูลขั้นตอนการพัฒนา: {target_summary}\n"
        context_data += f"- เอกสาร/ไฟล์ที่ตรวจพบ: {', '.join(stage_info['found_files']) or 'ไม่พบ'}\n"
        context_data += f"- เอกสาร/ไฟล์ที่ยังขาด: {', '.join(stage_info['missing_files']) or 'ไม่มี'}\n\n"
        
        # Load sample content from found files
        for fn in stage_info["found_files"][:3]:
            fp = PROJECT_ROOT / fn
            if fp.is_file():
                try:
                    text = fp.read_text(encoding="utf-8")[:2500]
                    context_data += f"#### เนื้อหาของ {fn}:\n```\n{text}\n```\n\n"
                except Exception:
                    pass
    elif target_path:
        # Specific File Mode
        fp = Path(target_path)
        if not fp.is_absolute():
            fp = PROJECT_ROOT / target_path
            
        if not fp.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์ที่ระบุ: {fp}")
            
        target_summary = f"ไฟล์: {fp.relative_to(PROJECT_ROOT) if PROJECT_ROOT in fp.parents else fp.name}"
        
        if fp.suffix == ".py":
            py_info = inspect_python_file(fp)
            context_data += f"### ข้อมูลวิเคราะห์โค้ด Python ({fp.name}):\n"
            context_data += f"- จำนวนบรรทัด: {py_info['lines']}\n"
            context_data += f"- ตรวจสอบไวยากรณ์ (Syntax): {'✅ ผ่าน' if py_info['syntax_ok'] else '❌ ผิดพลาด: ' + str(py_info['syntax_error'])}\n"
            context_data += f"- คลาสที่พบ ({len(py_info['classes'])}): {', '.join(py_info['classes']) or 'ไม่มี'}\n"
            context_data += f"- ฟังก์ชันที่พบ ({len(py_info['functions'])}): {', '.join(py_info['functions'][:15])}\n"
            context_data += f"- TODO/HACK ค้างอยู่: {py_info['todo_count']} จุด\n\n"
            
        try:
            code_text = fp.read_text(encoding="utf-8")
            # Truncate if too long, keep head and tail
            if len(code_text) > 8000:
                code_snippet = code_text[:4000] + "\n\n... [โค้ดยาวเกิน ตัดส่วนกลางออก] ...\n\n" + code_text[-3000:]
            else:
                code_snippet = code_text
            context_data += f"#### ตัวอย่างซอร์สโค้ด/เนื้อหาไฟล์ ({fp.name}):\n```\n{code_snippet}\n```\n\n"
        except Exception as e:
            context_data += f"ไม่สามารถอ่านเนื้อหาไฟล์: {e}\n"
    else:
        # Default: Project Wide & Latest Deliverables
        target_summary = "ภาพรวมผลงานล่าสุดของโปรเจกต์ (Deliverables & Status)"
        chk_file = PROJECT_ROOT / "LATEST_CHECKPOINT.md"
        if chk_file.exists():
            context_data += f"### สถานะงานล่าสุด (LATEST_CHECKPOINT.md):\n```markdown\n{chk_file.read_text(encoding='utf-8')[:3000]}\n```\n\n"
            
        mst_file = PROJECT_ROOT / "memory" / "mistakes.md"
        if mst_file.exists():
            context_data += f"### บันทึกข้อผิดพลาดและกฎป้องกันซ้ำ (memory/mistakes.md):\n```markdown\n{mst_file.read_text(encoding='utf-8')[:2000]}\n```\n\n"

    prompt = f"""กรุณาทำหน้าที่เป็น Senior Quality Gate Agent ทำการตรวจวัดคุณภาพของ:
**เป้าหมาย:** {target_summary}

{context_data}

โปรดประเมินผลงานตามเกณฑ์ต่อไปนี้:
1. 📊 สรุปผลการประเมิน 6 มิติ (Scope, Syntax, Tests, No Regression, Security, Cleanliness)
2. 🎯 รายการจุดเด่น (Strengths) และจุดบกพร่องที่พบ (Defects / Vulnerabilities) พร้อมระบุตำแหน่ง
3. 🛠️ Auto Gap-Closing: เสนอโค้ด/การปรับปรุงที่จำเป็น 2-3 ทางเลือกที่ดีที่สุดในครั้งเดียว
4. ⚖️ บทสรุปฟันธง:
   - **Quality Score:** [ระบุคะแนน 0 - 100]/100
   - **Verdict:** [APPROVED] หรือ [CHANGES_REQUIRED]
   - **เหตุผลสรุปสั้น 1-2 บรรทัด**"""

    print("🧠 กำลังวิเคราะห์เชิงลึกด้วย qwen2.5-coder:14b ...")
    report_text = call_senior_brain(prompt)
    
    # Determine verdict and score
    score_match = re.search(r"Quality Score[^\d\n]*?(\d{1,3})", report_text, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else 75
    verdict = "APPROVED" if ("[APPROVED]" in report_text and score >= 80 and "[CHANGES_REQUIRED]" not in report_text) else "CHANGES_REQUIRED"
    
    # Save Report
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_path = OUTPUT_DIR / f"QUALITY_INSPECTION_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    latest_report_path = OUTPUT_DIR / "QUALITY_INSPECTION_REPORT.md"
    
    full_report = f"""# 🛡️ QUALITY INSPECTION REPORT — DIGITAL EVIDENCE
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agent Engine:** ask-senior (`{DEFAULT_MODEL}`)  
**Target:** {target_summary}  
**Overall Verdict:** **{verdict}** (Quality Score: {score}/100)  

---

{report_text}
"""
    report_path.write_text(full_report, encoding="utf-8")
    latest_report_path.write_text(full_report, encoding="utf-8")
    
    print("\n" + "=" * 70)
    print(f"📊 ผลการตรวจวัดคุณภาพ: {verdict} ({score}/100)")
    print(f"📄 บันทึกรายงานฉบับสมบูรณ์ที่: {latest_report_path}")
    print("=" * 70 + "\n")
    
    return {
        "verdict": verdict,
        "score": score,
        "target": target_summary,
        "report_file": str(latest_report_path),
        "report_content": report_text
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Quality Gate Inspector (ask-senior)")
    parser.add_argument("--target", default=None, help="Path to file to inspect (e.g. tools/process_real_chat_evidence.py)")
    parser.add_argument("--stage", type=int, default=None, help="SDLC Stage number (0..7)")
    parser.add_argument("--all", action="store_true", help="Inspect overall project health and latest checkpoint")
    args = parser.parse_args()
    
    try:
        res = run_agent_inspection(target_path=args.target, stage=args.stage)
        sys.exit(0 if res["verdict"] == "APPROVED" else 1)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการรัน Quality Agent: {e}", file=sys.stderr)
        sys.exit(2)
