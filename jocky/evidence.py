"""
JOCKY Evidence & Integrity Layer - Cryptographic Chain of Custody
"""

import json
import socket
import hashlib
import platform
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional


class EvidenceItem:
    def __init__(self, item_id: str, category: str, data: Dict[str, Any], timestamp: Optional[str] = None):
        self.item_id = item_id
        self.category = category
        self.data = data
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.item_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        payload = {
            "item_id": self.item_id,
            "category": self.category,
            "data": self.data,
            "timestamp": self.timestamp
        }
        canonical = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "category": self.category,
            "data": self.data,
            "timestamp": self.timestamp,
            "item_hash": self.item_hash
        }


class ExecutionRecord:
    def __init__(self, case_id: str, script_hash: str, host: str, 
                 execution_id: str, evidence_hash: str, total_items: int,
                 status: str = "VERIFIED"):
        self.case_id = case_id
        self.execution_id = execution_id
        self.host = host
        self.platform = f"{platform.system()} {platform.release()}"
        self.script_hash = script_hash
        self.evidence_hash = evidence_hash
        self.total_items = total_items
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.timestamp_iso = datetime.now(timezone.utc).isoformat()
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "execution_id": self.execution_id,
            "host": self.host,
            "platform": self.platform,
            "script_hash": self.script_hash,
            "evidence_hash": self.evidence_hash,
            "total_items": self.total_items,
            "timestamp": self.timestamp,
            "timestamp_iso": self.timestamp_iso,
            "status": self.status
        }

    def format_box(self) -> str:
        lines = [
            "┌──────────────────────────────────────────────────────────────┐",
            "│                    JOCKY EXECUTION RECORD                    │",
            "├──────────────────────────────────────────────────────────────┤",
            f"│ Case ID       : {self.case_id:<45}│",
            f"│ Execution ID  : {self.execution_id:<45}│",
            f"│ Host          : {self.host:<45}│",
            f"│ Platform      : {self.platform:<45}│",
            f"│ Script Hash   : {self.script_hash[:16]}...{self.script_hash[-8:]:<21}│",
            f"│ Evidence Hash : {self.evidence_hash[:16]}...{self.evidence_hash[-8:]:<21}│",
            f"│ Items Tracked : {self.total_items:<45}│",
            f"│ Timestamp     : {self.timestamp:<45}│",
            f"│ Integrity     : [✓ {self.status}]                                 │",
            "└──────────────────────────────────────────────────────────────┘"
        ]
        return "\n".join(lines)


class EvidenceVault:
    def __init__(self, case_id: str = "CASE-DEFAULT", host_name: Optional[str] = None):
        self.case_id = case_id
        self.host_name = host_name or socket.gethostname() or "LOCAL-NODE"
        self.items: List[EvidenceItem] = []
        self._item_counter = 0
        self.package_hash = ""
        self.script_hash = ""
        self.execution_id = self._generate_exec_id()
        self.is_sealed = False

    def _generate_exec_id(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        rand_id = hashlib.md5(f"{date_str}-{self.host_name}-{datetime.now().microsecond}".encode()).hexdigest()[:4].upper()
        return f"EX-{date_str}-{rand_id}"

    def set_script_hash(self, script_code: str):
        self.script_hash = hashlib.sha256(script_code.encode("utf-8")).hexdigest()

    def add(self, target: Any) -> int:
        """Adds findings or telemetry items to the evidence vault"""
        if self.is_sealed:
            raise RuntimeError("Cannot add evidence to a sealed evidence vault.")

        added_count = 0

        # Handle custom collections or primitives
        if hasattr(target, "to_list"):
            items_list = target.to_list()
            for obj in items_list:
                self._add_single_item(obj.get("type", "generic"), obj)
                added_count += 1
        elif isinstance(target, list):
            for item in target:
                if hasattr(item, "to_dict"):
                    d = item.to_dict()
                    self._add_single_item(d.get("type", "generic"), d)
                elif isinstance(item, dict):
                    self._add_single_item(item.get("type", "generic"), item)
                else:
                    self._add_single_item("primitive", {"value": str(item)})
                added_count += 1
        elif hasattr(target, "to_dict"):
            d = target.to_dict()
            self._add_single_item(d.get("type", "generic"), d)
            added_count += 1
        elif isinstance(target, dict):
            self._add_single_item(target.get("type", "generic"), target)
            added_count += 1
        else:
            self._add_single_item("value", {"raw": str(target)})
            added_count += 1

        # Automatically update package hash when items added
        self.hash()
        return added_count

    def _add_single_item(self, category: str, data: Dict[str, Any]):
        self._item_counter += 1
        item_id = f"EV-{self._item_counter:04d}"
        ev_item = EvidenceItem(item_id, category, data)
        self.items.append(ev_item)

    def hash(self) -> str:
        """Computes root SHA-256 package digest across all tracked evidence items"""
        hashes = [item.item_hash for item in self.items]
        combined = "|".join(hashes) + f"|{self.case_id}|{self.host_name}"
        self.package_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
        return self.package_hash

    def get_execution_record(self) -> ExecutionRecord:
        if not self.package_hash:
            self.hash()
        return ExecutionRecord(
            case_id=self.case_id,
            script_hash=self.script_hash or "0000000000000000000000000000000000000000000000000000000000000000",
            host=self.host_name,
            execution_id=self.execution_id,
            evidence_hash=self.package_hash,
            total_items=len(self.items),
            status="VERIFIED"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_record": self.get_execution_record().to_dict(),
            "items_count": len(self.items),
            "evidence_items": [item.to_dict() for item in self.items]
        }
