class Token:
    def __init__(self, type_ : str, content : str):
        self.type_ = type_
        self.content = content
            
    # def __str__(self) -> str:
        # return "{} op line[{}] met index[{}]".format(self.content, self.line, self.idx)
            
    def __str__(self) -> str:
        return "{}('{}:  '{}')".\
            format(type(self).__name__, self.type_, self.content)
            
    def __repr__(self) -> str:
        return self.__str__()
