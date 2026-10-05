/**
 * JOCKY Forensic Studio - Client Application Controller
 */

// State
let scenarios = {};
let currentScenario = "case";
let evidenceItems = [];
let lastExecutionRecord = null;
let lastReportHtml = "";

// DOM Elements
const codeEditor = document.getElementById("codeEditor");
const lineNumbers = document.getElementById("lineNumbers");
const scenarioSelect = document.getElementById("scenarioSelect");
const hostSelect = document.getElementById("hostSelect");
const currentFilename = document.getElementById("currentFilename");
const btnRun = document.getElementById("btnRun");
const btnMultiRun = document.getElementById("btnMultiRun");
const btnRunFleetDirect = document.getElementById("btnRunFleetDirect");
const btnResetCode = document.getElementById("btnResetCode");
const btnClearLogs = document.getElementById("btnClearLogs");
const terminalLog = document.getElementById("terminalLog");
const evidenceFileList = document.getElementById("evidenceFileList");
const evidenceFileCount = document.getElementById("evidenceFileCount");
const evidenceTableBody = document.getElementById("evidenceTableBody");
const tabItemCount = document.getElementById("tabItemCount");
const recordContainer = document.getElementById("recordContainer");
const fleetCards = document.getElementById("fleetCards");
const reportFrame = document.getElementById("reportFrame");
const downloadHtmlBtn = document.getElementById("downloadHtmlBtn");
const downloadJsonBtn = document.getElementById("downloadJsonBtn");
const btnOpenNewTab = document.getElementById("btnOpenNewTab");
const evidenceFilter = document.getElementById("evidenceFilter");

// Pipeline Nodes
const pipelineNodes = [
    "node-script",
    "node-lexer",
    "node-parser",
    "node-policy",
    "node-exec",
    "node-vault",
    "node-hash",
    "node-report"
];

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    initLineNumbers();
    initTabs();
    initFilters();
    loadScenarios();
    loadEvidenceFiles();
    bindEvents();
});

// Line Numbers Sync
function initLineNumbers() {
    function updateLines() {
        const lines = codeEditor.value.split("\n").length;
        lineNumbers.innerHTML = Array.from({ length: lines }, (_, i) => i + 1).join("<br>");
    }
    codeEditor.addEventListener("input", updateLines);
    codeEditor.addEventListener("scroll", () => {
        lineNumbers.scrollTop = codeEditor.scrollTop;
    });
    updateLines();
}

// Tab Switching
function initTabs() {
    document.querySelectorAll(".i-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".i-tab").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

            tab.classList.add("active");
            const targetId = `tab-${tab.dataset.tab}`;
            const pane = document.getElementById(targetId);
            if (pane) pane.classList.add("active");
        });
    });
}

function selectTab(tabName) {
    const tabBtn = document.querySelector(`.i-tab[data-tab="${tabName}"]`);
    if (tabBtn) tabBtn.click();
}

// Evidence Filter Tabs
function initFilters() {
    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderEvidenceTable();
        });
    });

    evidenceFilter.addEventListener("input", () => {
        renderEvidenceTable();
    });
}

// Load Scenarios
async function loadScenarios() {
    try {
        const res = await fetch("/api/scenarios");
        const data = await res.json();
        scenarios = {};
        data.scenarios.forEach(s => {
            scenarios[s.id] = s;
        });

        // Set initial code
        if (scenarios["case"]) {
            codeEditor.value = scenarios["case"].code;
            currentFilename.textContent = scenarios["case"].filename;
            const event = new Event("input");
            codeEditor.dispatchEvent(event);
        }
    } catch (err) {
        logTerminal(`Warning: Could not fetch remote scenarios. Using embedded preset.`, "warn");
        // Fallback default code
        codeEditor.value = `CASE "INCIDENT_001"\n\nprocesses = host.processes()\nfiles = host.files.search("./investigation/evidence")\nconnections = host.network.connections()\n\nevidence.add(processes)\nevidence.add(files)\nevidence.add(connections)\nevidence.hash()\n\nreport.generate()`;
        const event = new Event("input");
        codeEditor.dispatchEvent(event);
    }
}

