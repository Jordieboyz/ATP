from typing import List
from lexer import lex
from tokens import Token, Func, Number, Variable, Is, ExprIfStatement, \
                   CloseFuncParam, OpenFuncParam, \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, EndExprLoop, Return
    
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


# These 2 functions append or remove an item frmo the list. I would have done this inline IF the "append" or "remove" function
# returned itself. Unfortunately, they don't so I have to do this myself. It is kinda tricky, cause these operations always return None,
# whether it worked or not, but assuming I put the right values in these lambda functions, I'll be okay
append = lambda l, x: l if l.append(x) is None else l
remove = lambda l, x: l if l.remove(x) is None else l
    

# This function is the first step of parsing in my program.
# The function creates a List[Statement] out of a List[Token]. Statements are combined Token(s)

# parseTokensToStatements :: List[Token] -> List[Statement] -> Token -> Statement -> List[String, List[Token]] -> List[Statement]
def parseTokensToStatements(tokenlist : List[Token], statementlist : List[Statement], last_token : Token, cur_statement : Statement):
    if not tokenlist:
        return None, statementlist

    token, *rest = tokenlist
    
    # This part of the function adds fucntion parameters to a certain function and and if the current 
    # token is a Token::CloseFunParam, the completed fucntion gets added to the List[Statement] or to the Statement::Mathstatement if it needs an rvalue
    if cur_statement is not None:
        if isinstance(cur_statement, Function) and isinstance( last_token, OpenFuncParam):
            if not isinstance(token, CloseFuncParam): 
                cur_statement.func_params.append(token)
                return parseTokensToStatements(rest, statementlist, last_token, cur_statement)
            else:
                # cur_statement.func_params = parseTokensToStatements(cur_statement.func_params, [], None, cur_statement, None)[1]
                
            #     tokens = list(filter(None, map( lambda x, y: x[1] if x[0] == y else None , func_list, [cur_statement.funcname]*len(func_list))))
            #     if tokens:
            #         cur_statement.func_scope = parseTokensToStatements(tokens[0], [], None, None, func_list)[1]
    
                if isinstance( statementlist[-1], (MathStatement, IfStatement, ReturnFunc)):
                    if statementlist[-1].rvalue is None:
                        statementlist[-1].rvalue = cur_statement
                        return parseTokensToStatements(rest, statementlist, token, None)
                return parseTokensToStatements(rest, append(statementlist, cur_statement), token, None)
  
    
  # Add the current Token::Variable or Token::Number to whatever the Statement::cur_statement is
    if isinstance( token, (Variable, Number)):
        if isinstance( cur_statement, (IfStatement, MathStatement, ReturnFunc)):
            if cur_statement.rvalue is None:
                cur_statement.rvalue = token
                return parseTokensToStatements(rest, statementlist, token, None)
        
   
    # The rest of this function is all the same but in different formats. Based on the current token, the corresponding 
    # value of the key in the st_dict wil get called and added to the List[Statement]
    elif isinstance(token, EndExprLoop):
        if isinstance( statementlist[-1], IfStatement) and isinstance(statementlist[-2], ConditionsLoop):
            statementlist[-2].expr = statementlist[-1]
            del statementlist[-1]        
        
    elif isinstance( token, (Is, Add, Minus, Times, Divide, Modulo, ExprIfStatement) ):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)](last_token, token, None)), token, statementlist[-1])
    
    elif isinstance(token, (StartExprLoop, OpenLoop, CloseLoop)):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, None)
    
    elif isinstance(token, Return):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, statementlist[-1])
    
    elif isinstance(token, OpenFuncParam):
        if isinstance(last_token, Func):
            return parseTokensToStatements(rest, statementlist, token, st_dict[type(last_token)](last_token.content))
        
    return parseTokensToStatements(rest, statementlist, token, cur_statement) 


# This function is the second part of my Parse proces. In this function, The different "scopes" will be created.
# f.e. a loop, a function scope or just te scope for an if statement.
# parseInScopes :: List[Statement] -> Scope -> List[Statement]
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
 
# Parse :: List[Token] -> String -> List[Statement]
def Parse(tokenlist : List[Token]):
    return parseInScopes(parseTokensToStatements(tokenlist, [], None, None)[1], Scope())

                                                   


