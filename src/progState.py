from typing import List

class ProgramState:
    def __init__(self, name : str, cells : List[int]):
        self.name = name
        self.cells = cells
        self.currentCell = 0
        
    def __str__(self) -> str:
        return "{} (cells: {} )".format(self.name, self.cells)

    def __repr__(self) -> str:
        return self.__str__()

    def write_register(self, data : int ):
        self.cells[self.currentCell] = data
    
    def output_register(self):
        print(self.cells[self.currentCell])
    
    def increment_currentCell(self):
        self.currentCell += 1
    
    def decrement_currentCell(self):
        self.currentCell -= 1
        
    def clear(self):
        self.cells[0] = 0
        self.cells[1] = 0
    
    