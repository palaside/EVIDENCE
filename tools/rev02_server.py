# -*- coding: utf-8 -*-
"""REV02 real-execution backend (NEW file, originals untouched).

Serves project root statically on 127.0.0.1:8010 and exposes REAL job APIs
that spawn the legacy pipeline with the conda interpreter (has cv2+fitz).
No mocks: every result comes from subprocess/files on disk.
Allowlist: inputs must live under D:/Project/DIGITAL_EVIDENCE, F:/Project/EDOK,
or Portable INBOX dirs. Outputs go to Folder_Out only.
"""
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE = Path(__file__).resolve().parent.parent
CONDA_PY = Path(os.environ.get("USERPROFILE", r"C:\Users\EVE")) / "miniconda3" / "python.exe"
if not CONDA_PY.exists():
    CONDA_PY = Path(sys.executable)
OUT_DIR = BASE / "Folder_Out"
JOB_DIR = BASE / "state" / "rev02_jobs"
JOB_DIR.mkdir(parents=True, exist_ok=True)
UP_DIR = BASE / "state" / "rev02_uploads"
UP_DIR.mkdir(parents=True, exist_ok=True)
PORT = 8010
MAX_JOBS = 2
UP_EXTS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_MB = 40
MAX_TOTAL_MB = 200
import re as _re
PROG_RE = _re.compile(r"\[(\d+)\s*/\s*(\d+)\]")

ALLOWED_INPUT_ROOTS = [
    (BASE / "EVIDENCE_IN").resolve(),
    (BASE / "EVIDENCE_CHAT_IN").resolve(),
    (BASE / "Portable").resolve(),
    (BASE / "Folder_Out").resolve(),
    Path(r"F:\Project\EDOK"),
]
ALLOWED_JSON_DIR = (BASE / "Folder_Out").resolve()

JOBS = {}
LOCK = threading.Lock()


def allow_input(p: str):
    try:
        rp = Path(p).resolve()
    except Exception:
        return None
    if not rp.exists():
        return None
    for root in ALLOWED_INPUT_ROOTS:
        try:
            if rp == root or root in rp.parents or rp == root:
                return rp
        except Exception:
            continue
    # also allow any path strictly under BASE (project-local new uploads excluded -> must exist)
    try:
        if BASE.resolve() in rp.parents:
            return rp
    except Exception:
        pass
    return None


