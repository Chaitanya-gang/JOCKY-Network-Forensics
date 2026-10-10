<<<<<<< HEAD
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
=======
# JOCKY — Next-Gen Forensic Analysis Language & Controlled Investigation Framework

> **Investigate. Correlate. Verify. Without Compromising Evidence.**

JOCKY is a domain-specific forensic scripting language and investigation framework designed to make repeatable computer and network forensic workflows easier to write, execute, audit, and verify.

It provides a high-level forensic DSL (`.jky`) over a Python runtime, with built-in modules for **process enumeration, file discovery and hashing, network connection inspection, evidence collection, cryptographic integrity verification, report generation, and multi-host investigation orchestration**.

---

## 🎯 Smart India Hackathon 2026

| | Details |
|---|---|
| **Problem Statement ID** | 26148 |
| **Problem Statement** | Creation of Scripts/Functions with New Programming Language to Commence Computer & Network Forensic Analysis Without Triggering Security Solutions |
| **Theme** | Blockchain & Cybersecurity |
| **Category** | Software |
| **Organization** | National Technical Research Organisation (NTRO) |
| **Project** | JOCKY |
| **Team ID** | 53476 |
| **Team Name** | SafeSecure Forensics |
| **Prototype** | JOCKY v0.1 |

---

## 🔎 Problem

Digital forensic investigations often involve several disconnected tools and ad-hoc scripts. This can make investigations:

- difficult to reproduce consistently
- dependent on platform-specific commands and tooling
- time-consuming to orchestrate across multiple endpoints
- harder to audit and verify
- vulnerable to inconsistent evidence-handling workflows

JOCKY addresses this by providing a **forensic-focused scripting layer** where an investigator can describe an investigation once and let the framework handle collection, evidence packaging, hashing, and reporting.

---

## 💡 Proposed Solution

JOCKY introduces a purpose-built forensic DSL with a simple syntax such as:
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

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

<<<<<<< HEAD
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
=======
The prototype translates this high-level investigation logic through:

```text
JOCKY Script (.jky)
        │
        ▼
      Lexer
        │
        ▼
     Parser
        │
        ▼
       AST
        │
        ▼
     Runtime
        │
        ├── Process Forensics
        ├── File Forensics
        └── Network Forensics
        │
        ▼
   Evidence Vault
        │
        ▼
   SHA-256 Integrity Seal
        │
        ▼
 JSON + HTML Reports
```

---

## ✨ Key Features

### 1. Forensic Domain-Specific Language

JOCKY provides a dedicated `.jky` syntax with support for:

- `CASE` declarations
- variable assignments
- method/member access
- function calls
- `FOR` loops
- `IF / ELSE`
- comparisons
- `ECHO / PRINT`
- comments
- strings, numbers, and booleans

This makes forensic workflows more readable and reusable than large collections of low-level commands.

---

### 2. Process Forensics

The process module can collect telemetry including:

- PID
- process name
- executable path
- username
- memory usage
- CPU usage
- process status
- command line
- parent PID
- executable SHA-256 when requested

The implementation uses `psutil` when available and provides a fallback dataset for prototype/demo environments.

---

### 3. File Forensics

JOCKY can recursively search evidence directories and inspect files for:

- filename
- absolute path
- extension
- size
- creation/modification timestamps
- SHA-256
- MD5
- suspicious executable/script extensions

Example:

```jocky
files = host.files.search("./investigation/evidence")
```

Files can then be explicitly hashed:

```jocky
FOR file IN files {
    file.hash("SHA256")
}
```

---

### 4. Network Forensics

The network module inspects active Internet connections and sockets, including:

- protocol
- local address
- remote address
- connection state
- PID
- associated process name

Example:

```jocky
connections = host.network.connections()
```

When `psutil` telemetry is unavailable, the prototype uses a controlled fallback baseline so demonstrations can still run.

---

### 5. Cryptographic Evidence Integrity

