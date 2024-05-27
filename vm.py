import token
from enum import Enum, auto

class OpCode(Enum):
    OP_NIL = auto()
    OP_TRUE = auto()
    OP_FALSE = auto()
    OP_CONSTANT = auto()
    OP_ADD = auto()
    OP_SUBTRACT = auto()
    OP_MULTIPLY = auto()
    OP_DIVIDE = auto()
    OP_MODULO = auto()
    OP_POWER = auto()
    OP_PRINT = auto()
    OP_NEGATE = auto()
    OP_RETURN = auto()
    OP_SET_GLOBAL = auto()
    OP_GET_GLOBAL = auto()
    OP_POP = auto()





class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.ip = 0
        self.bytecode = []
        self.constants = []
        self.variables = {}
        self.varsNames =[]

    def add_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def write_chunk(self, opcode, operand=None):
        self.bytecode.append(opcode)
        if operand is not None:
            self.bytecode.append(operand)

    def disassemble(self,name):
        print("========== Disassemble: " + name + " ===========")
        ip = 0
        while ip < len(self.bytecode):
            opcode = self.bytecode[ip]
            if opcode == OpCode.OP_CONSTANT:
                operand = self.bytecode[ip + 1]
                const_value = self.constants[operand]
                print(f"{ip:04d}  {opcode.name:<16} {operand} '{const_value}'")
                ip += 2
            elif opcode == OpCode.OP_SET_GLOBAL:
                operand = self.bytecode[ip +1]
                name  = self.varsNames[operand]
                value = self.variables[name]
                print(f"{ip:04d}  {opcode.name:<16} {operand} '{name}' '{value}'")
                ip += 2
            elif opcode == OpCode.OP_GET_GLOBAL:
                operand = self.bytecode[ip +1]
                name  = self.varsNames[operand]
                value = self.variables[name]
                print(f"{ip:04d}  {opcode.name:<16} {operand} '{name}' '{value}'")
                ip += 2
            else:
                print(f"{ip:04d}  |{opcode.name}")
                ip += 1

    def print_stack(self):
        print("Stack:", self.stack)
    def print_constants(self):
        print("Constants:", self.constants)
    def print_variables(self):
        print("Variables:", self.variables)

    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]
    
    def const(self, value):
        return self.constants[value]

    def addGlobal(self, name, value):
        self.variables[name] = value
        self.varsNames.append(name)
        index = len(self.varsNames) - 1
        self.write_chunk(OpCode.OP_SET_GLOBAL)
        self.write_chunk(index)
    
    def getGlobal(self, name):
        index = self.variablesIndex(name)
        if index == -1:
            raise Exception("Undefined variable '" + name + "'")
        self.write_chunk(OpCode.OP_GET_GLOBAL)
        self.write_chunk(index)

    def updateGlobal(self, name):
        index = self.variablesIndex(name)
        if index == -1:
            raise Exception("Undefined variable '" + name + "'")
        self.write_chunk(OpCode.OP_SET_GLOBAL)
        self.write_chunk(index)
   
    def variablesIndex(self, name):
        for i in range(len(self.varsNames)):
            if self.varsNames[i] == name:
                return i
        return -1

    def run(self):
        while self.ip < len(self.bytecode):
            opcode = self.bytecode[self.ip]
            self.ip += 1
            if opcode == OpCode.OP_CONSTANT:
                const_index = self.bytecode[self.ip]
                self.ip += 1
                self.push(self.const(const_index))
            elif opcode == OpCode.OP_ADD:
                b = self.pop()
                a = self.pop()
                self.push(a + b)
            elif opcode == OpCode.OP_SUBTRACT:
                b = self.pop()
                a = self.pop()
                self.push(a - b)
            elif opcode == OpCode.OP_MULTIPLY:
                b = self.pop()
                a = self.pop()
                self.push(a * b)
            elif opcode == OpCode.OP_DIVIDE:
                b = self.pop()
                a = self.pop()
                self.push(a / b)
            elif opcode == OpCode.OP_MODULO:
                b = self.pop()
                a = self.pop()
                self.push(a % b)
            elif opcode == OpCode.OP_POWER:
                b = self.pop()
                a = self.pop()
                self.push(a ** b)
            elif opcode == OpCode.OP_NEGATE:
                value = self.stack.pop()
                self.push(-value)
            elif opcode == OpCode.OP_PRINT:
                value = self.pop()
                print(value)
            elif opcode == OpCode.OP_POP:
                self.pop()
            elif opcode == OpCode.OP_NIL:
                self.push(0)
            elif opcode == OpCode.OP_TRUE:
                self.push(1)
            elif opcode == OpCode.OP_FALSE:
                self.push(0)
            elif opcode == OpCode.OP_SET_GLOBAL:
                index = self.bytecode[self.ip]
                self.ip += 1
                name  = self.varsNames[index]
                popValue =  self.peek()
                self.variables[name] = popValue

                #print("DEFINE GLOBAL VAR(",name,") Index:", index, " Value: ", popValue)

            elif opcode == OpCode.OP_GET_GLOBAL:
                name_index = self.bytecode[self.ip]
                self.ip += 1
                
                name  = self.varsNames[name_index]
                value = self.variables[name]
                
                self.push(value)
                #print("GET GLOBAL VAR", name, "Value: ", value)


            elif opcode == OpCode.OP_RETURN:
                return
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

