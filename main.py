
from lexer import Lexer
from token import TokenType
from parser import Parser
from ast import Ast,Interpreter


source = '''

var x=255;


print(2 + 3 * 4);



print((2 + 3) * 4); 



print(2 ^ 3 ^ 2);


print(18 / 3 * 2);
print(2 + 3 * 4 ^ 2);
print(2.5 % 2);
print(1+2*3);
print((1+2)*3);
print(2^3^2);
print(6 % 4);
print(-2 + 3 * 4 ^ 2);
print(-(2 + 3) * 4);
print(2 + 3 * 4 ^ -2);



'''

lexer = Lexer(source)
tokens = lexer.tokenize()
# for token in tokens:
#     print(token)

# ast = Ast(tokens)
# result = ast.parse()

# runner  = Interpreter()
# final = runner.interpret(result)
# runner.print_variables()

parser = Parser(tokens)
parser.parse()

print(eval("2 ** 2 * 3 + 5"))