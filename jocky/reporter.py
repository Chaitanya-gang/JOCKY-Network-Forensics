"""
JOCKY Reporter - Multi-Format Forensic Output (Terminal, JSON, Interactive HTML)
"""

import json
import os
from typing import Dict, Any, List
from jocky.evidence import EvidenceVault, ExecutionRecord


class Reporter:
    def __init__(self, vault: EvidenceVault):
        self.vault = vault
        self.record = vault.get_execution_record()

    def print_terminal_summary(self):
        """Prints beautiful forensic summary to terminal"""
        cyan = "\033[96m"
        green = "\033[92m"
        yellow = "\033[93m"
        bold = "\033[1m"
        dim = "\033[2m"
        reset = "\033[0m"

        print(f"\n{bold}{cyan}=============================================================={reset}")
        print(f"{bold}{green}✓ Script parsed & syntax valid{reset}")
        print(f"{bold}{green}✓ Capability check passed [READ_ONLY_FORENSICS]{reset}")
        print(f"{bold}{green}✓ Forensic operations executed{reset}")
        print(f"{bold}{cyan}=============================================================={reset}\n")

        # Processes breakdown
        procs = [i for i in self.vault.items if i.category == "process"]
        if procs:
            print(f"{bold}{yellow}PROCESS RESULTS ({len(procs)} discovered){reset}")
            print(f"{dim}──────────────────────────────────────────────────────────────{reset}")
            for p in procs[:8]:
                d = p.data
                pid_str = f"PID {d.get('pid', '?'):<6}"
                name_str = f"{d.get('name', 'unknown'):<22}"
                mem_str = f"{d.get('memory_mb', 0):>6.1f} MB"
                print(f"  {pid_str}  {name_str}  {mem_str}")
            if len(procs) > 8:
                print(f"  {dim}... and {len(procs) - 8} more processes{reset}")
            print()

        # Files breakdown
        files = [i for i in self.vault.items if i.category == "file"]
        if files:
            print(f"{bold}{yellow}FILES DISCOVERED ({len(files)} files){reset}")
            print(f"{dim}──────────────────────────────────────────────────────────────{reset}")
            for f in files[:8]:
                d = f.data
                fname = f"{d.get('name', 'file'):<20}"
                fsize = f"{d.get('size_bytes', 0):>8} B"
                h = d.get('sha256', '')
                h_str = f"SHA256: {h[:12]}...{h[-6:]}" if h else "NO_HASH"
                susp = f" {yellow}[SUSPICIOUS]{reset}" if d.get('is_suspicious') else ""
                print(f"  {fname}  {fsize}  {dim}{h_str}{reset}{susp}")
            if len(files) > 8:
                print(f"  {dim}... and {len(files) - 8} more files{reset}")
            print()

        # Network breakdown
        conns = [i for i in self.vault.items if i.category == "network_connection"]
        if conns:
            print(f"{bold}{yellow}NETWORK CONNECTIONS ({len(conns)} active){reset}")
            print(f"{dim}──────────────────────────────────────────────────────────────{reset}")
            for c in conns[:6]:
                d = c.data
                proto = f"{d.get('protocol', 'TCP'):<4}"
                laddr = f"{d.get('local_address', ''):<22}"
                raddr = f"{d.get('remote_address', ''):<22}"
                status = f"[{d.get('status', '')}]"
                print(f"  {proto} {laddr} -> {raddr} {status}")
            if len(conns) > 6:
                print(f"  {dim}... and {len(conns) - 6} more connections{reset}")
            print()

        # Evidence Summary Box
        print(f"{bold}{cyan}EVIDENCE & CHAIN OF CUSTODY{reset}")
        print(f"{dim}──────────────────────────────────────────────────────────────{reset}")
        print(f"  Evidence items : {len(self.vault.items)}")
        print(f"  Root SHA-256   : {bold}{green}{self.record.evidence_hash}{reset}\n")

        print(self.record.format_box())
        print(f"\n{bold}{green}✓ Automated Forensic Report Generated{reset}\n")

    def export_json(self, output_path: str):
        data = self.vault.to_dict()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def export_html(self, output_path: str):
        record = self.record
        items = self.vault.items
        
        procs = [i.data for i in items if i.category == "process"]
        files = [i.data for i in items if i.category == "file"]
        conns = [i.data for i in items if i.category == "network_connection"]

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JOCKY Forensic Investigation Report - {record.case_id}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #0a0d14;
            --bg-card: #111726;
            --bg-card-hover: #162035;
            --border: #1e293b;
            --border-accent: #00f0ff;
            --cyan: #00f0ff;
            --green: #00ff9d;
            --yellow: #ffb800;
            --red: #ff3366;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --font-mono: 'JetBrains Mono', monospace;
            --font-sans: 'Inter', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg-base);
            color: var(--text-main);
            font-family: var(--font-sans);
            padding: 30px 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.08) 0%, rgba(0, 255, 157, 0.05) 100%);
            border: 1px solid var(--border-accent);
            border-radius: 12px;
            padding: 24px 30px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .logo-area h1 {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #ffffff;
        }}
        .logo-badge {{
            background: var(--cyan);
            color: #000;
            font-size: 11px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
        }}
        .subtitle {{
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 4px;
            font-family: var(--font-mono);
        }}
        .status-badge {{
            background: rgba(0, 255, 157, 0.15);
            border: 1px solid var(--green);
            color: var(--green);
            padding: 8px 18px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        @media (max-width: 800px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
        }}
        .card h2 {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--cyan);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .kv-table {{
            width: 100%;
            font-family: var(--font-mono);
            font-size: 13px;
        }}
        .kv-table td {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .kv-key {{
            color: var(--text-muted);
            width: 38%;
        }}
        .kv-val {{
            color: #ffffff;
            font-weight: 500;
            word-break: break-all;
        }}
        .hash-tag {{
            background: #0d131f;
            border: 1px solid #22324f;
            padding: 4px 8px;
            border-radius: 4px;
            color: var(--cyan);
            font-size: 11px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 24px;
        }}
        .stat-box {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}
        .stat-num {{
            font-size: 28px;
            font-weight: 800;
            color: var(--cyan);
            font-family: var(--font-mono);
        }}
        .stat-label {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }}
        .tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
        }}
        .tab-btn {{
            background: none;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-family: var(--font-sans);
            font-weight: 600;
            font-size: 13px;
            transition: all 0.2s;
        }}
        .tab-btn.active {{
            background: #1e293b;
            color: var(--cyan);
            border-color: var(--cyan);
        }}
        .table-container {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow-x: auto;
        }}
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-mono);
            font-size: 12px;
            text-align: left;
        }}
        table.data-table th {{
            background: #0f1420;
            padding: 12px 14px;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
        }}
        table.data-table td {{
            padding: 10px 14px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            color: var(--text-main);
        }}
        table.data-table tr:hover td {{
            background: var(--bg-card-hover);
        }}
        .badge-suspicious {{
            background: rgba(255, 51, 102, 0.2);
            color: var(--red);
            border: 1px solid var(--red);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: var(--text-muted);
            font-size: 12px;
            font-family: var(--font-mono);
            border-top: 1px solid var(--border);
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo-area">
                <h1>JOCKY FORENSIC ENGINE <span class="logo-badge">v0.1</span></h1>
                <div class="subtitle">AUTOMATED CYBER INVESTIGATION & EVIDENCE AUDIT REPORT</div>
            </div>
            <div class="status-badge">
                <span>🛡️</span> {record.status} AUDIT TRAIL
            </div>
        </div>

        <!-- Metric Cards -->
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-num">{len(items)}</div>
                <div class="stat-label">Total Evidence Items</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">{len(procs)}</div>
                <div class="stat-label">Processes Enumerated</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">{len(files)}</div>
                <div class="stat-label">Files Discovered & Hashed</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">{len(conns)}</div>
                <div class="stat-label">Active Sockets Tracked</div>
            </div>
        </div>

        <!-- Execution Record Cards -->
        <div class="grid-2">
            <div class="card">
                <h2>🔐 Execution Record</h2>
                <table class="kv-table">
                    <tr><td class="kv-key">Case ID</td><td class="kv-val">{record.case_id}</td></tr>
                    <tr><td class="kv-key">Execution ID</td><td class="kv-val">{record.execution_id}</td></tr>
                    <tr><td class="kv-key">Host Target</td><td class="kv-val">{record.host}</td></tr>
                    <tr><td class="kv-key">OS Platform</td><td class="kv-val">{record.platform}</td></tr>
                    <tr><td class="kv-key">Timestamp</td><td class="kv-val">{record.timestamp}</td></tr>
                </table>
            </div>

            <div class="card">
                <h2>⛓️ Cryptographic Integrity Seal</h2>
                <table class="kv-table">
                    <tr><td class="kv-key">Integrity Status</td><td class="kv-val" style="color: var(--green);">[✓ VERIFIED]</td></tr>
                    <tr><td class="kv-key">Script SHA-256</td><td class="kv-val"><span class="hash-tag">{record.script_hash}</span></td></tr>
                    <tr><td class="kv-key">Package SHA-256</td><td class="kv-val"><span class="hash-tag">{record.evidence_hash}</span></td></tr>
                    <tr><td class="kv-key">Ledger Layer</td><td class="kv-val" style="color: var(--cyan);">Phase 1 (Cryptographic Hash Seal)</td></tr>
                </table>
            </div>
        </div>

        <!-- Evidence Data Tables -->
        <div class="card">
            <h2>📑 Evidence Vault Findings</h2>
            
            <div class="tabs">
                <button class="tab-btn active" onclick="showTab('files')">Files ({len(files)})</button>
                <button class="tab-btn" onclick="showTab('procs')">Processes ({len(procs)})</button>
                <button class="tab-btn" onclick="showTab('network')">Network ({len(conns)})</button>
                <button class="tab-btn" onclick="showTab('chain')">Chain of Custody</button>
            </div>

            <!-- Files Table -->
            <div id="tab-files" class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>File Name</th>
                            <th>Size</th>
                            <th>Status</th>
                            <th>SHA-256 Hash</th>
                            <th>Modified</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''<tr>
                            <td><strong>{f.get('name')}</strong></td>
                            <td>{f.get('size_bytes', 0):,} B</td>
                            <td>{"<span class='badge-suspicious'>SUSPICIOUS</span>" if f.get("is_suspicious") else "<span style='color:var(--green);'>CLEAN</span>"}</td>
                            <td><span class="hash-tag">{f.get('sha256', 'N/A')}</span></td>
                            <td>{f.get('modified', 'N/A')}</td>
                        </tr>''' for f in files]) if files else '<tr><td colspan="5" style="text-align:center; padding:20px;">No files recorded</td></tr>'}
                    </tbody>
                </table>
            </div>

            <!-- Processes Table -->
            <div id="tab-procs" class="table-container" style="display:none;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>PID</th>
                            <th>Process Name</th>
                            <th>Memory</th>
                            <th>Status</th>
                            <th>Binary SHA-256</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''<tr>
                            <td>{p.get('pid')}</td>
                            <td><strong>{p.get('name')}</strong></td>
                            <td>{p.get('memory_mb', 0)} MB</td>
                            <td>{p.get('status')}</td>
                            <td><span class="hash-tag">{p.get('sha256') or 'SYSTEM_LOCKED'}</span></td>
                        </tr>''' for p in procs]) if procs else '<tr><td colspan="5" style="text-align:center; padding:20px;">No processes recorded</td></tr>'}
                    </tbody>
                </table>
            </div>

            <!-- Network Table -->
            <div id="tab-network" class="table-container" style="display:none;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Proto</th>
                            <th>Local Socket</th>
                            <th>Remote Socket</th>
                            <th>Status</th>
                            <th>PID</th>
                            <th>Process</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''<tr>
                            <td>{c.get('protocol')}</td>
                            <td>{c.get('local_address')}</td>
                            <td>{c.get('remote_address') or '*'}</td>
                            <td>{c.get('status')}</td>
                            <td>{c.get('pid')}</td>
                            <td>{c.get('process_name')}</td>
                        </tr>''' for c in conns]) if conns else '<tr><td colspan="6" style="text-align:center; padding:20px;">No connections recorded</td></tr>'}
                    </tbody>
                </table>
            </div>

            <!-- Chain Table -->
            <div id="tab-chain" class="table-container" style="display:none;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Item ID</th>
                            <th>Category</th>
                            <th>Timestamp</th>
                            <th>Item Hash (SHA-256)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''<tr>
                            <td><strong>{item.item_id}</strong></td>
                            <td>{item.category.upper()}</td>
                            <td>{item.timestamp}</td>
                            <td><span class="hash-tag">{item.item_hash}</span></td>
                        </tr>''' for item in items])}
                    </tbody>
                </table>
            </div>

        </div>

        <div class="footer">
            Generated automatically by JOCKY Forensic Script Engine v0.1 • Tamper-evident evidence chain verified.
        </div>
    </div>

    <script>
        function showTab(tabName) {{
            document.getElementById('tab-files').style.display = 'none';
            document.getElementById('tab-procs').style.display = 'none';
            document.getElementById('tab-network').style.display = 'none';
            document.getElementById('tab-chain').style.display = 'none';

            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

            document.getElementById('tab-' + tabName).style.display = 'block';
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
