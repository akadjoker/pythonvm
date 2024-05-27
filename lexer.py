import enum
import re
from token import Token, TokenType, tokentostring


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.start = 0
        self.line = 1

    def tokenize(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "EOF", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scan_token(self):
        char = self.advance()
        if char == ' ' or char == '\r' or char == '\t':
            pass
        elif char == '\n':
            self.line += 1
        elif char.isdigit() or char == '.':
            self.number()
        elif char == '"':
            self.string()
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif char == '<':
            if self.match('='):
                self.add_token(TokenType.LESSE_QUAL)
            else:
                self.add_token(TokenType.LESS)
        elif char == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif char == '*':
            self.add_token(TokenType.STAR)
        elif char == '/':
            self.add_token(TokenType.SLASH)
        elif char == '%':
            self.add_token(TokenType.PERCENT)
        elif char == '^':
            self.add_token(TokenType.CARET)
        elif char == '=':
            self.add_token(TokenType.EQUAL)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '(':
            self.add_token(TokenType.LPAREN)
        elif char == ')':
            self.add_token(TokenType.RPAREN)
        elif char == '{':
            while self.peek() != '}' and not self.is_at_end():
                if self.peek() == '\n':
                    self.line += 1
                self.advance()
            if self.is_at_end():
                raise Exception("Unterminated comment. at line: " + str(self.line))
        elif char == '}':
            self.advance()
            
        elif char == '#':
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()            
        elif char == 'b' and self.match('egin'):
            self.add_token(TokenType.BEGIN)
        elif char == 'e' and self.match('nd'):
            self.add_token(TokenType.END)
        elif char == 't' and self.match('hen'):
            self.add_token(TokenType.THEN)
        elif char == 'e' and self.match('lse'):
            self.add_token(TokenType.ELSE)
        elif char == 'p' and self.match('rint'):
            self.add_token(TokenType.PRINT)
        elif char == 'i' and self.match('f'):
            self.add_token(TokenType.IF)
        elif char == 'w' and self.match('hile'):
            self.add_token(TokenType.WHILE)
        elif char == 'd' and self.match('o'):
            self.add_token(TokenType.DO)
        elif char == 'r' and self.match('eturn'):
            self.add_token(TokenType.RETURN)
        elif char == 'n' and self.match('il'):
            self.add_token(TokenType.NIL)
        elif char == 't' and self.match('rue'):
            self.add_token(TokenType.TRUE)
        elif char == 'f' and self.match('alse'):
            self.add_token(TokenType.FALSE)
        elif char.isalpha():
            self.identifier()
        elif char == ',':
            self.add_token(TokenType.COMMA)
        else:
            raise Exception(f"Unexpected character: {char} at line: {self.line}")

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current:self.current+len(expected)] != expected:
            return False
        self.current += len(expected)
        return True

    def number(self):
        isFloat = False
        while self.peek().isdigit() or (self.peek() == '.'):
            if self.peek() == '.':
                isFloat = True
            self.advance()
        if isFloat:
            self.add_token(TokenType.FLOAT, float(self.source[self.start:self.current]))
        else:
            self.add_token(TokenType.INTEGER, int(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise Exception("Unterminated string " + " at line: " + str(self.line))
        self.advance()  
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        if text == 'var':
            self.add_token(TokenType.VAR)
        else:
            self.add_token(TokenType.IDENTIFIER, text)

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]