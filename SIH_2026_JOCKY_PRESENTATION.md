# SMART INDIA HACKATHON 2026 — OFFICIAL PRESENTATION DECK
## Problem Statement ID: 26148
### Project: JOCKY — Next-Gen Forensic Analysis Language & Controlled Investigation Framework
**Theme:** Blockchain & Cybersecurity | **Category:** Software | **Organization:** National Technical Research Organisation (NTRO)  
**Team ID:** 53476 | **Team Name:** SafeSecure Forensics  

---

## 📑 SLIDE 1 — TITLE & IDENTIFICATION

### Slide Header & Identification
- **Event:** SMART INDIA HACKATHON 2026
- **Problem Statement ID:** 26148
- **Problem Statement Title:** Creation of Scripts/Functions with New Programming Language to Commence Computer & Network Forensic Analysis Without Triggering Security Solutions
- **Theme:** Blockchain & Cybersecurity
- **PS Category:** Software
- **Organization:** National Technical Research Organisation (NTRO)

### Project Branding
- **Project Name:** JOCKY (v0.1 Prototype Verified)
- **Subtitle:** Next-Gen Forensic Analysis Language & Controlled Investigation Framework
- **Tagline:** *“Investigate. Correlate. Verify. Without Compromising Evidence.”*

### Team Details
- **Team ID:** 53476
- **Team Name:** SafeSecure Forensics
- **Visual Motif:** Central Cyber-Forensic Core with 4 Orbiting Pillars: *Computer Forensics, Network Telemetry, SHA-256 Audit, Policy Control*.

---

## 📑 SLIDE 2 — PROBLEM + PROPOSED SOLUTION + UVP + ARCHITECTURE

### Section 1: PROBLEM EXISTING (Forensic Analysis is Powerful — But Operationally Difficult)
- **Tool Fragmentation:** Investigators are forced to juggle 10+ disjoint endpoint, OS, disk, and network tools.
- **Security Interference:** Legitimate diagnostic and forensic scripts trigger endpoint security false-positives.
- **Low-Level Complexity:** Deep memory and artifact extraction requires specialized, error-prone OS internals code.
- **Multi-System Challenge:** Investigating distributed fleets lacks synchronized orchestration and uniform telemetry.
- **Evidence Integrity:** Artifacts lack standardized, tamper-evident cryptographic provenance and audit chains.

### Section 2: PROPOSED SOLUTION (JOCKY — Forensic Analysis Language + Framework)
1. **Forensic DSL:** A clean, purpose-built domain-specific language for expressing repeatable forensic logic.
2. **Cross-Platform Runtime:** Native execution across Windows and Ubuntu via a common Intermediate Representation (IR).
3. **Controlled Execution:** Policy layer strictly separates authorized, read-only forensic operations from unsafe actions.
4. **Central Investigation Console:** Broadcast and orchestrate investigations across multiple endpoints simultaneously.
5. **Verifiable Evidence:** Automated per-item and root package SHA-256 hashing bound to verifiable execution certificates.

### Section 3: UVP (UNIQUE VALUE PROPOSITION)
> **“Write Once. Investigate Everywhere.”**
- **One Language → Multiple Platforms:** Unified abstraction over low-level Windows Win32 and Linux system APIs.
- **One Investigation → Multiple Endpoints:** Distributed multi-host sweep capability.
- **One Evidence Pipeline → Verifiable Results:** Deterministic cryptographic chain of custody.
- **The Investigator's Layer:** Bridges the gap between raw, fragile scripting and rigid monolithic tools.

### Section 4: INNOVATION ARCHITECTURE SIDEBAR
- **Investigator Workflow:** `Analyst ➔ Authentication ➔ Authorization ➔ Target System Selection`
- **3 System Modes:** `ONLINE MODE` | `OFFLINE MODE` | `MULTI-HOST MODE`
- **Execution Lifecycle:**
  - JOCKY Script: Parse, Validate & Policy Check
  - Runtime Engine: Live Host Telemetry & Artifact Collection
  - Evidence Vault: SHA-256 Merkle Package Seal
  - Deliverables: Verified JSON/HTML Investigation Package
