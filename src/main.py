from tokens import Token
from functools import reduce
from progState import ProgramState
from lexer import Lexer

FILE = "myL.txt"

file = open(FILE, "r")
file_content = file.readlines()

content = reduce(lambda x, y: x + y, file_content)

tokens = Lexer(content).create_tokens()

for token in tokens:
    print(token)
