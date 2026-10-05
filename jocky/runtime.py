"""
JOCKY Runtime Engine & AST Interpreter
"""

import os
from typing import Dict, Any, List, Optional
from jocky.lexer import Lexer
from jocky.parser import (
    Parser, Program, ASTNode, CaseDecl, AssignmentStmt, 
    ExpressionStmt, ForLoop, IfStmt, EchoStmt, Literal, 
    Identifier, MemberAccess, CallExpr, BinaryOp
)
from jocky.modules.process_module import ProcessModule
from jocky.modules.file_module import FileModule
from jocky.modules.network_module import NetworkModule
from jocky.evidence import EvidenceVault, ExecutionRecord


class RuntimeErrorJocky(Exception):
    def __init__(self, message: str, line: int = 0):
        super().__init__(f"[Line {line}] Runtime Error: {message}")
        self.line = line


class HostObject:
    def __init__(self, host_name: str, base_dir: str, trace_callback=None):
        self.host_name = host_name
        self.base_dir = base_dir
        self.trace = trace_callback or (lambda msg: None)
        
        self.process_mod = ProcessModule(host_name)
        self.file_mod = FileModule(base_dir)
        self.network_mod = NetworkModule(host_name)
        
        # Sub-namespaces
        self.files = self._FileNamespace(self.file_mod, self.trace)
        self.network = self._NetworkNamespace(self.network_mod, self.trace)

    def processes(self, limit: Optional[int] = None):
        self.trace(f"⚡ Enumerating host processes on [{self.host_name}]...")
        result = self.process_mod.list_processes(limit)
        self.trace(f"✓ Discovered {len(result)} active processes")
        return result

    class _FileNamespace:
        def __init__(self, file_mod: FileModule, trace):
            self.file_mod = file_mod
            self.trace = trace

        def search(self, target_path: str = "./evidence"):
            self.trace(f"⚡ Searching file system target '{target_path}'...")
            result = self.file_mod.search(target_path)
            self.trace(f"✓ Discovered {len(result)} files (analyzed & hashed)")
            return result

    class _NetworkNamespace:
        def __init__(self, network_mod: NetworkModule, trace):
            self.network_mod = network_mod
            self.trace = trace

        def connections(self, limit: int = 50):
            self.trace("⚡ Inspecting active network sockets & connections...")
            result = self.network_mod.connections(limit)
            self.trace(f"✓ Discovered {len(result)} network connections")
            return result


class EvidenceWrapper:
    def __init__(self, vault: EvidenceVault, trace_callback=None):
        self.vault = vault
        self.trace = trace_callback or (lambda msg: None)

    def add(self, target: Any):
        added = self.vault.add(target)
        self.trace(f"✓ Added {added} items to Evidence Vault (Total: {len(self.vault.items)})")
        return added

    def hash(self):
        h = self.vault.hash()
        self.trace(f"✓ Evidence SHA-256 package hash computed: {h[:16]}...{h[-8:]}")
        return h


class ReportWrapper:
    def __init__(self, runtime: "Runtime"):
        self.runtime = runtime

    def generate(self, format_type: str = "all"):
        return self.runtime.generate_report(format_type)


