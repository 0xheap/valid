import random


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {
            'N': True,
            'S': True,
            'E': True,
            'W': True
        }
        self.visited = False

    def has_wall(self, direction):
        return self.walls[direction]

    def remove_wall(self, direction):
        self.walls[direction] = False

    def __repr__(self):
        return f"Cell({self.row}, {self.col})"


class Maze:
    OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    DELTA = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_neighbors(self, cell):
        neighbors = []
        for direction, (dr, dc) in self.DELTA.items():
            nr, nc = cell.row + dr, cell.col + dc
            neighbor = self.get_cell(nr, nc)
            if neighbor is not None:
                neighbors.append((direction, neighbor))
        return neighbors

    def remove_wall_between(self, current, neighbor, direction):
        current.remove_wall(direction)
        neighbor.remove_wall(self.OPPOSITE[direction])

    def generate(self, start_row=0, start_col=0):
        stack = []
        start = self.grid[start_row][start_col]
        start.visited = True
        stack.append(start)

        while stack:
            current = stack[-1]
            unvisited = [
                (d, n) for d, n in self.get_neighbors(current) if not n.visited
            ]
            if unvisited:
                direction, neighbor = random.choice(unvisited)
                self.remove_wall_between(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()

    def display(self):
        output = "+" + "---+" * self.cols + "\n"
        for r in range(self.rows):
            row_str = "|"
            bottom_str = "+"
            for c in range(self.cols):
                cell = self.grid[r][c]
                row_str += "   "
                row_str += "|" if cell.has_wall('E') else " "
                bottom_str += "---+" if cell.has_wall('S') else "   +"
            output += row_str + "\n"
            output += bottom_str + "\n"
        return output

    def __str__(self):
        return self.display()

from collections import *

class Solver:
    def __init__(self, grid, width, height):
        self.grid = grid
        self.entry = (0,0)
        self.exit  = (3,3)
        self.width = width
        self.height = height
        self.visited = []
        self.tree = {self.entry: None}
        self.stack = deque([self.entry])
        self.visited.append(self.entry)
        self.moves = {
            'N': (-1, 0),
            'S': (1, 0),
            'E': (0, 1),
            'W': (0, -1)
        }
    def solver(self):      
        while self.stack:
            x, y = self.stack.popleft()
            if (x, y) == self.exit:
                return self.solution()
            friends = self.get_friends(x, y)
   
            for f in friends:
               if f not in self.visited:
                    self.stack.appendleft(f)
                    self.visited.append(f)
                    self.tree[f] = (x, y)
        return None
                
        
    def get_friends(self, x, y):
        friends = []
        for direction, (mx, my) in self.moves.items():
            nx, ny = x + mx, y + my
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.grid[x][y].has_wall(direction):
                    friends.append((nx, ny))
        return friends
 
    def solution(self):
        tree_ = self.valid_tree()
        path = []
        previous = self.entry
        for current in tree_:
            if current == self.entry:
                continue
            cx, cy = current
            px, py = previous
            for key, (mx, my) in self.moves.items():
                if px + mx == cx and py + my == cy:
                    path.append(key) 
            
            previous = current
            
            
            
            
        return path
    
    def valid_tree(self):
        path = deque()
        target = self.exit
        while target != self.entry:
            path.appendleft(target)
            target = self.tree[target]
        path.appendleft(self.entry)
        return path
    
if __name__ == "__main__":
    rows, cols = 4, 4
    maze = Maze(rows, cols)
    maze.generate()
    bfs = Solver(maze.grid, cols, rows)
    sol = bfs.solver()
    print(sol)
    print(maze)

    # ----- Helpful for your BFS -----
    # Access a cell:          maze.get_cell(row, col)
    # Check a wall:           cell.has_wall('N')  -> True / False
    # Get all neighbors:      maze.get_neighbors(cell) -> [(dir, cell), ...]
    # Can move to neighbor?   not current_cell.has_wall(direction)
