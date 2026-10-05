"""
JOCKY Parser - Abstract Syntax Tree (AST) generator for JOCKY
"""

from typing import List, Optional, Any
from jocky.lexer import Token, TokenType, LexerError


class ASTNode:
    def __init__(self, line: int = 0):
        self.line = line


class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        super().__init__(statements[0].line if statements else 1)
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"


class CaseDecl(ASTNode):
    def __init__(self, case_id: str, line: int):
        super().__init__(line)
        self.case_id = case_id

    def __repr__(self):
        return f"CaseDecl('{self.case_id}')"


class Literal(ASTNode):
    def __init__(self, value: Any, line: int):
        super().__init__(line)
        self.value = value

    def __repr__(self):
        return f"Literal({repr(self.value)})"


class Identifier(ASTNode):
    def __init__(self, name: str, line: int):
        super().__init__(line)
        self.name = name

    def __repr__(self):
        return f"Identifier('{self.name}')"


class MemberAccess(ASTNode):
    def __init__(self, target: ASTNode, member: str, line: int):
        super().__init__(line)
        self.target = target
        self.member = member

    def __repr__(self):
        return f"MemberAccess({self.target}, '{self.member}')"


class CallExpr(ASTNode):
    def __init__(self, callee: ASTNode, args: List[ASTNode], line: int):
        super().__init__(line)
        self.callee = callee
        self.args = args

    def __repr__(self):
        return f"CallExpr({self.callee}, {self.args})"


class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"


class AssignmentStmt(ASTNode):
    def __init__(self, var_name: str, value_expr: ASTNode, line: int):
        super().__init__(line)
        self.var_name = var_name
        self.value_expr = value_expr

    def __repr__(self):
        return f"AssignmentStmt({self.var_name} = {self.value_expr})"


class ExpressionStmt(ASTNode):
    def __init__(self, expr: ASTNode, line: int):
        super().__init__(line)
        self.expr = expr

    def __repr__(self):
        return f"ExpressionStmt({self.expr})"


class ForLoop(ASTNode):
    def __init__(self, var_name: str, iterable_expr: ASTNode, body: List[ASTNode], line: int):
        super().__init__(line)
        self.var_name = var_name
        self.iterable_expr = iterable_expr
        self.body = body

    def __repr__(self):
        return f"ForLoop({self.var_name} in {self.iterable_expr}, body={self.body})"


class IfStmt(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: Optional[List[ASTNode]], line: int):
        super().__init__(line)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfStmt(cond={self.condition}, then={self.then_branch}, else={self.else_branch})"


class EchoStmt(ASTNode):
    def __init__(self, expr: ASTNode, line: int):
        super().__init__(line)
        self.expr = expr

    def __repr__(self):
        return f"EchoStmt({self.expr})"


