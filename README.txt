Welcome to my repo!

This is my (Jort de Boer) ATP repo. 
I chose to "create" my own language.

I don't really have a name for it, but for now I'll call it "symbolic".
The language is Turing complete because it supports function calls, loops, if statements, simple operators like +, -, *, /, % and the assignment operator.
Some of these operators can be combinated, but that is more of a feature.

my language supports:

assigning variables and numbers 
using operators( -, +, *, /, %) 
loops                           
if-statements                   
"return"                        
scoping                         

The code uses:
Classes with inheritance        -> yes (tokens.py, parser.py)
Object-printing for every class -> yes
Type-annotation                 -> yes

3 Higher orde Functions:
Map    -> main.py      ; line 3   and ProgState.py ; line 103 
Filter -> ProgState.py ; line 103
Reduce -> main.py      ; line 13

P.S. the lines ending on '3' is just a coincedence lmao

The code supports 1 file where the code and all the function declaration are in.
Function-params are just passed in the parantheses, like a c++ function.
Function could call other function (recursion supported)
Function result doesn't imediately printed. The whole program needs to end and if it returned somewhere in the middle, after the return, no operations get executed anymore.
You return based on the '.' operator. you call it with the rvalue you like and that gets "printed" at the end of the whole interpret.

Below, you could read all the operators in my language and their syntax.

math-operators:
    myLanguage           synnonym
    
        =         ->        =
            -> a = 3
            -> a = b
            -> a = func(n)
        
        +         ->        +=    
            -> a + 1
            -> a + b
            -> a + func(n)

        -         ->        -=    
            -> a - 1
            -> a - b
            -> a - func(n)
            
        *        ->        *=    
            -> a * 1
            -> a * b
            -> a * func(n)
            
        /         ->        /=    
            -> a / 1
            -> a / b
            -> a / func(n)

if-expressions:

        $eq       ->        ==
        $neq      ->        !=
        $gt       ->        >
        $get      ->        >=
        $lt       ->        < 
        $let      ->        >=

bigger-operations:

    [ <EXPR> ]> (...) <                                   this is the loop-format.      
    
    func_ <NAME>(<PARAMS>) > (...) .<RETURNVALUE> <      this is the format for a function
    
    <EXPR> > (...) <                                     this is the format for an IF-statement
            
all characters and their fucntion:

    =   assign
    +   add
    -   minus
    *   times
    /   divide
    %   modulo
    []  expr for a loop
    ()  function parameter list
    .   return
    $   if-exppression
    <   open a new scope
    >   close a scope
    #   VERY IMPORTANT! this is the actual code and function declaration separator. This needs to stand in betweend these 2 in the same file.
    func_ This indicates the start of a function declaration
    
    

link to explaining: https://youtu.be/fgYMcvStBdg


 
