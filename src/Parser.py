from typing import List
from lexer import lex
from tokens import Token, Func, Number, Variable, Is, If, ExprIfStatement, \
                   StartIfStatement, CloseFuncParam, OpenFuncParam, \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, EndExprLoop, tokendict, Comma, Return
    
st_dict : dict() = {
    Is              : lambda l, op, r: MathStatement(l, op, r),
    Add               : lambda l, op, r: MathStatement(l, op, r),
    Minus             : lambda l, op, r: MathStatement(l, op, r),
    Times             : lambda l, op, r: MathStatement(l, op, r),
    Divide            : lambda l, op, r: MathStatement(l, op, r),
    Modulo            : lambda l, op, r: MathStatement(l, op, r),
    ExprIfStatement   : lambda l, op, r: IfStatement(l, op, r),
    OpenLoop          : lambda : OpenScope(),
    CloseLoop         : lambda : CloseScope(),
    StartExprLoop     : lambda : ConditionsLoop(),
    Func              : lambda n : Function(n),
    Return            : lambda : ReturnFunc()
}
    
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
        return self.statements.__str__()
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
    def __init__(self, lvalue, operator, rvalue):
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
        self.ret_val = None
        
    def __str__(self):
        return "{} {} with {} \t{}".format(type(self).__name__, self.funcname, self.func_params, self.func_scope.__str__())
    
    def __repr__(self):
        return self.__str__()

    
class ConditionsLoop(Statement):
    def __init__(self):
        self.expr = None
        
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
    
class ReturnFunc(Statement):
    def __init__(self):
        self.rvalue = None
        
    def __str__(self):
        return "{} with: {}". \
            format(type(self).__name__, self.rvalue)
    
    def __repr__(self):
        return self.__str__()


def parseTokensToStatements(tokenlist : List[Token], statementlist : List[Statement], last_token : Token, cur_statement : Statement, func_list):
    if not tokenlist:
        return None, statementlist
    append = lambda l, x: l if l.append(x) is None else l
    remove = lambda l, x: l if l.remove(x) is None else l
    token, *rest = tokenlist
    
    if cur_statement is not None:
        if isinstance(cur_statement, Function) and isinstance( last_token, OpenFuncParam):
            if not isinstance(token, CloseFuncParam): 
                cur_statement.func_params.append(token)
                return parseTokensToStatements(rest, statementlist, last_token, cur_statement, func_list)
            else:
                
                
                cur_statement.func_params = parseTokensToStatements(cur_statement.func_params, [], None, cur_statement, None)[1]
                
                tokens = list(filter(None, map( lambda x, y: x[1] if x[0] == y else None , func_list, [cur_statement.funcname]*len(func_list))))
                if tokens:
                    cur_statement.func_scope = parseTokensToStatements(tokens[0], [], None, None, func_list)[1]
    
                if isinstance( statementlist[-1], (MathStatement, IfStatement, ReturnFunc)):
                    if statementlist[-1].rvalue is None:
                        statementlist[-1].rvalue = cur_statement
                        return parseTokensToStatements(rest, statementlist, token, None, func_list)
                return parseTokensToStatements(rest, append(statementlist, cur_statement), token, None, func_list)
  

    if isinstance( token, (Variable, Number)):
        if isinstance( cur_statement, (IfStatement, MathStatement, ReturnFunc)):
            if cur_statement.rvalue is None:
                cur_statement.rvalue = token
                return parseTokensToStatements(rest, statementlist, token, None, func_list)
        
    if func_list is None:
        if isinstance(token, (Variable, Number)):
            return parseTokensToStatements(rest, append(statementlist, token), token, cur_statement, func_list)
        elif isinstance( token, (Is, Add, Minus, Times, Divide, Modulo, ExprIfStatement) ):
            return parseTokensToStatements(rest, remove(append(statementlist, st_dict[type(token)](last_token, token, None)), statementlist[-2]), token, statementlist[-1], func_list)
        
    elif isinstance(token, EndExprLoop):
        if isinstance( statementlist[-1], IfStatement) and isinstance(statementlist[-2], ConditionsLoop):
            statementlist[-2].expr = statementlist[-1]
            del statementlist[-1]        
        
    elif isinstance( token, (Is, Add, Minus, Times, Divide, Modulo, ExprIfStatement) ):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)](last_token, token, None)), token, statementlist[-1], func_list)
    
    elif isinstance(token, (StartExprLoop, OpenLoop, CloseLoop)):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, None, func_list)
    
    elif isinstance(token, Return):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, statementlist[-1], func_list)
    
    elif isinstance(token, OpenFuncParam):
        if isinstance(last_token, Func):
            return parseTokensToStatements(rest, statementlist, token, st_dict[type(last_token)](last_token.content), func_list)
        
    
    return parseTokensToStatements(rest, statementlist, token, cur_statement, func_list) 


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
    
    elif isinstance( statement, Function):
        newrest, newscope = parseInScopes(statement.func_scope, Scope(nest=cur_scope.nestlevel + 1))
        statement.func_scope = newscope
        
    elif isinstance( statement, OpenScope ):
        newrest, newscope = parseInScopes(rest, Scope(nest=cur_scope.nestlevel + 1))
        return parseInScopes(newrest, cur_scope.add_statement(newscope))
    return parseInScopes(rest, cur_scope.add_statement(statement))
 
import re
def Parse(tokenlist : List[Token], function_string : str = None):
    s = parseTokensToStatements(tokenlist, [], None, None, init_functions([], function_string))
    return parseInScopes(s[1], Scope())

def init_functions(function_list : List, function_content : str):
    return list(map( lambda x: (x.group()[6:], lex(function_content, x.start() + len('func_'))[4:]),                                                   \
                   list( re.finditer(r'func_ (\w+)', function_content )))   )                                                    


