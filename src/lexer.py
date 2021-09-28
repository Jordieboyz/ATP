import re
from typing import List
from tokens import Token, Func, Number, Variable, Is, If, ExprIfStatement, \
                   StartIfStatement, CloseFuncParam, OpenFuncParam, Comma, \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, EndExprLoop, tokendict
                  
def is_number(c : chr):
    return re.compile(r'[0-9]').match(c)
                 
def is_alpha_char( c: chr):
    return re.compile(r'[a-z]|[A-Z]').match(c)

def char_expr( expr : chr):
    return expr in r'={}&+-?/*()[]<>%,$'

def lex_it( file_string : str, tokenlist, tmp : str):
    def add_var_or_number_token():
        if tmp:
            tokenlist.append(Number(tmp)) if is_number(tmp[0]) else tokenlist.append(Variable(tmp))
            return True
        return False
    
    if not file_string:
        return tokenlist

    c, *rest = file_string 
    
    if c in '#_':
        return tokenlist
    
    if c in ' \t\n':
        if add_var_or_number_token():
            tmp = ''
            
    elif is_number(c) or is_alpha_char(c):
        tmp += c  
    
    elif char_expr(c):
        if add_var_or_number_token():
            tmp = ''
        if c in tokendict:   
            tokenlist.append(tokendict[c]())
   
    return lex_it(rest, tokenlist, tmp)
                   
def finish_lexing(tokens: List[Token], idx : int):
    if not idx < len(tokens):
        return tokens
    
    # Variable + OpenFuncParam == Func
    if isinstance(tokens[idx], OpenFuncParam):
        tokens[idx - 1] = Func(tokens[idx - 1].content)
    
    # fix the "$-exprsessions" f.e.  ($) + (eq) or ($) + (lt)        
    if isinstance(tokens[idx], ExprIfStatement):
        tokens[idx].expr = tokens[idx + 1].content
        del tokens[idx + 1]
    return finish_lexing(tokens, idx + 1)
        
def lex(file_str : str, start_from : int = 0):
    tokens = lex_it(file_str[start_from:], [], '')
    return finish_lexing(tokens, 0)