Every evidence item receives a SHA-256 digest based on canonicalized evidence metadata and data.

The Evidence Vault then creates a deterministic package-level SHA-256 digest from:

```text
Evidence Item Hashes
        +
Case ID
        +
Host Name
        ↓
Root Evidence SHA-256
```

Reports contain an execution record with:

- Case ID
- Execution ID
- Host
- Platform
- Script SHA-256
- Evidence Root SHA-256
- Evidence count
- Timestamp
- Integrity status

The `verify` command recomputes the evidence digest and reports whether the stored package matches.

---

### 6. Multi-Host Investigation Engine

JOCKY includes a cluster execution layer for running the same investigation logic across multiple named endpoints.

Example:

```bash
python -m jocky multi investigation/fleet_sweep.jky
```

Custom hosts can be supplied:

```bash
python -m jocky multi investigation/fleet_sweep.jky --hosts NODE-A,NODE-B,NODE-C
```

The prototype produces per-node execution information including:

- host
- OS profile
- status
- findings count
- evidence hash
- execution ID
- execution duration

> **Prototype note:** the current multi-host engine is a controlled simulation layer. It executes the investigation runtime locally for each named node and applies predefined endpoint profiles/variance rather than performing remote endpoint execution.

---

### 7. Web Forensic Studio

JOCKY includes a browser-based forensic studio for interacting with the investigation engine.

Start it with:

```bash
python -m jocky web --port 8000
```

Then open:

```text
http://localhost:8000
```

The web interface exposes investigation functionality and generated forensic reports through a local HTTP server.

---

### 8. Automated Reports

The framework generates machine-readable and human-readable forensic reports:

```text
JSON
HTML
```

Example reports included in the prototype:

```text
investigation/reports/
├── INCIDENT_001_report.html
├── INCIDENT_001_report.json
├── RANSOMWARE_TRIAGE_042_report.html
├── RANSOMWARE_TRIAGE_042_report.json
├── DISTRIBUTED_PERSISTENCE_SWEEP_report.html
└── DISTRIBUTED_PERSISTENCE_SWEEP_report.json
```

---

# 🧪 Included Investigation Scripts

## 1. Core Incident Triage

```text
investigation/case.jky
```

Performs:

1. process enumeration
2. evidence file discovery
3. network socket inspection
4. evidence ingestion
5. SHA-256 evidence sealing
6. report generation

Run:

```bash
python -m jocky run investigation/case.jky
```

---

## 2. Ransomware Rapid Triage

```text
investigation/ransomware_hunt.jky
```

Performs:

- evidence file discovery
- SHA-256 hashing
- network connection inspection
- evidence sealing
- report generation

Run:

```bash
python -m jocky run investigation/ransomware_hunt.jky
```

---

## 3. Distributed Persistence Sweep

```text
investigation/fleet_sweep.jky
```

Performs:

- process enumeration
- evidence discovery
- evidence sealing
- multi-host execution support

Run:

```bash
python -m jocky multi investigation/fleet_sweep.jky
```

---

# 🔐 Evidence Verification

A generated JSON report can be cryptographically verified using:

```bash
python -m jocky verify investigation/reports/INCIDENT_001_report.json
```

The verifier:

1. reads the recorded evidence items
2. recomputes each evidence-item SHA-256
3. reconstructs the package hash
4. compares it with the recorded root hash
5. reports either:

```text
[✓ VERIFIED] Evidence integrity intact.
```

or:

```text
[✗ TAMPERED] Hash mismatch!
```

This provides a simple tamper-evidence mechanism for the prototype's generated investigation packages.

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Forensic DSL | Custom `.jky` language |
| Lexer | Custom Python lexer |
| Parser | Custom AST-based parser |
| Runtime | Python |
| Process Telemetry | psutil |
| Network Telemetry | psutil / socket information |
| File Analysis | Python filesystem APIs |
| Cryptographic Integrity | SHA-256 |
| Evidence Format | JSON |
| Reports | JSON + HTML |
| Web Studio | Python HTTP server + HTML/CSS/JavaScript |
| Testing | Python `unittest` |

