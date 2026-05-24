import sys
from pathlib import Path

class Maze:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.walls = []
   

        filepath = Path(__file__).parent / filename

        with open(filepath, "r", encoding="utf8") as f:
            self.content = f.read().splitlines()

        self.height = len(self.content) -1
        self.width = len(self.content[0])
        row = self.height

        
        for line in self.content:
            col = 0
            for char in line:
                if char == "A":
                    self.start = State(row,col)
                    self.initial_state = self.start
                elif char == "B":
                    self.goal = State(row,col)
                elif char == "#":
                    self.walls.append(State(row,col))
                col += 1
            row -= 1

class State:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

       

class Node:
    def __init__(self, node, parent) -> None:
        self.node = node
        self.parent = parent
        self.neighbors = []
        
    def evaluate_node(self):
        if State(self.row - 1, self.col) not in m.walls \
        and (self.row - 1) > 0:
            self.neighbors.append(State(self.row - 1, self.col))

        if State(self.row + 1, self.col) not in m.walls \
        and (self.row + 1) < self.height:
            self.neighbors.append(State(self.row + 1, self.col))

        if State(self.row, self.col + 1) not in m.walls \
        and (self.col + 1) > 0:
            self.neighbors.append(State(self.row, self.col - 1))
              
        if State(self.row - 1, self.col + 1) not in m.walls \
        and (self.col + 1) > 0:
            self.neighbors.append(State(self.row, self.col + 1))    
        
               
    
m = Maze("maze1.txt")
print(f"Start is ({m.start.row}, {m.start.col})")
print(f"Goal is ({m.goal.row}, {m.goal.col})")
print(m.walls[1].row, m.walls[1].col)