- **Compliance Badge:** NIST SP 800-86 | ISO/IEC 27037 | RFC 3161

---

## 📑 SLIDE 3 — TECHNICAL APPROACH & EXECUTION

### Decision & Execution Flow
1. **Mode 1: Live Endpoint Forensics**
   - Connect to active endpoint ➔ JOCKY Compiler generates safe IR ➔ Collect Live Telemetry (Processes, Open Sockets, Memory) ➔ Ingest to Evidence Vault ➔ Generate Verified Live Report.
2. **Mode 2: Offline Forensics (Disk Images & Post-Mortem)**
   - Load raw image (E01/RAW) ➔ Read-only mount ➔ Reconstruct Registry, MFT, and Event Log Timelines ➔ Bitstream SHA-256 validation ➔ Offline Case Archive.
3. **Mode 3: Multi-Endpoint Central Fleet Sweep**
   - Central JOCKY Studio Orchestration ➔ Broadcast script to Windows & Ubuntu worker agents ➔ Parallel Execution Matrix ➔ Synchronize Cross-Node Evidence Hashes ➔ Central SOC Dashboard.

### Tech Stack Badges
- **Language Core:** Rust, Tree-sitter AST, LLVM IR, Python 3.13 Runtime
- **Forensic Telemetry:** Windows API, Linux eBPF, psutil, Native Sockets
- **Integrity & Storage:** SHA-256 Merkle Vault, SQLite, JSON Evidence Format
- **Standards:** NIST SP 800-86, ISO/IEC 27037

---

## 📑 SLIDE 4 — FEASIBILITY AND VIABILITY

### Feasibility:
- **Technical Feasibility:** Proven compiler architecture (Lexer + Parser + AST + IR + Runtime) ensures robust, predictable parsing and execution.
- **Cross-Platform:** Windows & Ubuntu runtimes execute identical investigation logic via OS-level abstractions.
- **Compliance:** Built-in ISO/IEC 27037 and NIST SP 800-86 compliance guarantees courtroom-admissible digital evidence.
- **Operational:** Rapid agent deployment without kernel modifications, driver signing risks, or system reboots.

### Viability:
- **National & Defence:** Tailored for NTRO, CERT-In, defence, and law enforcement incident response teams.
- **Enterprise & SOC:** Replaces fragile ad-hoc scripts with standardized, version-controlled investigation playbooks.
- **Scalability:** Proven linear scalability from 1 endpoint ➔ 10 endpoints ➔ 1,000+ enterprise endpoints.
- **Future Scope:** JOCKY Community Marketplace for peer-reviewed, cryptographically signed investigation modules.

### Technical & Operational Risk Mitigation Table:
| Risk Area | Identified Risk | Engineering & Operational Mitigation |
| :--- | :--- | :--- |
| **Technical** | OS API Discrepancies | Modular Hardware Abstraction Layer (HAL) & OS adapters |
| **Technical** | Security Tool False Positives | Policy-validated IR avoids unsafe behavioral heuristics |
| **Technical** | Evidence Tampering | Immediate per-item SHA-256 hashing + append-only Merkle chain |
| **Operational** | Analyst Learning Curve | Intuitive Pythonic DSL syntax + ready-to-use template library |
| **Operational** | Network Congestion | Edge execution: filtering and hashing at endpoint before transmission |
| **Operational** | Endpoint Disconnections | Local offline execution queue with auto-resync upon reconnect |

---

## 📑 SLIDE 5 — HOW JOCKY WORKS, MODES & IMPACTS

