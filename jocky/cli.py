import sys
import os
import argparse
import json
import hashlib

# Ensure UTF-8 stdout encoding on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from jocky.runtime import Runtime
from jocky.reporter import Reporter
from jocky.cluster import JockyCluster


def cmd_run(args):
    script_path = args.script
    if not os.path.exists(script_path):
        print(f"Error: Script file '{script_path}' not found.")
        sys.exit(1)

    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    base_dir = os.path.dirname(os.path.abspath(script_path)) or os.getcwd()
    runtime = Runtime(base_dir=os.getcwd())
    
    try:
        res = runtime.execute_script(code)
        # Always generate reports
        runtime.generate_report("all")
        reporter = Reporter(runtime.evidence_vault)
        reporter.print_terminal_summary()
    except Exception as e:
        print(f"\nExecution Failed: {e}")
        sys.exit(1)


def cmd_multi(args):
    script_path = args.script
    if not os.path.exists(script_path):
        print(f"Error: Script file '{script_path}' not found.")
        sys.exit(1)

    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()

    hosts = args.hosts.split(",") if args.hosts else ["LAB-WIN-01", "LAB-WIN-02", "PROD-UBUNTU-01"]
    cluster = JockyCluster(base_dir=os.getcwd())
    
    try:
        res = cluster.run_multi_host(code, hosts)
        cluster.print_cluster_summary(res)
    except Exception as e:
        print(f"\nMulti-Host Execution Failed: {e}")
        sys.exit(1)


def cmd_verify(args):
    report_path = args.report_file
    if not os.path.exists(report_path):
        print(f"Error: Report file '{report_path}' not found.")
        sys.exit(1)

    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rec = data.get("execution_record", {})
    items = data.get("evidence_items", [])
    expected_hash = rec.get("evidence_hash", "")
    case_id = rec.get("case_id", "")
    host = rec.get("host", "")

    # Recompute hashes
    item_hashes = []
    for item in items:
        payload = {
            "item_id": item["item_id"],
            "category": item["category"],
            "data": item["data"],
            "timestamp": item["timestamp"]
        }
        canonical = json.dumps(payload, sort_keys=True)
        h = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        item_hashes.append(h)

    combined = "|".join(item_hashes) + f"|{case_id}|{host}"
    calculated_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()

    print("\n==============================================================")
    print("           JOCKY EVIDENCE CRYPTOGRAPHIC VERIFICATION           ")
    print("==============================================================")
    print(f"Case ID           : {case_id}")
    print(f"Execution ID      : {rec.get('execution_id')}")
    print(f"Evidence Items    : {len(items)}")
    print(f"Recorded Root Hash: {expected_hash}")
    print(f"Verified Root Hash: {calculated_hash}")

    if calculated_hash == expected_hash:
        print("\n\033[92m[✓ VERIFIED] Evidence integrity intact. No tampering detected.\033[0m\n")
    else:
        print("\n\033[91m[✗ TAMPERED] Hash mismatch! Evidence package has been altered.\033[0m\n")


def cmd_web(args):
    from jocky.server import start_server
    start_server(port=args.port)


def main():
    parser = argparse.ArgumentParser(
        prog="jocky",
        description="JOCKY - Domain Specific Forensic Scripting Language & Execution Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a single JOCKY forensic script")
    run_parser.add_argument("script", help="Path to .jky script file")

    # Multi command
    multi_parser = subparsers.add_parser("multi", help="Execute script across distributed hosts")
    multi_parser.add_argument("script", help="Path to .jky script file")
    multi_parser.add_argument("--hosts", default="LAB-WIN-01,LAB-WIN-02,PROD-UBUNTU-01", help="Comma-separated hostnames")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Cryptographically verify an evidence package")
    verify_parser.add_argument("report_file", help="Path to report.json")

    # Web IDE command
    web_parser = subparsers.add_parser("web", help="Start the JOCKY Web IDE & Forensic Studio")
    web_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default 8000)")

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(args)
    elif args.command == "multi":
        cmd_multi(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "web":
        cmd_web(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