---

# 📁 Project Structure

```text
JOCKY-Network-Forensics/
│
├── investigation/
│   ├── evidence/
│   │   ├── notes.txt
│   │   ├── ransom_note.txt
│   │   ├── beacon_script.ps1
│   │   └── ...
│   │
│   ├── reports/
│   │   ├── INCIDENT_001_report.html
│   │   ├── INCIDENT_001_report.json
│   │   └── ...
│   │
│   ├── case.jky
│   ├── ransomware_hunt.jky
│   └── fleet_sweep.jky
│
├── jocky/
│   ├── modules/
│   │   ├── file_module.py
│   │   ├── network_module.py
│   │   └── process_module.py
│   │
│   ├── web/
│   │   ├── app.js
│   │   ├── index.html
│   │   └── styles.css
│   │
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f
│   ├── cli.py
│   ├── cluster.py
│   ├── evidence.py
│   ├── lexer.py
│   ├── parser.py
│   ├── reporter.py
│   ├── runtime.py
│   └── server.py
<<<<<<< HEAD
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
=======
│
├── tests/
│   └── test_engine.py
│
├── presentation.html
├── JOCKY_PPT1.pdf
├── SIH_2026_JOCKY_PRESENTATION.md
├── run.py
├── run.bat
└── .gitignore
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.10+
- Windows or Linux
- `pip`

Python 3.13 was used during prototype development.

---

## 1. Clone the repository
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
git clone https://github.com/Chaitanya-gang/JOCKY-Network-Forensics.git
cd JOCKY-Network-Forensics
```

<<<<<<< HEAD
### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux**
=======
---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Ubuntu
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
python3 -m venv .venv
source .venv/bin/activate
```

<<<<<<< HEAD
### 3. Install the telemetry dependency

```bash
python -m pip install psutil
```

If a dependency manifest is added to the repository, install dependencies from that file instead.

## Run the Prototype

Run the default entry point:
=======
---

## 3. Install optional live telemetry dependency

```bash
pip install psutil
```

`psutil` enables live process and network telemetry. The prototype contains fallback behavior for environments where it is unavailable.

---

# ▶️ Running JOCKY

### Default investigation
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
python run.py
```

<<<<<<< HEAD
Run an investigation script:
=======
With no arguments, `run.py` defaults to:
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
python -m jocky run investigation/case.jky
```

<<<<<<< HEAD
Run the ransomware triage script:

```bash
python -m jocky run investigation/ransomware_hunt.jky
```

Run the multi-host prototype workflow:

```bash
python -m jocky multi investigation/fleet_sweep.jky
```

Start the local web interface:
=======
### Run a specific investigation

```bash
python -m jocky run investigation/case.jky
```

### Start Web Forensic Studio
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
python -m jocky web --port 8000
```

<<<<<<< HEAD
Then open `http://localhost:8000` in your browser.

> CLI options may change during development. Use the current command help or the `run.bat` menu if a command differs in your checkout.

## Verify Evidence

Example:
=======
Open:

```text
http://localhost:8000
```

### Multi-host investigation

```bash
python -m jocky multi investigation/fleet_sweep.jky
```