### Four Pillars of Impact
1. **🛡️ Security Impact:** Rapid threat identification and controlled acquisition without triggering false alarms.
2. **⚡ Operational Speed:** Reusable JOCKY investigation scripts reduce mean-time-to-triage (MTTR) from hours to minutes.
3. **🔐 Forensic Trust:** Cryptographic SHA-256 binding and execution records guarantee tamper-evident chain of custody.
4. **🌐 National Security:** A sovereign, vendor-neutral cyber forensic programming framework for critical national infrastructure.

### 8-Step Forensic Execution Pipeline
$$\text{Define} \rightarrow \text{Write Script} \rightarrow \text{Compile IR} \rightarrow \text{Validate Policy} \rightarrow \text{Collect} \rightarrow \text{Correlate} \rightarrow \text{Hash \& Seal} \rightarrow \text{Report}$$

### Three Investigation Modes Comparison:
| Mode Specification | Mode 1: ONLINE (Live Endpoint) | Mode 2: OFFLINE (Dead / Image) | Mode 3: MULTI-ENDPOINT (Fleet) |
| :--- | :--- | :--- | :--- |
| **Target** | Active running endpoints | Raw disk images (E01/RAW) | 10 to 1,000+ distributed endpoints |
| **Process** | Connect ➔ Acquire ➔ Analyze | Mount ➔ Extract ➔ Correlate | Push Script ➔ Parallel Exec ➔ Sync |
| **Speed / Time** | < 60 seconds per host | Thorough deep-dive triage | Synchronous parallel sweep |
| **Scope** | Processes, Sockets, Live Memory | MFT, Registry Hives, Event Logs | Cross-node IOC matching |
| **Best For** | Active Incident Response | Post-Mortem Lab Forensics | Enterprise SOC & Lateral Movement |

---

## 📑 SLIDE 6 — RESEARCH, REFERENCES & ROADMAP

### Academic & Standards Grounding
- **NIST SP 800-86 & ISO/IEC 27037:** Foundational digital forensic principles for evidence identification, collection, acquisition, and chain of custody.
- **Compiler Architecture:** LLVM Intermediate Representation and Tree-sitter incremental parsing for predictable, safe execution.
- **DFIR Literature:** Replaces fragmented point-tools with a unified, high-level programmable abstraction layer.

### Existing Solutions vs Our Solution:
| Existing Approaches (Traditional / Scripting) | Our Solution (JOCKY Framework) |
| :--- | :--- |
| Fragmented across 10+ disconnected tools | **Unified Forensic DSL:** Single clean language |
| Fragile, platform-specific OS scripts (C++/PowerShell) | **Cross-Platform IR:** Write once, run on Windows & Ubuntu |
| Manual, separate evidence hashing steps | **Built-in Evidence Vault:** Automated SHA-256 package seal |
| Complex, uncoordinated multi-host sweeps | **Distributed Orchestration:** Centralized fleet management |

### Validation & Working Prototype Assets (JOCKY v0.1)
- **Live Interactive Web Studio:** Accessible locally on `http://localhost:8000`
- **CLI Command Runner:** `python -m jocky run investigation/case.jky`
- **Multi-Host Sweep Engine:** `python -m jocky multi investigation/fleet_sweep.jky`
- **Cryptographic Verifier:** `python -m jocky verify investigation/reports/INCIDENT_001_report.json`

### Future Scope & Roadmap (JOCKY 2.0)
- **Phase 1 (Completed):** JOCKY v0.1 Parser, Host Telemetry & SHA-256 Evidence Vault.
- **Phase 2:** Native Rust Compiler & LLVM bytecode execution backend.
- **Phase 3:** Linux eBPF probes for real-time kernel-level telemetry.
- **Phase 4:** Permissioned blockchain-backed immutable audit ledger.

---

### 🌟 FINAL CLOSING STATEMENT:
> **JOCKY — TURN FORENSIC INVESTIGATION INTO A REPEATABLE, VERIFIABLE PROGRAM.**
