import vm
from vm import OpCode
from vm import VirtualMachine

from token import TokenType, Token
from enum import Enum, auto


# program         -> statement* EOF ;
# statement       -> varDecl | exprStmt | block ;
# varDecl         -> "var" IDENTIFIER "=" expression ";" ;
# exprStmt        -> expression ";" ;
# block           -> "begin" statement* "end" ;
# expression      -> term ( ( "+" | "-" ) term )* ;
# term            -> factor ( ( "*" | "/" | "%" ) factor )* ;
# factor          -> primary ( "^" factor )? ;
# primary         -> FLOAT | INTEGER | STRING | IDENTIFIER | "(" expression ")" ;


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.vm = VirtualMachine()


    
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise Exception(message)
   
   
    def endCompiler(self):
        self.emitReturn()
    def emitReturn(self):
        self.vm.write_chunk(OpCode.OP_RETURN)
    
    def emitByte(self, bytecode):
        self.vm.write_chunk(bytecode)
    
    def emitBytes(self, bytecode1, bytecode2):
        self.vm.write_chunk(bytecode1)
        self.vm.write_chunk(bytecode2)
    
    def emitConstant(self, value):
        const_index = self.vm.add_constant(value)
        self.emitBytes(OpCode.OP_CONSTANT, const_index)




    def parse(self):
        while not self.is_at_end():
            self.declaration()
        #self.vm.write_chunk(OpCode.OP_PRINT)
        self.vm.write_chunk(OpCode.OP_RETURN)
        self.vm.run()
        #self.vm.disassemble("test chunk")
        self.vm.print_stack()
        self.vm.print_variables()
        self.vm.print_constants()
        
    
    # declaration     -> varDecl | statement ;
    def declaration(self):
        if self.match(TokenType.VAR):
            self.var_declaration()
        else:
            self.statement()

       
        

    # statement       -> printStmt | exprStmt | block ;
    def statement(self):
        if self.match(TokenType.BEGIN):
            self.block()
        elif self.match(TokenType.PRINT):
            self.printStatement()
        else:
            self.expression_statement()

    def variable(self):
        token = self.previous()
        name = token.lexeme
        if self.match(TokenType.EQUAL):
            self.expression()
            self.vm.updateGlobal(name)
            #print ("VARIABLE set", name)

        else :
            token = self.previous()
            self.vm.getGlobal(name)
            #print("VARIABLE get", token)
    
    def printStatement(self):
        self.consume(TokenType.LPAREN, "Expect '(' after 'print'.")
        self.expression()
        self.consume(TokenType.RPAREN, "Expect ')' after expression.")
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        self.emitByte(OpCode.OP_PRINT)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        if self.match(TokenType.EQUAL):
            self.expression()
        else :
            self.emitByte(OpCode.OP_NIL)
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        self.vm.addGlobal(name.lexeme, None)        # the virtual machine will add the value 




    def identifierConstant(self,name):
        for i in range(len(self.vm.constants)):
            if self.vm.constants[i] == name:
                return i
        return -1

    def block(self):
        while not self.check(TokenType.END) and not self.is_at_end():
            self.statement()
        self.consume(TokenType.END, "Expect 'end' after block.")

    def expression_statement(self):
        self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        self.emitByte(OpCode.OP_POP)

    def expression(self):
        self.term()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            self.term()
            if operator.type == TokenType.PLUS:
                self.emitByte(OpCode.OP_ADD)
            elif operator.type == TokenType.MINUS:
                self.emitByte(OpCode.OP_SUBTRACT)

    def term(self):
        self.factor()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.previous()
            self.factor()
            if operator.type == TokenType.STAR:
                self.emitByte(OpCode.OP_MULTIPLY)
            elif operator.type == TokenType.SLASH:
                self.emitByte(OpCode.OP_DIVIDE)
            elif operator.type == TokenType.PERCENT:
                self.emitByte(OpCode.OP_MODULO)

    def factor(self):
        self.unary()
        while self.match(TokenType.CARET):
            self.factor()
            self.emitByte(OpCode.OP_POWER)

    def unary(self):
        if self.match(TokenType.MINUS):
            self.unary()
            self.emitByte(OpCode.OP_NEGATE)
        else:
            self.primary()

    def primary(self):
        if self.match(TokenType.INTEGER, TokenType.FLOAT):
            self.emitConstant(self.previous().literal)
        elif self.match(TokenType.STRING):
            string_literal = self.previous().literal
            self.emitConstant(string_literal)
        elif self.match(TokenType.TRUE):
            self.emitByte(OpCode.OP_TRUE)
        elif self.match(TokenType.FALSE):
            self.emitByte(OpCode.OP_FALSE)
        elif self.match(TokenType.NIL):
            self.emitByte(OpCode.OP_NIL)
        elif self.match(TokenType.IDENTIFIER):
            self.variable()
        elif self.match(TokenType.LPAREN):
            self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
        else:
            raise Exception("Expect expression, but have" + str(self.previous()))      