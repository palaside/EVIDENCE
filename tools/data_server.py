# -*- coding: utf-8 -*-
"""
LIGHTWEIGHT DIGITAL EVIDENCE DATA & SCAFFOLDING HTTP SERVER
- Port: 8088
- Serves static SPA & Sandbox
- Provides live data endpoints for 560 Master Slips & Chat Correlations
- Provides live Parametric Configuration update endpoint
- Full CORS & Route Fallback support
"""
import os
import sys
import json
import http.server
import socketserver
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from tools.scaffold_agent import generate_sandbox_bundle, load_config, log_event, CONFIG_PATH, clean_person_name
from tools.pdf_export import PdfExportError, export_canvas_pages_to_pdf

PORT = 8088

class EvidenceRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        # Health / Status check
        if path in ["/api/health", "/health", "/status", "/api/status"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "service": "DIGITAL_EVIDENCE_SERVER",
                "port": PORT,
                "agent": "Autonomous Coding Agent (watchandslice)"
            }).encode("utf-8"))
            return

        # Live Data Bundle & Slips
        elif path in ["/api/data", "/api/slips", "/api/evidence", "/api/chat-correlations"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            
            bundle_file = BASE_DIR / "sandbox" / "live_evidence_data.json"
            if not bundle_file.exists():
                bundle = generate_sandbox_bundle()
            else:
                with open(bundle_file, "r", encoding="utf-8") as f:
                    bundle = json.load(f)
            self.wfile.write(json.dumps(bundle, ensure_ascii=False).encode("utf-8"))
            return

        # Config SSOT
        elif path in ["/api/config", "/config"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            config = load_config()
            self.wfile.write(json.dumps(config, ensure_ascii=False).encode("utf-8"))
            return

        # Route to prototype by default
        elif path in ["", "/", "/app", "/studio", "/glass-studio", "/glass-studio/liquid"]:
            self.path = "/PROJECT_EVIDENCE_3COL_PROTOTYPE.html"

        # Check if requesting a valid file in workspace
        target_path = BASE_DIR / self.path.lstrip('/')
        if not target_path.exists() and path.startswith('/api/'):
            # Fallback for any unknown API route
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "message": f"Endpoint {path} routed to Evidence Engine",
                "availableEndpoints": ["/api/data", "/api/slips", "/api/config", "/api/health"]
            }, ensure_ascii=False).encode("utf-8"))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        if path in ["/api/pdf/export", "/pdf/export"]:
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0 or length > 64 * 1024 * 1024:
                self.send_response(413)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "error": "PDF export payload is empty or too large."
                }, ensure_ascii=False).encode("utf-8"))
                return

            body = self.rfile.read(length).decode("utf-8")
            try:
                payload = json.loads(body)
                result = export_canvas_pages_to_pdf(payload, BASE_DIR)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except (json.JSONDecodeError, PdfExportError) as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": f"PDF export failed: {e}"}, ensure_ascii=False).encode("utf-8"))
            return
        
        if path in ["/api/config", "/config"]:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                new_config = json.loads(body)
                with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(new_config, f, ensure_ascii=False, indent=2)
                
                bundle = generate_sandbox_bundle()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "message": "Config updated & bundle resliced",
                    "metrics": bundle.get("metrics", {})
                }, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode("utf-8"))
            return

        # Fallback for any unknown POST endpoint
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "acknowledged",
            "endpoint": path,
            "message": "Evidence API received request successfully"
        }, ensure_ascii=False).encode("utf-8"))

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), EvidenceRequestHandler) as httpd:
        log_event(f"Digital Evidence Data Server running on http://127.0.0.1:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            log_event("Server stopped by user.")

if __name__ == "__main__":
    run_server()
