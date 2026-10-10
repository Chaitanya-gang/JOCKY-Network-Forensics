# JOCKY — Network Forensics Framework

**Investigate. Correlate. Verify. Without Compromising Evidence.**

JOCKY is a prototype forensic scripting language and investigation framework for expressing repeatable computer and network forensic workflows as readable `.jky` scripts. It combines a custom lexer and parser, a Python runtime, host telemetry modules, evidence hashing, and JSON/HTML report generation.

Developed for **Smart India Hackathon 2026 — Problem Statement 26148**.

## Overview

Digital investigations often involve disconnected tools and one-off scripts, making workflows harder to repeat, audit, and report consistently. JOCKY explores a higher-level approach: investigators describe an investigation in a dedicated domain-specific language (DSL), and the framework interprets the script and collects supported evidence.

### At a glance

- **Implementation language:** Python
- **Investigation language:** JOCKY (`.jky`)
- **Analysis areas:** process information, file metadata and hashes, local network connections
- **Evidence integrity:** SHA-256 hashes and a package-level digest
- **Reports:** JSON and HTML
- **Interfaces:** command-line runner and local web interface
- **Tests:** Python `unittest`

## Problem Statement

**SIH 2026 — PS ID 26148**

*Creation of Scripts/Functions with New Programming Language to Commence Computer & Network Forensic Analysis Without Triggering Security Solutions.*

JOCKY explores how a purpose-built forensic DSL can make investigation steps easier to express, reuse, and execute through a consistent runtime. The prototype focuses on workflow orchestration, supported host telemetry, evidence packaging, integrity checks, and report generation.

> JOCKY does not guarantee that its activity will avoid detection by security products. The prototype does not implement stealth or security-control bypass functionality; its goal is to provide a readable and repeatable forensic workflow.

## Architecture

```text
Investigation script (.jky)
          |
          v
        Lexer
          |
          v
     Parser / AST
          |
          v
    Python runtime
          |
    +-----+----------------+
    |          |           |
    v          v           v
 Processes    Files      Network
    |          |           |
    +----------+-----------+
               |
               v
         Evidence Vault
               |
               v
       SHA-256 integrity data
               |
               v
       JSON / HTML reports
```

### Execution flow

1. The investigator selects a `.jky` investigation script.
2. The lexer converts source text into tokens.
3. The parser builds the syntax representation used by the runtime.
4. The runtime invokes supported process, file, and network modules.
5. Evidence records are collected and hashed.
6. A report is generated with case/execution metadata and integrity information.
7. The verification command can recompute the report's evidence digest and compare it with the recorded value.

## Features

### 1. JOCKY forensic DSL

The custom `.jky` language supports syntax implemented in the prototype, including case declarations, variable assignments, function and member calls, loops, conditionals, comparisons, and output statements. The DSL is interpreted by the Python runtime; it is **not currently a native compiled language**.

Illustrative workflow:

```jocky
CASE "INCIDENT_001"

processes = host.processes()
files = host.files.search("./investigation/evidence")
connections = host.network.connections()

evidence.add(processes)
evidence.add(files)
evidence.add(connections)

evidence.hash()
report.generate()
```

This example illustrates the intended workflow. Refer to the `.jky` files in `investigation/` for scripts supported by the current checkout.

### 2. Process inspection

The process module can collect available host process information, such as process ID, name, executable path, user, CPU/memory information, status, and command line, subject to operating-system permissions and the fields exposed by the runtime.

### 3. File discovery and hashing

The file module searches configured paths and records file metadata. The prototype supports cryptographic hashing for evidence integrity. File extensions or names may be used as simple triage indicators; these heuristics **do not establish that a file is malicious**.

### 4. Network connection inspection

The network module can inspect local socket/connection information exposed by the host environment. This is **not packet capture**, full network traffic analysis, or remote network surveillance.

### 5. Evidence integrity

JOCKY records hashes for collected evidence and a package-level digest. The verification command recalculates the digest from stored report data and checks whether it matches the recorded value.

