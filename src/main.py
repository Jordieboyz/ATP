from functools import reduce
from lexer import lex
from Parser import Parse
import sys
sys.setrecursionlimit(200000)

FILE_NAME = "myL.txt"

content = reduce(lambda x, y: x + y, open(FILE_NAME, "r").readlines())

lexed = lex(content)
empty, parsed = Parse(lexed, content.split('#')[1])
print(parsed)