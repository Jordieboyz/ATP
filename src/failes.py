
def parseInStatements(tokenlist : List[Token], statementlist : List[Statement], last_token : Token, cur_statement : Statement, func_list : List[Scope]):
    if not tokenlist:
        return None, statementlist
    
    token, *rest = tokenlist 
    
    if isinstance( token, (Is, Add, Minus, Times, Divide, Modulo) ):
        return parseInStatements(rest, statementlist, token, MathStatement(last_token, token, None), func_list)
        
    elif isinstance( token, Func ):
        if cur_statement is not None:
            statementlist.append(cur_statement)
            return parseInStatements(rest, statementlist, token, Function(token.content), func_list)
            
    elif isinstance( token, OpenFuncParam ):
        if not cur_statement.func_scope:
            for fname in func_list:
                if cur_statement.funcname == fname[0]:
                    cur_statement.func_scope = parseInStatements(fname[1], cur_statement.func_scope, None, None, func_list)[1]
        return parseInStatements(rest, statementlist, token, cur_statement, func_list)
    
    
    elif isinstance( token, CloseFuncParam ):
        if isinstance( cur_statement, Function ):
            if isinstance( statementlist[-1], (IfStatement, MathStatement)):
                if statementlist[-1].rvalue is None:
                    statementlist[-1].rvalue = cur_statement
        return parseInStatements(rest, statementlist, token, cur_statement, func_list)
            
        
    elif isinstance( token, (Variable, Number) ):
        if cur_statement is not None:
            if isinstance(cur_statement, Function):
                cur_statement.func_params.append(token)
                return parseInStatements(rest, statementlist, token, cur_statement, func_list)
            else:
                cur_statement.rvalue = token
                statementlist.append(cur_statement)
                return parseInStatements(rest, statementlist, token, None, func_list)
        
    elif isinstance(token, ExprIfStatement):
        return parseInStatements(rest, statementlist, token, IfStatement(last_token, token, None), func_list)
    
    elif isinstance(token, StartExprLoop):
        statementlist.append(ConditionsLoop(None))
        return parseInStatements(rest, statementlist, token, None, func_list) 
    
    elif isinstance(token, EndExprLoop):
        statementlist[-2].expr = statementlist[-1]
        del statementlist[-1]
        return parseInStatements(rest, statementlist, token, None, func_list)
    
    elif isinstance(token, OpenLoop):
        statementlist.append(OpenScope())
        return parseInStatements(rest, statementlist, token, None, func_list)
    
    elif isinstance(token, CloseLoop):
        statementlist.append(CloseScope())
        return parseInStatements(rest, statementlist, token, None, func_list)

    return parseInStatements(rest, statementlist, token, None, func_list)

def parseInScopes(statementlist : List[Statement], cur_scope : Scope):
    if not statementlist:
        return None, cur_scope
    
    statement, *rest = statementlist
    
    if isinstance( statement, CloseScope):
        return rest, cur_scope
    
    elif isinstance( statement, (IfStatement, MathStatement)):
        if isinstance( statement.rvalue, Function):
            newrest, newscope = parseInScopes(statement.rvalue.func_scope, Scope(nest=cur_scope.nestlevel + 1))
            statement.rvalue.func_scope = newscope

    elif isinstance( statement, OpenScope ):
        newrest, newscope = parseInScopes(rest, Scope(nest=cur_scope.nestlevel + 1))
        return parseInScopes(newrest, cur_scope.add_statement(newscope))
    return parseInScopes(rest, cur_scope.add_statement(statement))
 
import re
def Parse(tokenlist : List[Token], function_string : str = None):
    s = parseTokensToStatements(tokenlist, [], None)
    for t in s[1]:
        print(t)
    return s
    
    
    
    # if function_string is not None:
    #     return parseInScopes(parseInStatements(tokenlist, [], None, None, init_functions([], function_string))[1], Scope())
    # else:
    #     return parseInScopes(parseInStatements(tokenlist, [], None, None, None)[1], Scope())

def init_functions(function_list : List, function_content : str):
    return map( lambda x: (x.group()[6:], lex(function_content, x.start() + len('func_'))[4:]),                                                   \
                   list( re.finditer(r'func_ (\w+)', function_content )))                                                       


