from functools import reduce
from progState import ProgramState
from lexer import lex
import re
from Parser import Parse

FILE = "myL.txt"

content = reduce(lambda x, y: x + y, open(FILE, "r").readlines())

print(Parse(lex(content), content.split('#')[1])[1])
