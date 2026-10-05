"""
JOCKY File Forensics Module - Search, Inspection & Cryptographic Hashing
"""

import os
import glob
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional


class FileItem:
    def __init__(self, file_path: str):
        self.path = os.path.abspath(file_path)
        self.name = os.path.basename(file_path)
        self.extension = os.path.splitext(self.name)[1].lower()
        self.size_bytes = 0
        self.created = ""
        self.modified = ""
        self.sha256 = ""
        self.md5 = ""
        self.is_suspicious = False
        
        self._inspect()

    def _inspect(self):
        if os.path.isfile(self.path):
            try:
                stat = os.stat(self.path)
                self.size_bytes = stat.st_size
                self.created = datetime.fromtimestamp(stat.st_ctime).isoformat()
                self.modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                
                # Check suspicious extensions
                if self.extension in ('.exe', '.dll', '.bat', '.ps1', '.vbs', '.js', '.scr', '.elf'):
                    self.is_suspicious = True
                
                # Default hash
                self.hash("SHA256")
            except Exception:
                pass

    def hash(self, algorithm: str = "SHA256") -> str:
        algo = algorithm.upper()
        if not os.path.isfile(self.path):
            return ""

        try:
            if algo == "SHA256":
                hasher = hashlib.sha256()
            elif algo == "MD5":
                hasher = hashlib.md5()
            elif algo == "SHA1":
                hasher = hashlib.sha1()
            else:
                hasher = hashlib.sha256()

            with open(self.path, "rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            
            digest = hasher.hexdigest()
            if algo == "SHA256":
                self.sha256 = digest
            elif algo == "MD5":
                self.md5 = digest
            return digest
        except Exception:
            return ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "file",
            "name": self.name,
            "path": self.path,
            "extension": self.extension,
            "size_bytes": self.size_bytes,
            "created": self.created,
            "modified": self.modified,
            "sha256": self.sha256,
            "md5": self.md5,
            "is_suspicious": self.is_suspicious
        }

    def __repr__(self):
        return f"File('{self.name}', size={self.size_bytes}B, sha256={self.sha256[:8]}...)"


class FileCollection:
    def __init__(self, items: List[FileItem]):
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]

    def hash(self, algorithm: str = "SHA256") -> "FileCollection":
        """Hashes all files in collection"""
        for item in self.items:
            item.hash(algorithm)
        return self

    def filter(self, extension: str = "") -> "FileCollection":
        ext = extension if extension.startswith('.') else f".{extension}"
        filtered = [f for f in self.items if f.extension == ext.lower()]
        return FileCollection(filtered)

    def to_list(self) -> List[Dict[str, Any]]:
        return [f.to_dict() for f in self.items]

    def __repr__(self):
        return f"FileCollection({len(self.items)} files)"


class FileModule:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.getcwd()

    def search(self, target_path: str = "./evidence") -> FileCollection:
        """Searches files in the specified path (relative or absolute)"""
        if not os.path.isabs(target_path):
            resolved_path = os.path.normpath(os.path.join(self.base_dir, target_path))
        else:
            resolved_path = target_path

        results: List[FileItem] = []

        if os.path.isdir(resolved_path):
            for root, _, files in os.walk(resolved_path):
                for f in sorted(files):
                    full_p = os.path.join(root, f)
                    results.append(FileItem(full_p))
        elif os.path.isfile(resolved_path):
            results.append(FileItem(resolved_path))
        else:
            # Try glob pattern
            matched = glob.glob(resolved_path, recursive=True)
            for p in sorted(matched):
                if os.path.isfile(p):
                    results.append(FileItem(p))

        return FileCollection(results)
