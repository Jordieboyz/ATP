from typing import List
from Parser import MathStatement
from tokens import Is, Number, Variable, Add, Minus ,Times, Divide, Modulo
from Parser import ConditionsLoop, IfStatement, Scope, ReturnFunc

exec_dict = {
    Add : "+=",
    Minus : "-=",
    Times : "*=",
    Divide : "/=",
    Modulo : "%",
    'eq' : lambda l, r: l == r ,
    'neq' : lambda l, r: l != r,
    'gt' : lambda l, r: l > r,
    'get' : lambda l, r: l >= r,
    'lt' : lambda l, r: l < r,
    'let' : lambda l, r: l <= r,
}



class ProgramState:
    def __init__(self):
        self.cells = dict()
        self.cur_loop = None
        self.last_statement = None
        self.returned = False
        
    def __str__(self) -> str:
        return self.cells.__str__()

    def __repr__(self) -> str:
        return self.__str__()
    
    def op_on_var(self, name : str, operator, value : int):
        make_exec = lambda l, o, r: l.__str__() + o.__str__() + r.__str__()
        
        if name and isinstance( name, Variable):
            if not self.returned:
                if isinstance( value, Number ):
                    if isinstance( operator, Is):
                        self.cells[name.content] = int(value.content)
                    elif name.content in self.cells:
                        if type(operator) in exec_dict: 
                            exec(make_exec('self.cells[name.content]', exec_dict[type(operator)] , 'int(value.content)'))
                        
                elif isinstance(value, Variable):
                    if value.content in self.cells:
                        if isinstance( operator, Is ):
                            self.cells[name.content] = self.cells[value.content]
                        elif name.content in self.cells:
                            if type(operator) in exec_dict:
                                exec(make_exec('self.cells[name.content]', exec_dict[type(operator)] , 'self.cells[value.content]'))

    def evaluate_expr(self, expr):
        if not self.returned:
            if isinstance(expr.lvalue, Variable):
                if expr.lvalue.content in self.cells:
                    if isinstance( expr.rvalue, Number ):
                        if expr.operator.expr in exec_dict:
                            return exec_dict[expr.operator.expr](self.cells[expr.lvalue.content], int(expr.rvalue.content))


# def evaluate_if(state,)

                    
def runLoop( scope, state : ProgramState, output ):
    print(state)
    if state.cur_loop is not None:
        if not state.evaluate_expr(state.cur_loop) or output is not None:
            return state, output
        else:
            state_, output_ = runCode(scope, 0, state, output)
            return runLoop(scope, state_, output_)
        
def runScope( scope, state : ProgramState, output ):
    print(state)
    if state.last_statement is not None:
        if not state.evaluate_expr(state.last_statement) or output is not None:
            return state, output
        else:
            return runCode(scope, 0, state, output)

def runCode(code, ptr : int, state : ProgramState,  output):
    if(ptr >= len(code.statements)):
        return state, output
    
    cur = code.statements[ptr]
    
    # print("\ncur ptr: ", ptr, end='\n')
    # for i in range(len(code.statements)):
    #     print(i,".  ", code.statements[i], end='\n')
    print(state)
    if isinstance( cur, MathStatement):
        state.op_on_var(cur.lvalue, cur.operator, cur.rvalue)
        return runCode( code, ptr + 1, state, output)
    
    elif isinstance( cur, ReturnFunc):
        if isinstance(cur.rvalue, Number):
            state.returned = True
            return runCode(code, ptr + 1, state, int(cur.rvalue.content))
        elif isinstance(cur.rvalue, Variable):
            state.returned = True
            return runCode(code, ptr + 1, state, state.cells[cur.rvalue.content])
        
    elif isinstance( cur, IfStatement):
        if state.evaluate_expr( cur ) :
            state.last_statement = cur
            return runCode(code, ptr + 1, state, output)
        else:
            return runCode(code, ptr + 2, state, output)

    elif isinstance( cur, ConditionsLoop):
        if state.evaluate_expr( cur.expr ) :
            state.cur_loop = cur.expr
            return runCode(code , ptr + 1, state, output)
        else:
            return runCode(code, ptr + 2, state, output)
    
    elif isinstance( cur, Scope):
        # print("old_state: ", state, "\after: ", cur)
        if isinstance( code.statements[ptr - 1], IfStatement):
            state_, output_ = runScope(cur, state, None)
            return runCode(code, ptr + 1, state_, output_)
        elif isinstance( code.statements[ptr -1], ConditionsLoop):
            state_, output_ = runLoop(cur, state, None)
            return runCode(code, ptr + 1, state_, output_)
        # print("new_state: ", state_, "\ncontinue: ", code.statements[ptr])
  
    else:    
        return runCode(code, ptr + 1, state, output)







import re
def init_functions(function_list : List, function_content : str):
    return list(map( lambda x: (x.group()[6:], lex(function_content, x.start() + len('func_'))[4:]),    \
                   list( re.finditer(r'func_ (\w+)', function_content )))) 









    # 
    
    