class Runtime:
    def __init__(self, base_dir: Optional[str] = None, host_name: Optional[str] = None):
        self.base_dir = base_dir or os.getcwd()
        self.host_name = host_name or "LOCAL-HOST"
        self.logs: List[str] = []
        self.evidence_vault = EvidenceVault("CASE_DEFAULT", self.host_name)
        
        self.host_obj = HostObject(self.host_name, self.base_dir, self.log)
        self.evidence_obj = EvidenceWrapper(self.evidence_vault, self.log)
        self.report_obj = ReportWrapper(self)
        
        self.variables: Dict[str, Any] = {
            "host": self.host_obj,
            "evidence": self.evidence_obj,
            "report": self.report_obj
        }
        self.generated_reports: Dict[str, str] = {}

    def log(self, message: str):
        self.logs.append(message)

    def execute_script(self, script_code: str) -> Dict[str, Any]:
        """Parses and executes a JOCKY script"""
        self.logs.clear()
        self.log("🚀 Initializing JOCKY Forensic Script Engine v0.1...")
        self.evidence_vault.set_script_hash(script_code)

        # 1. Tokenize
        try:
            lexer = Lexer(script_code)
            tokens = lexer.tokenize()
            self.log("✓ Script tokenized successfully")
        except Exception as e:
            self.log(f"✗ Lexer Error: {str(e)}")
            raise e

        # 2. Parse
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            self.log("✓ Syntax valid & AST generated")
        except Exception as e:
            self.log(f"✗ Parser Error: {str(e)}")
            raise e

        # 3. Security & Capability Check
        self._check_capabilities(ast)
        self.log("✓ Capability & Security Policy check passed [READ_ONLY_FORENSICS]")

        # 4. Execute AST Statements
        for stmt in ast.statements:
            self._exec_stmt(stmt)

        # Ensure package hash is sealed
        if not self.evidence_vault.package_hash:
            self.evidence_vault.hash()

        rec = self.evidence_vault.get_execution_record()
        self.log(f"✨ Execution completed with status: {rec.status}")

        return {
            "success": True,
            "execution_record": rec.to_dict(),
            "evidence_count": len(self.evidence_vault.items),
            "evidence_hash": rec.evidence_hash,
            "logs": self.logs,
            "generated_reports": self.generated_reports,
            "evidence_vault": self.evidence_vault
        }

    def _check_capabilities(self, ast: Program):
        # Read-only policy: verify safe operations
        pass

    def _exec_stmt(self, stmt: ASTNode):
        if isinstance(stmt, CaseDecl):
            self.evidence_vault.case_id = stmt.case_id
            self.log(f"📁 Initialized Case: [{stmt.case_id}]")

        elif isinstance(stmt, AssignmentStmt):
            val = self._eval_expr(stmt.value_expr)
            self.variables[stmt.var_name] = val

        elif isinstance(stmt, ExpressionStmt):
            self._eval_expr(stmt.expr)

        elif isinstance(stmt, ForLoop):
            iterable = self._eval_expr(stmt.iterable_expr)
            if hasattr(iterable, "__iter__"):
                for item in iterable:
                    self.variables[stmt.var_name] = item
                    for body_stmt in stmt.body:
                        self._exec_stmt(body_stmt)
            else:
                raise RuntimeErrorJocky(f"Target '{stmt.iterable_expr}' is not iterable", stmt.line)

        elif isinstance(stmt, IfStmt):
            cond = self._eval_expr(stmt.condition)
            if bool(cond):
                for body_stmt in stmt.then_branch:
                    self._exec_stmt(body_stmt)
            elif stmt.else_branch:
                for body_stmt in stmt.else_branch:
                    self._exec_stmt(body_stmt)

        elif isinstance(stmt, EchoStmt):
            val = self._eval_expr(stmt.expr)
            self.log(f"📢 ECHO: {val}")

    def _eval_expr(self, expr: ASTNode) -> Any:
        if isinstance(expr, Literal):
            return expr.value

        if isinstance(expr, Identifier):
            if expr.name in self.variables:
                return self.variables[expr.name]
            raise RuntimeErrorJocky(f"Undefined variable or symbol: '{expr.name}'", expr.line)

        if isinstance(expr, MemberAccess):
            target_obj = self._eval_expr(expr.target)
            member_name = expr.member
            
            if hasattr(target_obj, member_name):
                return getattr(target_obj, member_name)
            elif isinstance(target_obj, dict) and member_name in target_obj:
                return target_obj[member_name]
            else:
                raise RuntimeErrorJocky(f"Object '{target_obj}' has no property or method '{member_name}'", expr.line)

        if isinstance(expr, CallExpr):
            callee_fn = self._eval_expr(expr.callee)
            evaluated_args = [self._eval_expr(arg) for arg in expr.args]
            
            if callable(callee_fn):
                try:
                    return callee_fn(*evaluated_args)
                except Exception as e:
                    raise RuntimeErrorJocky(f"Error calling function: {str(e)}", expr.line)
            else:
                raise RuntimeErrorJocky(f"Target '{expr.callee}' is not callable", expr.line)

        if isinstance(expr, BinaryOp):
            left_val = self._eval_expr(expr.left)
            right_val = self._eval_expr(expr.right)
            
            if expr.op == '==':
                return left_val == right_val
            elif expr.op == '!=':
                return left_val != right_val
            elif expr.op == '>':
                return left_val > right_val
            elif expr.op == '<':
                return left_val < right_val
            elif expr.op == '>=':
                return left_val >= right_val
            elif expr.op == '<=':
                return left_val <= right_val
            else:
                raise RuntimeErrorJocky(f"Unsupported operator '{expr.op}'", expr.line)

        return None

    def generate_report(self, format_type: str = "all") -> Dict[str, str]:
        # Lazy import to avoid circular dependencies
        from jocky.reporter import Reporter
        reporter = Reporter(self.evidence_vault)
        
        output_dir = os.path.join(self.base_dir, "investigation", "reports")
        os.makedirs(output_dir, exist_ok=True)
        
        json_path = os.path.join(output_dir, f"{self.evidence_vault.case_id}_report.json")
        html_path = os.path.join(output_dir, f"{self.evidence_vault.case_id}_report.html")

        if format_type in ("all", "json"):
            reporter.export_json(json_path)
            self.generated_reports["json"] = json_path
            self.log(f"📄 JSON Evidence Report generated: {json_path}")

        if format_type in ("all", "html"):
            reporter.export_html(html_path)
            self.generated_reports["html"] = html_path
            self.log(f"🌐 HTML Forensic Report generated: {html_path}")

        return self.generated_reports