// Load Evidence Directory Files
async function loadEvidenceFiles() {
    try {
        const res = await fetch("/api/evidence-files");
        const data = await res.json();
        if (data.files && data.files.length > 0) {
            evidenceFileCount.textContent = `${data.files.length} items`;
            evidenceFileList.innerHTML = data.files.map(f => {
                const isSusp = f.name.endsWith(".exe") || f.name.endsWith(".ps1") || f.name.includes("ransom");
                return `
                    <div class="file-chip ${isSusp ? 'suspicious' : ''}">
                        <span>${isSusp ? '⚠️' : '📄'}</span>
                        <span style="flex:1; overflow:hidden; text-overflow:ellipsis;">${f.name}</span>
                        <span style="color:var(--text-dim); font-size:10px;">${(f.size / 1024).toFixed(1)}K</span>
                    </div>
                `;
            }).join("");
        }
    } catch (e) {
        console.error("Could not load evidence directory preview", e);
    }
}

// Event Bindings
function bindEvents() {
    scenarioSelect.addEventListener("change", (e) => {
        currentScenario = e.target.value;
        if (scenarios[currentScenario]) {
            codeEditor.value = scenarios[currentScenario].code;
            currentFilename.textContent = scenarios[currentScenario].filename;
            const event = new Event("input");
            codeEditor.dispatchEvent(event);
            logTerminal(`> Switched scenario to: ${scenarios[currentScenario].title}`, "highlight");
        }
    });

    btnResetCode.addEventListener("click", () => {
        if (scenarios[currentScenario]) {
            codeEditor.value = scenarios[currentScenario].code;
            const event = new Event("input");
            codeEditor.dispatchEvent(event);
            logTerminal(`> Code reset to preset default.`, "info");
        }
    });

    btnClearLogs.addEventListener("click", () => {
        terminalLog.innerHTML = `<div class="term-line info">> Console cleared. Ready.</div>`;
    });

    btnRun.addEventListener("click", executeScript);
    btnMultiRun.addEventListener("click", executeFleetSweep);
    btnRunFleetDirect.addEventListener("click", executeFleetSweep);

    btnOpenNewTab.addEventListener("click", () => {
        if (lastReportHtml) {
            const blob = new Blob([lastReportHtml], { type: "text/html" });
            const url = URL.createObjectURL(blob);
            window.open(url, "_blank");
        }
    });
}

// Log to Terminal
function logTerminal(message, type = "info") {
    const line = document.createElement("div");
    line.className = `term-line ${type}`;
    line.textContent = message;
    terminalLog.appendChild(line);
    terminalLog.scrollTop = terminalLog.scrollHeight;
}

// Reset & Animate Pipeline Nodes
function resetPipeline() {
    pipelineNodes.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.className = "p-node";
        }
    });
}

async function animatePipelineStep(nodeId, delayMs = 120) {
    const el = document.getElementById(nodeId);
    if (el) {
        el.classList.add("active");
        await new Promise(r => setTimeout(r, delayMs));
        el.classList.remove("active");
        el.classList.add("done");
    }
}

// Execute JOCKY Script
async function executeScript() {
    const code = codeEditor.value.trim();
    const host = hostSelect.value;

    if (!code) {
        logTerminal("Error: Script editor is empty.", "error");
        return;
    }

    btnRun.disabled = true;
    btnRun.innerHTML = `<span class="btn-icon">⏳</span><span>EXECUTING...</span>`;
    selectTab("console");

    resetPipeline();
    logTerminal(`\n======================================================`, "highlight");
    logTerminal(`🚀 [${new Date().toLocaleTimeString()}] DISPATCHING JOCKY RUN TO [${host}]...`, "highlight");
    logTerminal(`======================================================`, "highlight");

    await animatePipelineStep("node-script", 100);
    await animatePipelineStep("node-lexer", 150);
    await animatePipelineStep("node-parser", 150);
    await animatePipelineStep("node-policy", 150);

    try {
        const startTime = performance.now();
        const response = await fetch("/api/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, host })
        });

        const result = await response.json();
        const duration = (performance.now() - startTime).toFixed(1);

        if (!result.success) {
            logTerminal(`✗ Execution Error: ${result.error}`, "error");
            btnRun.disabled = false;
            btnRun.innerHTML = `<span class="btn-icon">▶</span><span>RUN JOCKY</span>`;
            return;
        }

        // Stream Runtime Logs
        if (result.logs) {
            result.logs.forEach(log => {
                if (log.includes("✓") || log.includes("✨")) {
                    logTerminal(log, "success");
                } else if (log.includes("⚡") || log.includes("📁")) {
                    logTerminal(log, "highlight");
                } else {
                    logTerminal(log, "info");
                }
            });
        }

        await animatePipelineStep("node-exec", 150);
        await animatePipelineStep("node-vault", 150);
        await animatePipelineStep("node-hash", 150);
        await animatePipelineStep("node-report", 150);

        // Store state
        evidenceItems = result.evidence_items || [];
        lastExecutionRecord = result.execution_record;
        lastReportHtml = result.report_html || "";

        // Update UI
        tabItemCount.textContent = result.evidence_count;
        renderEvidenceTable();
        renderExecutionRecord(result.execution_record);
        renderReportPreview(result.report_html);

        logTerminal(`\n✔ Execution completed in ${duration}ms. Status: ${result.execution_record.status}`, "success");
        logTerminal(`✔ Evidence Hash: ${result.evidence_hash}`, "highlight");

    } catch (err) {
        logTerminal(`✗ Network / Server Error: ${err.message}`, "error");
    } finally {
        btnRun.disabled = false;
        btnRun.innerHTML = `<span class="btn-icon">▶</span><span>RUN JOCKY</span>`;
    }
}

