from typing import List
from tokens import Token, Func, Number, Variable, ExprIfStatement, \
                   OpenFuncParam, tokendict

def char_expr( expr : chr ):
    return expr in r'=+-*()[]<>%$,.'


def lex_it( file_string : str, tokenlist : List[Token], tmp : str):
    if not file_string:
        return tokenlist

    c, *rest = file_string 
    
    if c in '#_':
        return tokenlist
    
    if c in ' \t\n':
        if tmp:
            tokenlist.append(Number(tmp)) if tmp[0].isnumeric() else tokenlist.append(Variable(tmp))
            tmp = ''
            
    elif c.isnumeric() or c.isalpha():
        tmp += c  
    
    elif char_expr(c):
        if tmp:
            tokenlist.append(Number(tmp)) if tmp[0].isnumeric() else tokenlist.append(Variable(tmp))
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


