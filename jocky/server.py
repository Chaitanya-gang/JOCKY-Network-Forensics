"""
JOCKY Web Studio Server - Lightweight HTTP Server with REST APIs
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from typing import Dict, Any

from jocky.runtime import Runtime
from jocky.cluster import JockyCluster
from jocky.reporter import Reporter


PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class JockyAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/scenarios":
            self.send_json_response(self.get_scenarios())
        elif path == "/api/evidence-files":
            self.send_json_response(self.get_evidence_files())
        elif path == "/api/latest-report":
            self.serve_latest_report()
        else:
            # Fall back to static files in jocky/web/
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            body = {}

        if path == "/api/run":
            self.handle_run(body)
        elif path == "/api/multi-run":
            self.handle_multi_run(body)
        else:
            self.send_error(404, "Endpoint not found")

    def handle_run(self, body: Dict[str, Any]):
        code = body.get("code", "")
        host = body.get("host", "LAB-WIN-01")
        
        if not code:
            self.send_json_response({"success": False, "error": "No code provided"}, status=400)
            return

        try:
            runtime = Runtime(base_dir=os.getcwd(), host_name=host)
            result = runtime.execute_script(code)
            reports = runtime.generate_report("all")

            # Extract structured evidence items for UI
            items = [item.to_dict() for item in runtime.evidence_vault.items]
            
            # Read generated HTML report if available
            html_content = ""
            if "html" in reports and os.path.exists(reports["html"]):
                with open(reports["html"], "r", encoding="utf-8") as f:
                    html_content = f.read()

            response = {
                "success": True,
                "execution_record": result["execution_record"],
                "logs": result["logs"],
                "evidence_count": result["evidence_count"],
                "evidence_hash": result["evidence_hash"],
                "evidence_items": items,
                "report_html": html_content
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def handle_multi_run(self, body: Dict[str, Any]):
        code = body.get("code", "")
        hosts = body.get("hosts", ["LAB-WIN-01", "LAB-WIN-02", "PROD-UBUNTU-01"])

        if not code:
            self.send_json_response({"success": False, "error": "No code provided"}, status=400)
            return

        try:
            cluster = JockyCluster(base_dir=os.getcwd())
            res = cluster.run_multi_host(code, hosts)
            self.send_json_response({"success": True, "cluster": res})
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, status=500)

    def get_scenarios(self) -> Dict[str, Any]:
        scenarios = []
        inv_dir = os.path.join(os.getcwd(), "investigation")
        
        # Load known script files
        sample_files = [
            ("case.jky", "Core Incident Triage (INCIDENT_001)", "Official PS demonstration script checking processes, evidence files, and network sockets."),
            ("ransomware_hunt.jky", "Ransomware Rapid File Sweep", "Loops through all files, computes cryptographic SHA-256 digests and indexes suspicious extensions."),
            ("fleet_sweep.jky", "Multi-Host Persistence Audit", "Distributed sweep across all corporate endpoints for unauthorized running binaries.")
        ]

        for fname, title, desc in sample_files:
            fpath = os.path.join(inv_dir, fname)
            code = ""
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    code = f.read()
            scenarios.append({
                "id": fname.replace(".jky", ""),
                "filename": fname,
                "title": title,
                "description": desc,
                "code": code
            })

        return {"scenarios": scenarios}

    def get_evidence_files(self) -> Dict[str, Any]:
        ev_dir = os.path.join(os.getcwd(), "investigation", "evidence")
        files_data = []
        if os.path.exists(ev_dir):
            for fname in sorted(os.listdir(ev_dir)):
                fpath = os.path.join(ev_dir, fname)
                if os.path.isfile(fpath):
                    files_data.append({
                        "name": fname,
                        "size": os.path.getsize(fpath),
                        "path": fpath
                    })
        return {"files": files_data}

    def serve_latest_report(self):
        rep_dir = os.path.join(os.getcwd(), "investigation", "reports")
        if os.path.exists(rep_dir):
            html_files = [f for f in os.listdir(rep_dir) if f.endswith(".html")]
            if html_files:
                latest = os.path.join(rep_dir, sorted(html_files)[-1])
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(latest, 'rb') as f:
                    self.wfile.write(f.read())
                return
        self.send_error(404, "No report found")

    def send_json_response(self, data: Dict[str, Any], status: int = 200):
        payload = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def start_server(port: int = 8000):
    server_address = ('', port)
    # Ensure port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, JockyAPIHandler) as httpd:
        print(f"\n==============================================================")
        print(f"   ⚡ JOCKY FORENSIC STUDIO & WEB IDE RUNNING ON PORT {port}   ")
        print(f"==============================================================")
        print(f"👉 Open in browser: http://localhost:{port}")
        print(f"Press Ctrl+C to stop.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down JOCKY Web Server...")
            httpd.server_close()


if __name__ == "__main__":
    start_server(8000)
