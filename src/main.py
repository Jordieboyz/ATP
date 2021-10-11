import re
def create_func_declarations(function_list, function_content : str):
    return list(map( lambda x: (x.group()[6:], lex(function_content, x.start() + len('func_'))),   list( re.finditer(r'func_ (\w+)', function_content ))))

from functools import reduce
from lexer import lex
from Parser import Parse
from progState import ProgramState, runCode
        
FILE_NAME = "test_func00.txt"

content = reduce(lambda x, y: x + y, open(FILE_NAME, "r").readlines())

lexed = lex(content)

_, parsed = Parse(lexed)

print(runCode(parsed, 0, ProgramState(create_func_declarations([], content.split('#')[1])), None)[1])