def run_job(cmd, label, total=None, json_out=None, xlsx_out=None):
    jid = uuid.uuid4().hex[:8]
    log = JOB_DIR / (jid + ".log")
    rec = {"id": jid, "label": label, "cmd": cmd, "status": "queued",
           "exit": None, "log": str(log), "started": time.time(), "ended": None,
           "percent": 0, "total": total, "json_out": json_out, "xlsx_out": xlsx_out}
    with LOCK:
        running = sum(1 for j in JOBS.values() if j["status"] == "running")
        if running >= MAX_JOBS:
            rec["status"] = "rejected"
            rec["error"] = "max %d concurrent jobs" % MAX_JOBS
            JOBS[jid] = rec
            return rec
        JOBS[jid] = rec

    def _t():
        rec["status"] = "running"
        try:
            with open(log, "w", encoding="utf-8") as fh:
                fh.write("$ %s\n\n" % " ".join(cmd))
                fh.flush()
                p = subprocess.Popen(cmd, cwd=str(BASE), stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
                for line in p.stdout:
                    fh.write(line)
                    m = PROG_RE.search(line)
                    if m:
                        try:
                            i, n = int(m.group(1)), int(m.group(2))
                            if n > 0:
                                rec["percent"] = max(0, min(99, round(i * 100 / n)))
                                rec["total"] = n
                        except Exception:
                            pass
                    elif "[OK] Saved" in line:
                        rec["percent"] = 100
                code = p.wait(timeout=6 * 3600)
                rec["exit"] = code
                rec["status"] = "done" if code == 0 else "failed"
                if code == 0:
                    rec["percent"] = 100
        except Exception as e:  # noqa: BLE001
            rec["status"] = "failed"
            rec["error"] = str(e)[:500]
            try:
                with open(log, "a", encoding="utf-8") as fh:
                    fh.write("\n[server-error] %s\n" % e)
            except Exception:
                pass
        rec["ended"] = time.time()
    threading.Thread(target=_t, daemon=True).start()
    return rec


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(BASE), **kw)

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b)

    def _body(self, limit=65536):
        n = int(self.headers.get("Content-Length", 0) or 0)
        if n <= 0 or n > limit:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    def do_GET(self):
        u = urlparse(self.path)
        p = u.path.rstrip("/") or "/"
        if p == "/api/status":
            pdfs = sorted(OUT_DIR.glob("*.pdf")) if OUT_DIR.exists() else []
            idx = BASE / "Folder_Out" / "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json"
            n = None
            if idx.exists():
                try:
                    j = json.loads(idx.read_text(encoding="utf-8"))
                    rows = j.get("rows", j.get("slips", j)) if isinstance(j, dict) else j
                    n = len(rows) if isinstance(rows, (list, dict)) else None
                except Exception:
                    n = None
            cp = BASE / "LATEST_CHECKPOINT.md"
            return self._json({"ok": True, "python": str(CONDA_PY),
                               "pdfs": len(pdfs), "slip_index_rows": n,
                               "checkpoint_mtime": cp.stat().st_mtime if cp.exists() else None,
                               "engines": {"ocr": (BASE / "_skills/OCR_Slip/scripts/ocr_slip.py").exists(),
                                           "chat": (BASE / "tools/process_real_chat_evidence.py").exists(),
                                           "gate": (BASE / "tools/pre_delivery_quality_gate.py").exists()}})
        if p == "/api/pdfs":
            items = []
            if OUT_DIR.exists():
                for f in sorted(OUT_DIR.glob("*.pdf"), key=lambda x: x.stat().st_mtime, reverse=True)[:50]:
                    st = f.stat()
                    items.append({"name": f.name, "path": "Folder_Out/" + f.name,
                                  "bytes": st.st_size, "mtime": st.st_mtime})
            return self._json({"ok": True, "pdfs": items})
        if p == "/api/slip-index":
            q = parse_qs(u.query)
            name = (q.get("name", ["Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json"])[0] or "")
            if "/" in name or "\\" in name or not name.endswith(".json"):
                return self._json({"ok": False, "error": "bad name"}, 400)
            f = (ALLOWED_JSON_DIR / name)
            if not f.exists():
                return self._json({"ok": False, "error": "not found"}, 404)
            try:
                j = json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                return self._json({"ok": False, "error": str(e)[:300]}, 500)
            rows = j.get("rows", j.get("slips", j)) if isinstance(j, dict) else j
            if isinstance(rows, list) and len(rows) > 300:
                rows = rows[:300]
            return self._json({"ok": True, "name": name, "total": (len(j.get("rows", j.get("slips", []))) if isinstance(j, dict) and isinstance(j.get("rows", j.get("slips", [])), list) else (len(j) if isinstance(j, list) else None)), "rows": rows})
        if p.startswith("/api/jobs/"):
            jid = p.rsplit("/", 1)[-1]
            rec = JOBS.get(jid)
            if not rec:
                return self._json({"ok": False, "error": "unknown job"}, 404)
            out = dict(rec)
            try:
                t = Path(rec["log"]).read_text(encoding="utf-8", errors="replace")
                out["log_tail"] = t[-6000:]
            except Exception:
                out["log_tail"] = ""
            return self._json({"ok": True, "job": out})
        if p == "/api/jobs":
            return self._json({"ok": True, "jobs": [{k: v for k, v in j.items() if k != "cmd"} for j in list(JOBS.values())[-20:]]})
        return super().do_GET()

    def do_POST(self):
        u = urlparse(self.path)
        p = u.path.rstrip("/") or "/"
        if p == "/api/upload":
            import base64
            body = self._body(limit=250 * 1024 * 1024)
            files = body.get("files", [])
            if not files or len(files) > 60:
                return self._json({"ok": False, "error": "no files (max 60)"}, 400)
            uid = uuid.uuid4().hex[:8]
            dest = UP_DIR / uid
            dest.mkdir(parents=True, exist_ok=True)
            saved, total_b = [], 0
            for f in files:
                name = Path(str(f.get("name", "file"))).name
                ext = Path(name).suffix.lower()
                if ext not in UP_EXTS or not name:
                    continue
                try:
                    raw = base64.b64decode(f.get("data_b64", ""), validate=True)
                except Exception:
                    continue
                if len(raw) > MAX_FILE_MB * 1024 * 1024:
                    continue
                total_b += len(raw)
                if total_b > MAX_TOTAL_MB * 1024 * 1024:
                    break
                (dest / name).write_bytes(raw)
                saved.append({"name": name, "bytes": len(raw)})
            if not saved:
                return self._json({"ok": False, "error": "no valid files (jpg/png/pdf only)"}, 400)
            return self._json({"ok": True, "uploadId": uid, "files": saved})
        body = self._body()
        if p == "/api/run/upload-slip":
            uid = str(body.get("uploadId", "") or "")
            if not _re.fullmatch(r"[0-9a-f]{8}", uid):
                return self._json({"ok": False, "error": "bad uploadId"}, 400)
            src = UP_DIR / uid
            if not src.exists():
                return self._json({"ok": False, "error": "upload not found"}, 404)
            imgs = [x for x in src.iterdir() if x.suffix.lower() in (".jpg", ".jpeg", ".png")]
            if not imgs:
                return self._json({"ok": False, "error": "no slip images in upload (jpg/png only)"}, 400)
            stamp = time.strftime("%Y%m%d_%H%M%S")
            out = str(OUT_DIR / ("REV02_%s_%s.xlsx" % (stamp, uid)))
            cmd = [str(CONDA_PY), "_skills/OCR_Slip/scripts/ocr_slip.py",
                   "--input", str(src), "--output", out]
            if body.get("maskPii"):
                cmd.append("--mask-pii")
            cmd += ["--json-out", out.replace(".xlsx", ".json")]
            return self._json({"ok": True, "job": run_job(cmd, "upload-slip", total=len(imgs),
                                                           json_out=out.replace(".xlsx", ".json"), xlsx_out=out)})
        if p == "/api/result":
            jid = str(body.get("job", "") or "")
            rec = JOBS.get(jid)
            if not rec or rec.get("status") != "done" or not rec.get("json_out"):
                return self._json({"ok": False, "error": "result not ready"}, 404)
            try:
                j = json.loads(Path(rec["json_out"]).read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                return self._json({"ok": False, "error": str(e)[:300]}, 500)
            rows = j.get("rows", j.get("slips", j)) if isinstance(j, dict) else j
            total = len(rows) if isinstance(rows, list) else None
            return self._json({"ok": True, "total": total,
                               "rows": rows[:300] if isinstance(rows, list) else rows,
                               "xlsx": Path(rec["xlsx_out"]).name if rec.get("xlsx_out") else None})
        if p == "/api/run/slip":
            rp = allow_input(str(body.get("input", "") or ""))
            if not rp:
                return self._json({"ok": False, "error": "input not in allowlist or not found"}, 400)
            out = str(OUT_DIR / ("Slip_Result_%s.xlsx" % time.strftime("%Y%m%d_%H%M%S")))
            cmd = [str(CONDA_PY), "_skills/OCR_Slip/scripts/ocr_slip.py",
                   "--input", str(rp), "--output", out]
            if body.get("maskPii"):
                cmd.append("--mask-pii")
            cmd += ["--json-out", out.replace(".xlsx", ".json")]
            return self._json({"ok": True, "job": run_job(cmd, "slip")})
        if p == "/api/run/search":
            rp = allow_input(str(body.get("pdf", "") or ""))
            if not rp or rp.suffix.lower() != ".pdf":
                return self._json({"ok": False, "error": "pdf not in allowlist"}, 400)
            cmd = [str(CONDA_PY), "_skills/Search_Slip/scripts/search_slip.py", str(rp)]
            return self._json({"ok": True, "job": run_job(cmd, "search")})
        if p == "/api/run/chat":
            cmd = [str(CONDA_PY), "tools/process_real_chat_evidence.py"]
            return self._json({"ok": True, "job": run_job(cmd, "chat"),
                               "warning": "heavy job: full 3-volume run"})
        if p == "/api/run/gate":
            cmd = [str(CONDA_PY), "tools/pre_delivery_quality_gate.py"]
            return self._json({"ok": True, "job": run_job(cmd, "gate")})
        return self._json({"ok": False, "error": "unknown endpoint"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    from socketserver import TCPServer
    TCPServer.allow_reuse_address = True
    with ThreadingHTTPServer(("127.0.0.1", PORT), H) as srv:
        print("REV02 real backend on http://127.0.0.1:%d (py=%s)" % (PORT, CONDA_PY), flush=True)
        srv.serve_forever()