// Multi-Host Fleet Sweep
async function executeFleetSweep() {
    const code = codeEditor.value.trim();
    if (!code) {
        logTerminal("Error: Script editor is empty.", "error");
        return;
    }

    btnMultiRun.disabled = true;
    btnMultiRun.innerHTML = `<span class="btn-icon">⏳</span><span>SWEEPING...</span>`;
    selectTab("fleet");

    logTerminal(`\n======================================================`, "highlight");
    logTerminal(`🌐 ORCHESTRATING DISTRIBUTED FLEET SWEEP (3 ENDPOINTS)...`, "highlight");
    logTerminal(`======================================================`, "highlight");

    try {
        const response = await fetch("/api/multi-run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                code,
                hosts: ["LAB-WIN-01", "LAB-WIN-02", "PROD-UBUNTU-01"]
            })
        });

        const data = await response.json();
        if (data.success && data.cluster) {
            renderFleetCards(data.cluster.nodes);
            logTerminal(`✔ Fleet execution matrix synchronized across all 3 nodes.`, "success");
        } else {
            logTerminal(`✗ Multi-run failed: ${data.error}`, "error");
        }
    } catch (e) {
        logTerminal(`✗ Fleet error: ${e.message}`, "error");
    } finally {
        btnMultiRun.disabled = false;
        btnMultiRun.innerHTML = `<span class="btn-icon">🌐</span><span>FLEET SWEEP</span>`;
    }
}

// Render Evidence Table with filtering
function renderEvidenceTable() {
    const activeFilterBtn = document.querySelector(".filter-btn.active");
    const categoryFilter = activeFilterBtn ? activeFilterBtn.dataset.filter : "all";
    const textQuery = evidenceFilter.value.toLowerCase().trim();

    const filtered = evidenceItems.filter(item => {
        if (categoryFilter !== "all" && item.category !== categoryFilter) {
            return false;
        }
        if (textQuery) {
            const str = JSON.stringify(item).toLowerCase();
            return str.includes(textQuery);
        }
        return true;
    });

    if (filtered.length === 0) {
        evidenceTableBody.innerHTML = `<tr><td colspan="5" class="empty-state">No matching evidence items found.</td></tr>`;
        return;
    }

    evidenceTableBody.innerHTML = filtered.map(item => {
        const d = item.data || {};
        let detailsHtml = "";

        if (item.category === "file") {
            detailsHtml = `<strong>${d.name || ''}</strong> (${(d.size_bytes || 0)} B)`;
            if (d.is_suspicious) {
                detailsHtml += ` <span style="background:rgba(255,51,102,0.2); color:var(--red); padding:1px 4px; border-radius:3px; font-size:10px;">SUSPICIOUS</span>`;
            }
        } else if (item.category === "process") {
            detailsHtml = `<strong>${d.name || ''}</strong> [PID ${d.pid || '?'}] (${d.memory_mb || 0} MB)`;
        } else if (item.category === "network_connection") {
            detailsHtml = `${d.protocol || 'TCP'} ${d.local_address || ''} -> ${d.remote_address || '*'} [${d.status || ''}]`;
        } else {
            detailsHtml = JSON.stringify(d);
        }

        const digest = d.sha256 || item.item_hash || '';
        const shortHash = digest ? `${digest.substring(0, 10)}...${digest.substring(digest.length - 6)}` : 'N/A';

        return `
            <tr>
                <td><strong>${item.item_id}</strong></td>
                <td><span style="color:var(--cyan); text-transform:uppercase;">${item.category}</span></td>
                <td>${detailsHtml}</td>
                <td><span class="hash-pill" title="${digest}">${shortHash}</span></td>
                <td style="color:var(--text-dim); font-size:11px;">${item.timestamp ? item.timestamp.split("T")[1].substring(0, 8) : ''}</td>
            </tr>
        `;
    }).join("");
}

