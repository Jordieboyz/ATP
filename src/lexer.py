import re
from tokens import Token

def is_number(c : chr):
    return re.compile(r'[0-9]').match(c)
                 
def is_alpha_char( c: chr):
    return re.compile(r'[a-z]|[A-Z]').match(c)

def char_expr( expr : chr):
    return expr in r'={}&+-?/*()[]<>'

def if_expr( expr: str, sidx : int, eidx : int ):
    return re.compile(r'\$eq|\$gt|\$lt|\$get|\$let').match(expr, sidx, eidx)
    
class Lexer:
    def __init__(self, file_content : str):
        self.file_content = file_content
        self.cur_pos = -1
        self.cur_char = None
        self.next_pos()
    
    def next_pos(self):
        self.cur_pos += 1
        if self.cur_pos < len(self.file_content): 
            self.cur_char = self.file_content[self.cur_pos]

    def create_tokens(self):
        tokenlist = []
        tmp = ''
        skip_chars = 0
        
        def add_number_or_var_token(content : str):
            if content: 
                if is_number(content[0]):
                    tokenlist.append(Token("NUMBER", content))
                else:
                    tokenlist.append(Token("VARIABLE", content))

        for idx in range(len(self.file_content)):
            if skip_chars != 0:
                skip_chars -= 1
                self.next_pos()
                continue
                
            if self.cur_char in ' \t\n':
                add_number_or_var_token(tmp)
                tmp = ''
                
            elif self.cur_char == '$':
               add_number_or_var_token(tmp)
               tmp = ''
               expr = if_expr(self.file_content, idx, idx + 4)
               if expr:
                   tokenlist.append(Token("EXPRESSION", expr.group()))
                   skip_chars = len(expr.group())
                    
            elif is_number(self.cur_char):
                tmp += self.cur_char  
            
            elif is_alpha_char(self.cur_char):
                tmp += self.cur_char
                
            elif char_expr(self.cur_char):
                add_number_or_var_token(tmp)
                tmp = ''
                if self.cur_char == '?':
                    tokenlist.append(Token("IF_STATEMENT", self.cur_char))
                else:    
                    tokenlist.append(Token("EXPRESSION", self.cur_char))

            self.next_pos()

        add_number_or_var_token(tmp)
        return tokenlist
            
            
            
            
            
            
            
            
            
            
            
            
            
            