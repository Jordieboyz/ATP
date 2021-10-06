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
    'eq' : '==',
    'neq' : '!=',
    'gt' : '>',
    'get' : '>=',
    'lt' : '<',
    'let' : '<=',
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
                        exec(make_exec('self.cells[name.content]', exec_dict[type(operator)] , 'int(value.content)'))
                        
                elif isinstance(value, Variable):
                    if value.content in self.cells:
                        if isinstance( operator, Is ):
                            self.cells[name.content] = self.cells[value.content]
                        elif name.content in self.cells:
                            exec(make_exec('self.cells[name.content]', exec_dict[type(operator)] , 'self.cells[value.content]'))

                        
    def evaluate_expr(self, expr):
        if not self.returned:
            if isinstance(expr, ConditionsLoop):
                if isinstance(expr.expr.lvalue, Variable):
                    if expr.expr.lvalue.content in self.cells:
                        if isinstance( expr.expr.rvalue, Number ):
                            if expr.expr.operator.expr == 'gt':
                                return self.cells[expr.expr.lvalue.content] > int(expr.expr.rvalue.content)
                            if expr.expr.operator.expr == 'lt':
                                return self.cells[expr.expr.lvalue.content] < int(expr.expr.rvalue.content)
                            if expr.expr.operator.expr == 'eq':
                                return self.cells[expr.expr.lvalue.content] == int(expr.expr.rvalue.content)
                            if expr.expr.operator.expr == 'neq':
                                return self.cells[expr.expr.lvalue.content] != int(expr.expr.rvalue.content)
                            if expr.expr.operator.expr == 'get':
                                return self.cells[expr.expr.lvalue.content] >= int(expr.expr.rvalue.content)
                            if expr.expr.operator.expr == 'let':
                                return self.cells[expr.expr.lvalue.content] <= int(expr.expr.rvalue.content)
            # else:
            elif isinstance(expr.lvalue, Variable):
                if expr.lvalue.content in self.cells:
                    if isinstance( expr.rvalue, Number ):
                        if expr.operator.expr == 'gt':
                            return self.cells[expr.lvalue.content] > int(expr.rvalue.content)
                        if expr.operator.expr == 'lt':
                            return self.cells[expr.lvalue.content] < int(expr.rvalue.content)
                        if expr.operator.expr == 'eq':
                            return self.cells[expr.lvalue.content] == int(expr.rvalue.content)
                        if expr.operator.expr == 'neq':
                            return self.cells[expr.lvalue.content] != int(expr.rvalue.content)
                        if expr.operator.expr == 'get':
                            return self.cells[expr.lvalue.content] >= int(expr.rvalue.content)
                        if expr.operator.expr == 'let':
                            return self.cells[expr.lvalue.content] <= int(expr.rvalue.content)
                    
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

# def runScope( scope)
def runCode(code, ptr : int, state : ProgramState,  output):
    if(ptr >= len(code.statements)):
        return state, output
    
    cur = code.statements[ptr]
    state.codePtr = ptr
    
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
        if state.evaluate_expr( cur ) :
            state.cur_loop = cur
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

















    # 
    
    