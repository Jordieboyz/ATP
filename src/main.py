from functools import reduce
from lexer import lex
from Parser import Parse
from progState import ProgramState, runCode

FILE_NAME = "myL.txt"

content = reduce(lambda x, y: x + y, open(FILE_NAME, "r").readlines())

lexed = lex(content)
empty, parsed = Parse(lexed, content.split('#')[1])

print(runCode(parsed, 0, ProgramState(), None))
