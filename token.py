from enum import Enum, auto

class TokenType(Enum):
    FLOAT = auto()
    INTEGER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    VAR = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    BANG = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    CARET = auto()
    SEMICOLON = auto()
    BEGIN = auto()
    END = auto()
    NIL = auto()
    TRUE = auto()
    FALSE = auto()
    THEN = auto()
    ELSE = auto()
    PRINT = auto()
    IF = auto()
    WHILE = auto()
    DO = auto()
    RETURN = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


def tokentostring(token):
    if token.type == TokenType.FLOAT:
        return "FLOAT"
    elif token.type == TokenType.INTEGER:
        return "INTEGER"
    elif token.type == TokenType.STRING:
        return "STRING"
    elif token.type == TokenType.IDENTIFIER:
        return "IDENTIFIER"
    elif token.type == TokenType.VAR:
        return "VAR"
    elif token.type == TokenType.EQUAL:
        return "EQUAL"
    elif token.type == TokenType.PLUS:
        return "PLUS"
    elif token.type == TokenType.MINUS:
        return "MINUS"
    elif token.type == TokenType.STAR:
        return "STAR"
    elif token.type == TokenType.SLASH:
        return "SLASH"
    elif token.type == TokenType.PERCENT:
        return "PERCENT"
    elif token.type == TokenType.CARET:
        return "CARET"
    elif token.type == TokenType.SEMICOLON:
        return "SEMICOLON"
    elif token.type == TokenType.BEGIN:
        return "BEGIN"
    elif token.type == TokenType.END:
        return "END"
    elif token.type == TokenType.THEN:
        return "THEN"
    elif token.type == TokenType.ELSE:
        return "ELSE"
    elif token.type == TokenType.PRINT:
        return "PRINT"
    elif token.type == TokenType.IF:
        return "IF"
    elif token.type == TokenType.WHILE:
        return "WHILE"
    elif token.type == TokenType.DO:
        return "DO"
    elif token.type == TokenType.RETURN:
        return "RETURN"
    elif token.type == TokenType.COMMA:
        return "COMMA"
    elif token.type == TokenType.LPAREN:
        return "LPAREN"
    elif token.type == TokenType.RPAREN:
        return "RPAREN"
    elif token.type == TokenType.NIL:
        return "NIL"
    elif token.type == TokenType.TRUE:
        return "TRUE"
    elif token.type == TokenType.FALSE:
        return "FALSE"
    elif token.type == TokenType.EOF:
        return "EOF"

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
    
    def __str__(self):
        if self.literal is None:
            return "(" + self.lexeme + ")" + " " + tokentostring(self)
        return "(" + self.lexeme + ")" + " " + tokentostring(self) + " " + str(self.literal)
