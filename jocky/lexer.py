"""
JOCKY Lexer - Tokenizer for JOCKY Forensic Scripting Language
"""

from enum import Enum, auto
from typing import List, Optional


class TokenType(Enum):
    # Keywords
    KEYWORD_CASE = auto()
    KEYWORD_FOR = auto()
    KEYWORD_IN = auto()
    KEYWORD_IF = auto()
    KEYWORD_ELSE = auto()
    KEYWORD_FILTER = auto()
    KEYWORD_ECHO = auto()
    KEYWORD_RETURN = auto()
    
    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    
    # Symbols & Operators
    ASSIGN = auto()          # =
    DOT = auto()             # .
    COMMA = auto()           # ,
    COLON = auto()           # :
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    
    EQUALS = auto()          # ==
    NOT_EQUALS = auto()      # !=
    GREATER = auto()         # >
    LESS = auto()            # <
    GREATER_EQ = auto()      # >=
    LESS_EQ = auto()         # <=
    
    # Special
    NEWLINE = auto()
    EOF = auto()


class Token:
    def __init__(self, type_: TokenType, value: any, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"


KEYWORDS = {
    "CASE": TokenType.KEYWORD_CASE,
    "case": TokenType.KEYWORD_CASE,
    "FOR": TokenType.KEYWORD_FOR,
    "for": TokenType.KEYWORD_FOR,
    "IN": TokenType.KEYWORD_IN,
    "in": TokenType.KEYWORD_IN,
    "IF": TokenType.KEYWORD_IF,
    "if": TokenType.KEYWORD_IF,
    "ELSE": TokenType.KEYWORD_ELSE,
    "else": TokenType.KEYWORD_ELSE,
    "FILTER": TokenType.KEYWORD_FILTER,
    "filter": TokenType.KEYWORD_FILTER,
    "ECHO": TokenType.KEYWORD_ECHO,
    "echo": TokenType.KEYWORD_ECHO,
    "PRINT": TokenType.KEYWORD_ECHO,
    "print": TokenType.KEYWORD_ECHO,
    "RETURN": TokenType.KEYWORD_RETURN,
    "return": TokenType.KEYWORD_RETURN,
    "TRUE": TokenType.BOOLEAN,
    "true": TokenType.BOOLEAN,
    "FALSE": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
}


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"[Line {line}, Col {column}] Lexer Error: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def current_char(self) -> Optional[str]:
        if self.pos >= self.length:
            return None
        return self.source[self.pos]

    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        if peek_pos >= self.length:
            return None
        return self.source[peek_pos]

    def advance(self) -> Optional[str]:
        char = self.current_char()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def skip_whitespace_and_comments(self):
        while self.pos < self.length:
            char = self.current_char()
            
            # Skip space/tab/carriage return
            if char in (' ', '\t', '\r'):
                self.advance()
                continue
                
            # Skip single-line comments (# or //)
            if char == '#':
                while self.pos < self.length and self.current_char() != '\n':
                    self.advance()
                continue
            if char == '/' and self.peek() == '/':
                self.advance()
                self.advance()
                while self.pos < self.length and self.current_char() != '\n':
                    self.advance()
                continue
                
            break

    def read_string(self, quote_char: str) -> Token:
        start_col = self.column
        start_line = self.line
        self.advance() # Skip opening quote
        chars = []
        
        while self.pos < self.length:
            char = self.current_char()
            if char == quote_char:
                self.advance() # Skip closing quote
                return Token(TokenType.STRING, "".join(chars), start_line, start_col)
            elif char == '\\':
                self.advance()
                escaped = self.current_char()
                if escaped == 'n':
                    chars.append('\n')
                elif escaped == 't':
                    chars.append('\t')
                elif escaped == '\\':
                    chars.append('\\')
                elif escaped == quote_char:
                    chars.append(quote_char)
                else:
                    chars.append('\\')
                    if escaped:
                        chars.append(escaped)
                self.advance()
            elif char == '\n':
                raise LexerError("Unterminated string literal across newline", start_line, start_col)
            else:
                chars.append(char)
                self.advance()
                
        raise LexerError("Unterminated string literal at end of input", start_line, start_col)

    def read_number(self) -> Token:
        start_col = self.column
        start_line = self.line
        num_str = []
        has_dot = False

        while self.pos < self.length:
            char = self.current_char()
            if char.isdigit():
                num_str.append(char)
                self.advance()
            elif char == '.' and not has_dot and self.peek() and self.peek().isdigit():
                has_dot = True
                num_str.append(char)
                self.advance()
            else:
                break

        val = float("".join(num_str)) if has_dot else int("".join(num_str))
        return Token(TokenType.NUMBER, val, start_line, start_col)

    def read_identifier(self) -> Token:
        start_col = self.column
        start_line = self.line
        chars = []

        while self.pos < self.length:
            char = self.current_char()
            if char.isalnum() or char in ('_', '-'):
                chars.append(char)
                self.advance()
            else:
                break

        ident = "".join(chars)
        if ident in KEYWORDS:
            token_type = KEYWORDS[ident]
            if token_type == TokenType.BOOLEAN:
                val = ident.lower() == "true"
                return Token(TokenType.BOOLEAN, val, start_line, start_col)
            return Token(token_type, ident.upper(), start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, ident, start_line, start_col)

    def tokenize(self) -> List[Token]:
        tokens = []

        while self.pos < self.length:
            self.skip_whitespace_and_comments()
            
            if self.pos >= self.length:
                break

            char = self.current_char()
            start_line = self.line
            start_col = self.column

            if char == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                self.advance()
            elif char in ('"', "'"):
                tokens.append(self.read_string(char))
            elif char.isdigit():
                tokens.append(self.read_number())
            elif char.isalpha() or char == '_':
                tokens.append(self.read_identifier())
            elif char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.EQUALS, '==', start_line, start_col))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col))
            elif char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.NOT_EQUALS, '!=', start_line, start_col))
                else:
                    raise LexerError(f"Unexpected character '!'", start_line, start_col)
            elif char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.GREATER_EQ, '>=', start_line, start_col))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.GREATER, '>', start_line, start_col))
            elif char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(TokenType.LESS_EQ, '<=', start_line, start_col))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.LESS, '<', start_line, start_col))
            elif char == '.':
                self.advance()
                tokens.append(Token(TokenType.DOT, '.', start_line, start_col))
            elif char == ',':
                self.advance()
                tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
            elif char == ':':
                self.advance()
                tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
            elif char == '(':
                self.advance()
                tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
            elif char == ')':
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
            elif char == '{':
                self.advance()
                tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col))
            elif char == '}':
                self.advance()
                tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col))
            elif char == '[':
                self.advance()
                tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col))
            elif char == ']':
                self.advance()
                tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col))
            else:
                raise LexerError(f"Unexpected character: '{char}'", start_line, start_col)

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