### Verify evidence
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
python -m jocky verify investigation/reports/INCIDENT_001_report.json
```

<<<<<<< HEAD
Use a report generated by your current run if the example report is not present. Verification checks the digest represented in the report; it is not a substitute for independent acquisition validation, trusted timestamps, digital signatures, or a complete chain-of-custody process.

## Run Tests
=======
---

# 🧪 Testing

JOCKY includes a test suite covering:

- lexer tokenization
- parser / AST generation
- runtime execution
- evidence hashing determinism
- multi-host execution

Run:
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f

```bash
python -m unittest discover -s tests -v
```

<<<<<<< HEAD
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
=======
---

# 🧠 JOCKY Execution Model

The prototype follows this investigation lifecycle:

```text
        ┌────────────────────┐
        │ Investigator       │
        │ writes .jky script │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Lexer              │
        │ Tokenization       │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Parser             │
        │ AST Generation     │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Runtime            │
        │ Execute Forensics  │
        └─────────┬──────────┘
                  │
          ┌───────┼────────┐
          ▼       ▼        ▼
       Process   Files   Network
       Module   Module    Module
          │       │        │
          └───────┼────────┘
                  ▼
        ┌────────────────────┐
        │ Evidence Vault     │
        │ Item SHA-256       │
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ Package SHA-256    │
        │ Integrity Seal     │
        └─────────┬──────────┘
                  ▼
        ┌────────────────────┐
        │ HTML / JSON Report │
        └────────────────────┘
```

---

# 📊 Prototype Modes

| Mode | Purpose | Current Prototype Status |
|---|---|---|
| **Online / Live** | Inspect processes, files and network connections on the current host | Implemented |
| **Multi-Host** | Execute investigation logic for multiple named endpoints | Implemented as controlled prototype simulation |
| **Offline / Disk Image** | Post-mortem disk image analysis | Planned / Future Scope |

---

# 🔭 Roadmap

### Phase 1 — JOCKY v0.1
- [x] Custom forensic DSL
- [x] Lexer
- [x] AST parser
- [x] Runtime execution engine
- [x] Process telemetry
- [x] File discovery and hashing
- [x] Network connection inspection
- [x] Evidence Vault
- [x] SHA-256 integrity verification
- [x] JSON/HTML reporting
- [x] Web Forensic Studio
- [x] Multi-host prototype engine
- [x] Automated test suite

### Phase 2 — Advanced Runtime
- [ ] Native compiler/backend
- [ ] richer policy enforcement
- [ ] deeper OS-specific forensic adapters
- [ ] expanded investigation modules

### Phase 3 — Advanced Telemetry
- [ ] Linux eBPF-based telemetry
- [ ] deeper Windows-native telemetry
- [ ] offline disk-image analysis
- [ ] event/log timeline reconstruction

### Phase 4 — Distributed Evidence Infrastructure
- [ ] signed investigation modules
- [ ] immutable audit infrastructure
- [ ] permissioned blockchain-backed evidence ledger
- [ ] enterprise-scale endpoint orchestration

---

# 📚 Standards & Research Direction

The project is designed with established digital-forensics principles in mind, including:

- **NIST SP 800-86** — Guide to Integrating Forensic Techniques into Incident Response
- **ISO/IEC 27037** — Guidelines for identification, collection, acquisition and preservation of digital evidence

These references provide conceptual grounding for evidence handling and forensic workflows; the current prototype should **not** be interpreted as independently guaranteeing legal admissibility or formal standards certification.

---

# 📌 Prototype Scope & Disclaimer

JOCKY v0.1 is a **research / hackathon prototype**.

The current implementation focuses on demonstrating:

- a custom forensic scripting language
- repeatable investigation workflows
- host telemetry collection
- evidence packaging
- SHA-256 integrity verification
- report generation
- controlled multi-host orchestration

Some capabilities shown in the broader roadmap or presentation concept—such as offline disk-image reconstruction, kernel-level eBPF telemetry, native compiler backends, and blockchain-backed immutable ledgers—are **future development targets and are not fully implemented in this prototype**.

Use the framework only on systems and evidence for which you have appropriate authorization.

---


# 👥 Team

**SafeSecure Forensics**  
Smart India Hackathon 2026  
Problem Statement ID: **26148**

---

## ⭐ Vision

> **Turn forensic investigation into a repeatable, verifiable program.**

JOCKY aims to provide investigators with a higher-level way to express forensic intent while keeping evidence collection, integrity verification, and investigation reporting as first-class parts of the workflow.
>>>>>>> 8a3acf67b823fca3116f5f64522b7a2dc272df3f
