"""
JOCKY Test Suite - Lexer, Parser, Runtime, Evidence Hashing & Verification
"""

import unittest
import os
import shutil
import json
from jocky.lexer import Lexer, TokenType
from jocky.parser import Parser, CaseDecl, AssignmentStmt, ForLoop
from jocky.runtime import Runtime
from jocky.evidence import EvidenceVault
from jocky.cluster import JockyCluster


class TestJockyEngine(unittest.TestCase):

    def test_lexer_basic(self):
        code = 'CASE "INC_001"\nprocesses = host.processes()\nevidence.add(processes)'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        token_types = [t.type for t in tokens]
        self.assertIn(TokenType.KEYWORD_CASE, token_types)
        self.assertIn(TokenType.STRING, token_types)
        self.assertIn(TokenType.IDENTIFIER, token_types)
        self.assertIn(TokenType.ASSIGN, token_types)
        self.assertIn(TokenType.DOT, token_types)
        self.assertIn(TokenType.LPAREN, token_types)
        self.assertIn(TokenType.RPAREN, token_types)

    def test_parser_ast(self):
        code = '''
        CASE "INCIDENT_001"
        files = host.files.search("./evidence")
        FOR file IN files {
            file.hash("SHA256")
        }
        evidence.add(files)
        evidence.hash()
        report.generate()
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()

        self.assertEqual(len(program.statements), 6)
        self.assertIsInstance(program.statements[0], CaseDecl)
        self.assertEqual(program.statements[0].case_id, "INCIDENT_001")
        self.assertIsInstance(program.statements[1], AssignmentStmt)
        self.assertIsInstance(program.statements[2], ForLoop)

    def test_runtime_execution(self):
        code = '''
        CASE "TEST_CASE"
        files = host.files.search("./investigation/evidence")
        evidence.add(files)
        evidence.hash()
        '''
        runtime = Runtime(base_dir=os.getcwd(), host_name="TEST-NODE")
        result = runtime.execute_script(code)

        self.assertTrue(result["success"])
        self.assertGreater(result["evidence_count"], 0)
        self.assertTrue(len(result["evidence_hash"]) == 64) # Valid SHA-256
        self.assertEqual(result["execution_record"]["status"], "VERIFIED")

    def test_evidence_hash_determinism(self):
        vault1 = EvidenceVault("CASE_A", "HOST_1")
        vault1.add({"type": "test", "key": "val1"})
        h1 = vault1.hash()

        vault2 = EvidenceVault("CASE_A", "HOST_1")
        # Same payload and ID
        vault2.items = [i for i in vault1.items]
        h2 = vault2.hash()

        self.assertEqual(h1, h2)

    def test_cluster_multi_host(self):
        code = '''
        CASE "CLUSTER_TEST"
        processes = host.processes(5)
        evidence.add(processes)
        evidence.hash()
        '''
        cluster = JockyCluster(base_dir=os.getcwd())
        res = cluster.run_multi_host(code, ["NODE-A", "NODE-B"])
        self.assertEqual(res["total_hosts"], 2)
        self.assertEqual(len(res["nodes"]), 2)
        for n in res["nodes"]:
            self.assertEqual(n["status"], "COMPLETE")
            self.assertEqual(len(n["evidence_hash"]), 64)


if __name__ == "__main__":
    unittest.main()
