from mailbox import NotEmptyError
import sys
from pathlib import Path
from PIL import Image, ImageDraw

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
                    self.walls.append((row,col))
                col += 1
            row -= 1

    def output_image(self, path):
        img = Image.new("RGBA", (self.width * 10, (self.height + 1) * 10), "black")
        path_coords = {(s.row, s.col) for s in path}
        draw = ImageDraw.Draw(img)
        for row in range(self.height + 1):
            for col in range(self.width):
                if (row, col) in self.walls:
                    draw.rectangle((col * 10, row * 10, (col + 1) * 10, (row + 1) * 10), fill="black")
                elif (row, col) in path_coords:
                    draw.rectangle((col * 10, row * 10, (col + 1) * 10, (row + 1) * 10), fill="blue")
                else:
                    draw.rectangle((col * 10, row * 10, (col + 1) * 10, (row + 1) * 10), fill="white")
        img.save(f"maze_{self.filename}.png")       


class State:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.col == other.col
    
    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self):
        return f"({self.row}, {self.col})"

class Node:
    def __init__(self, state, maze, parent_node = None) -> None:
        
        self.state = state
        self.parent_node = parent_node
        self.maze = maze
        self.neighbors = []

        row = self.state.row
        col = self.state.col
        
        if (row - 1, col) not in self.maze.walls \
        and (row - 1) >= 0 \
        and (self.parent_node is None or State(row - 1, col) != self.parent_node.state):
            self.neighbors.append(State(row - 1, col))

        if (row + 1, col) not in self.maze.walls \
        and (row + 1) <= self.maze.height \
        and (self.parent_node is None or State(row + 1, col) != self.parent_node.state):
            self.neighbors.append(State(row + 1, col))

        if (row, col + 1) not in self.maze.walls \
        and (col + 1) >= 0 \
        and (self.parent_node is None or State(row, col + 1) != self.parent_node.state):
            self.neighbors.append(State(row, col + 1))

        if (row, col - 1) not in self.maze.walls \
        and (col - 1) >= 0 \
        and (self.parent_node is None or State(row, col - 1) != self.parent_node.state):
            self.neighbors.append(State(row, col - 1))    
        
class Search:
    def __init__(self, maze) -> None:
        self.maze = maze
        
        frontier = [Node(maze.start, maze)]

        explored = set()

        while frontier:
            next_node = frontier.pop()
            explored.add(next_node.state)
            
            
            new_neighbors = next_node.neighbors

            for i in new_neighbors:
                if i not in explored:
                    frontier.append(Node(i, maze, next_node))   

            if next_node.state == maze.goal:
                path = []
                while next_node:
                    path.append(next_node.state)
                    next_node = next_node.parent_node
                path.reverse()
                self.path = path
                print(path)
                return
        
    
m = Maze("maze1.txt")
s =Search(m)
m.output_image(s.path)