This can help identify changes to the data covered by the digest. It does not, by itself, prove who collected the evidence, when collection occurred, or that the original collection process was forensically sound. The prototype does not claim a legally certified chain of custody.

### 6. JSON and HTML reporting

The framework generates machine-readable JSON reports and human-readable HTML reports for supported investigation runs.

### 7. Local web interface

The project includes a web interface served locally for interacting with the prototype. It is intended for local demonstration and should not be exposed to an untrusted network without appropriate security review.

### 8. Multi-host workflow prototype

The repository includes a multi-host orchestration path for demonstrating repeated investigation workflows across named host profiles. In the current prototype, this is a **controlled simulation**, not a production remote endpoint agent or verified remote execution system.

## Repository Structure

```text
JOCKY-Network-Forensics/
├── investigation/
│   ├── evidence/
│   ├── reports/
│   ├── case.jky
│   ├── fleet_sweep.jky
│   └── ransomware_hunt.jky
├── jocky/
│   ├── modules/
│   ├── web/
│   ├── cli.py
│   ├── cluster.py
│   ├── evidence.py
│   ├── lexer.py
│   ├── parser.py
│   ├── reporter.py
│   ├── runtime.py
│   └── server.py
├── tests/
│   └── test_engine.py
├── .gitignore
├── run.py
└── run.bat
```

*The exact contents may evolve as the project develops.*

## Requirements

- Python 3
- `pip`
- Windows or Linux
- `psutil` for live process and network telemetry where supported

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Chaitanya-gang/JOCKY-Network-Forensics.git
cd JOCKY-Network-Forensics
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the telemetry dependency

```bash
python -m pip install psutil
```

If a dependency manifest is added to the repository, install dependencies from that file instead.

## Run the Prototype

Run the default entry point:

```bash
python run.py
```

Run an investigation script:

```bash
python -m jocky run investigation/case.jky
```

Run the ransomware triage script:

```bash
python -m jocky run investigation/ransomware_hunt.jky
```

Run the multi-host prototype workflow:

```bash
python -m jocky multi investigation/fleet_sweep.jky
```

Start the local web interface:

```bash
python -m jocky web --port 8000
```

Then open `http://localhost:8000` in your browser.

> CLI options may change during development. Use the current command help or the `run.bat` menu if a command differs in your checkout.

## Verify Evidence

Example:

```bash
python -m jocky verify investigation/reports/INCIDENT_001_report.json
```

Use a report generated by your current run if the example report is not present. Verification checks the digest represented in the report; it is not a substitute for independent acquisition validation, trusted timestamps, digital signatures, or a complete chain-of-custody process.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Current Scope and Limitations

JOCKY is a **hackathon/research prototype**, not a production-grade forensic suite. The current scope is centered on a custom interpreted DSL, local host telemetry, evidence hashing, reporting, and a controlled multi-host demonstration.

Do not assume the prototype provides the following unless separately implemented and validated:

- guaranteed evasion of antivirus, EDR, or other security controls
- remote execution on real endpoints
- packet capture or full network traffic analysis
- definitive malware detection from file names or extensions
- offline disk-image analysis or memory forensics
- native compilation of JOCKY scripts
- blockchain-backed evidence storage
- legally certified chain of custody or standards compliance

Use the framework only on systems and evidence you are authorized to examine. Live process and network inspection may require elevated permissions and may vary by operating system.

## Roadmap

Potential future work includes:

- richer DSL diagnostics and language features
- additional OS-specific forensic collectors
- improved evidence provenance and signed manifests
- timeline reconstruction and event-log analysis
- offline disk-image analysis
- secure remote endpoint orchestration
- stronger automated tests and packaging
- optional immutable audit-log integrations

These are development directions, not claims that the features are already available.

## Team

**SafeSecure Forensics**  
Smart India Hackathon 2026 · Problem Statement 26148

---

**JOCKY aims to make forensic workflows easier to express, repeat, inspect, and verify.**
