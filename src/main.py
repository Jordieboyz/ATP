from functools import reduce
from typing import List
from lexer import lex, Token
from Parser import Parse
import re
from progState import ProgramState, runCode

def create_func_declarations(function_list, function_content : str):
    return list(map( lambda x: (x.group()[6:], lex(function_content, x.start() + len('func_'))),   list( re.finditer(r'func_ (\w+)', function_content ))))
        
FILE_NAME = "myL.txt"

content = reduce(lambda x, y: x + y, open(FILE_NAME, "r").readlines())

lexed = lex(content)

empty, parsed = Parse(lexed)


print(runCode(parsed, 0, ProgramState(create_func_declarations([], content.split('#')[1])), None)[1])
