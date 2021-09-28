from typing import List
from lexer import lex
from tokens import Token, Func, Number, Variable, Is, If, ExprIfStatement, \
                   StartIfStatement, CloseFuncParam, OpenFuncParam, Comma, \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, EndExprLoop, tokendict
    
class Statement():
    def __str__(self):
        return "undefined statement"

class Scope:
    def __init__(self, nest : int = 1):
        self.statements = []
        self.nestlevel = nest
    
    def add_statement(self, statement : Statement):
        self.statements.append(statement)
        return self
    
    def __str__(self):
        nstr = repeatStr("   ", self.nestlevel)
        statestr = ''.join(map(lambda st: nstr + str(st) + "\n", self.statements))
        return "Begin Scope: \n" + statestr + repeatStr("   ", self.nestlevel - 1) + "End Scope"
    
    def __repr__(self):
        return self.__str__()

#repeatStr :: String -> Integer -> String
def repeatStr(s : str, i : int):
    if (i <= 0):
        return ""
    return s + repeatStr(s, i - 1)

class MathStatement(Statement):
    def __init__(self, lvalue : Variable, operator : Token, rvalue : Number):
        self.lvalue = lvalue
        self.operator = operator
        self.rvalue = rvalue
        
    def __str__(self):
        return "{} with: {} {} {}". \
            format(type(self).__name__, self.lvalue, self.operator, self.rvalue)
    
    def __repr__(self):
        return self.__str__()
    
class IfStatement(Statement):
    def __init__(self, lvalue, operator : Token, rvalue):
        self.lvalue = lvalue
        self.operator = operator
        self.rvalue = rvalue
        
    def __str__(self):
        return "{} with: {} {} {}". \
            format(type(self).__name__, self.lvalue, self.operator, self.rvalue)
    
    def __repr__(self):
        return self.__str__()
        
class Function(Statement):
    def __init__(self, funcname : str):
        self.funcname = funcname
        self.func_params = []
        self.func_scope = []
        
    def __str__(self):
        return "{} {} with {} and [ {} ]".format(type(self).__name__, self.funcname, self.func_params, self.func_scope.__str__())
    
    def __repr__(self):
        return self.__str__()

    
class ConditionsLoop(Statement):
    def __init__(self, expr : IfStatement):
        self.expr = expr
        
    def __str__(self):
        return "{} with: {}". \
            format(type(self).__name__, self.expr)
    
    def __repr__(self):
        return self.__str__()
    
class OpenScope(Statement):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class CloseScope(Statement):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()


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
    if function_string is not None:
        return parseInScopes(parseInStatements(tokenlist, [], None, None, init_functions([], function_string))[1], Scope())
    else:
        return parseInScopes(parseInStatements(tokenlist, [], None, None, None)[1], Scope())

def init_functions(function_list : List, function_content : str):
    for m in re.finditer(r'func_ (\w+)', function_content):
        function_list.append([m.group()[6:],  lex(function_content, m.start() + len('func_'))[4:]])
    return function_list