// Render Execution Record
function renderExecutionRecord(record) {
    if (!record) return;

    recordContainer.innerHTML = `
        <div class="cert-card">
            <div class="cert-header">
                <div>
                    <div class="cert-title">JOCKY EVIDENCE EXECUTION RECORD</div>
                    <div style="font-size:11px; color:var(--text-dim); font-family:var(--font-mono); margin-top:3px;">
                        CRYPTOGRAPHIC PROVENANCE & CHAIN OF CUSTODY
                    </div>
                </div>
                <div class="cert-stamp">✓ ${record.status}</div>
            </div>

            <div class="cert-grid">
                <div class="cert-row">
                    <span class="cert-key">Case Identifier:</span>
                    <span class="cert-val" style="color:var(--cyan);">${record.case_id}</span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">Execution ID:</span>
                    <span class="cert-val">${record.execution_id}</span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">Host Target:</span>
                    <span class="cert-val">${record.host}</span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">OS Platform:</span>
                    <span class="cert-val">${record.platform}</span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">Timestamp (UTC):</span>
                    <span class="cert-val">${record.timestamp_iso || record.timestamp}</span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">Evidence Items:</span>
                    <span class="cert-val">${record.total_items} items tracked</span>
                </div>
                <div class="cert-row" style="border-top:1px solid rgba(0,240,255,0.2); padding-top:12px;">
                    <span class="cert-key">Script Hash (SHA-256):</span>
                    <span class="cert-val"><span class="hash-pill">${record.script_hash}</span></span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">Evidence Root SHA-256:</span>
                    <span class="cert-val"><span class="hash-pill" style="color:var(--green); border-color:var(--green);">${record.evidence_hash}</span></span>
                </div>
                <div class="cert-row">
                    <span class="cert-key">Integrity Layer:</span>
                    <span class="cert-val" style="color:var(--cyan);">Phase 1 (Cryptographic Hash Seal)</span>
                </div>
            </div>
        </div>
    `;
}

// Render Fleet Sweep Matrix
function renderFleetCards(nodes) {
    if (!nodes || nodes.length === 0) return;

    fleetCards.innerHTML = nodes.map(n => {
        const shortHash = `${n.evidence_hash.substring(0, 10)}...${n.evidence_hash.substring(n.evidence_hash.length - 6)}`;
        return `
            <div class="fleet-node-card">
                <div><strong style="color:var(--text-primary); font-size:13px;">${n.host}</strong></div>
                <div style="color:var(--text-secondary);">${n.os_type}</div>
                <div><span style="color:var(--green); background:rgba(0,255,157,0.1); padding:2px 6px; border-radius:3px; font-weight:bold;">[${n.status}]</span></div>
                <div><span style="color:var(--cyan); font-weight:bold;">${n.findings_count} items</span></div>
                <div><span class="hash-pill" title="${n.evidence_hash}">${shortHash}</span></div>
            </div>
        `;
    }).join("");
}

// Render HTML Report Preview
function renderReportPreview(htmlContent) {
    if (!htmlContent) return;

    const blob = new Blob([htmlContent], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    reportFrame.src = url;

    downloadHtmlBtn.href = url;
    downloadHtmlBtn.download = `${lastExecutionRecord ? lastExecutionRecord.case_id : 'investigation'}_report.html`;

    if (lastExecutionRecord) {
        const jsonBlob = new Blob([JSON.stringify({
            execution_record: lastExecutionRecord,
            evidence_items: evidenceItems
        }, null, 2)], { type: "application/json" });
        downloadJsonBtn.href = URL.createObjectURL(jsonBlob);
        downloadJsonBtn.download = `${lastExecutionRecord.case_id}_evidence.json`;
    }
}