class ParserError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        if token:
            super().__init__(f"[Line {token.line}, Col {token.column}] Parser Error: {message}")
            self.line = token.line
            self.column = token.column
        else:
            super().__init__(f"Parser Error: {message}")
            self.line = 0
            self.column = 0


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def peek(self, offset: int = 1) -> Token:
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return self.tokens[-1]

    def advance(self) -> Token:
        token = self.current_token()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def match(self, *types: TokenType) -> bool:
        if self.current_token().type in types:
            self.advance()
            return True
        return False

    def expect(self, token_type: TokenType, error_msg: str) -> Token:
        token = self.current_token()
        if token.type == token_type:
            return self.advance()
        raise ParserError(f"{error_msg}. Expected {token_type.name}, found {token.type.name} ('{token.value}')", token)

    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()

    def parse(self) -> Program:
        statements = []
        self.skip_newlines()

        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()

        return Program(statements)

    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        token = self.current_token()

        if token.type == TokenType.EOF:
            return None

        # CASE "INCIDENT_001"
        if token.type == TokenType.KEYWORD_CASE:
            return self.parse_case_decl()

        # FOR item IN list { ... }
        if token.type == TokenType.KEYWORD_FOR:
            return self.parse_for_loop()

        # IF cond { ... } ELSE { ... }
        if token.type == TokenType.KEYWORD_IF:
            return self.parse_if_stmt()

        # ECHO expr
        if token.type == TokenType.KEYWORD_ECHO:
            return self.parse_echo_stmt()

        # Identifier: could be assignment (a = ...) or method call (evidence.add(...))
        if token.type == TokenType.IDENTIFIER:
            # Check if next token is ASSIGN (=)
            if self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()
            
            # Expression statement (e.g. evidence.add(...), report.generate())
            expr = self.parse_expression()
            return ExpressionStmt(expr, token.line)

        # Fallback to general expression
        expr = self.parse_expression()
        return ExpressionStmt(expr, token.line)

    def parse_case_decl(self) -> CaseDecl:
        case_token = self.expect(TokenType.KEYWORD_CASE, "Expected 'CASE'")
        str_token = self.expect(TokenType.STRING, "Expected string case identifier (e.g. CASE 'INC_001')")
        return CaseDecl(str_token.value, case_token.line)

    def parse_assignment(self) -> AssignmentStmt:
        var_token = self.expect(TokenType.IDENTIFIER, "Expected variable name in assignment")
        self.expect(TokenType.ASSIGN, "Expected '=' in assignment")
        expr = self.parse_expression()
        return AssignmentStmt(var_token.value, expr, var_token.line)

    def parse_for_loop(self) -> ForLoop:
        for_token = self.expect(TokenType.KEYWORD_FOR, "Expected 'FOR'")
        var_token = self.expect(TokenType.IDENTIFIER, "Expected loop variable name")
        self.expect(TokenType.KEYWORD_IN, "Expected 'IN' after loop variable")
        iterable_expr = self.parse_expression()
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE, "Expected '{' to begin FOR loop block")
        
        body = []
        self.skip_newlines()
        while self.current_token().type not in (TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.RBRACE, "Expected '}' to close FOR loop block")
        return ForLoop(var_token.value, iterable_expr, body, for_token.line)

    def parse_if_stmt(self) -> IfStmt:
        if_token = self.expect(TokenType.KEYWORD_IF, "Expected 'IF'")
        condition = self.parse_expression()

        self.skip_newlines()
        self.expect(TokenType.LBRACE, "Expected '{' to begin IF block")

        then_branch = []
        self.skip_newlines()
        while self.current_token().type not in (TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                then_branch.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.RBRACE, "Expected '}' to close IF block")

        else_branch = None
        self.skip_newlines()
        if self.current_token().type == TokenType.KEYWORD_ELSE:
            self.advance()
            self.skip_newlines()
            self.expect(TokenType.LBRACE, "Expected '{' to begin ELSE block")
            else_branch = []
            self.skip_newlines()
            while self.current_token().type not in (TokenType.RBRACE, TokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    else_branch.append(stmt)
                self.skip_newlines()
            self.expect(TokenType.RBRACE, "Expected '}' to close ELSE block")

        return IfStmt(condition, then_branch, else_branch, if_token.line)

    def parse_echo_stmt(self) -> EchoStmt:
        echo_token = self.expect(TokenType.KEYWORD_ECHO, "Expected 'ECHO'")
        expr = self.parse_expression()
        return EchoStmt(expr, echo_token.line)

    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()

    def parse_comparison(self) -> ASTNode:
        expr = self.parse_primary_or_call()

        while self.current_token().type in (
            TokenType.EQUALS, TokenType.NOT_EQUALS,
            TokenType.GREATER, TokenType.LESS,
            TokenType.GREATER_EQ, TokenType.LESS_EQ
        ):
            op_token = self.advance()
            right = self.parse_primary_or_call()
            expr = BinaryOp(expr, op_token.value, right, op_token.line)

        return expr

    def parse_primary_or_call(self) -> ASTNode:
        expr = self.parse_primary()

        while True:
            # Method or member access: expr.member
            if self.current_token().type == TokenType.DOT:
                dot_token = self.advance()
                ident_token = self.expect(TokenType.IDENTIFIER, "Expected property or method name after '.'")
                expr = MemberAccess(expr, ident_token.value, dot_token.line)
            # Function/Method invocation: expr(...)
            elif self.current_token().type == TokenType.LPAREN:
                paren_token = self.advance()
                args = []
                self.skip_newlines()
                if self.current_token().type != TokenType.RPAREN:
                    while True:
                        self.skip_newlines()
                        arg = self.parse_expression()
                        args.append(arg)
                        self.skip_newlines()
                        if self.current_token().type == TokenType.COMMA:
                            self.advance()
                        else:
                            break
                self.expect(TokenType.RPAREN, "Expected ')' after argument list")
                expr = CallExpr(expr, args, paren_token.line)
            else:
                break

        return expr

    def parse_primary(self) -> ASTNode:
        token = self.current_token()

        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value, token.line)

        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(token.value, token.line)

        if token.type == TokenType.BOOLEAN:
            self.advance()
            return Literal(token.value, token.line)

        if token.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.value, token.line)

        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' to close parentheses")
            return expr

        raise ParserError(f"Unexpected token: {token.type.name} ('{token.value}')", token)
