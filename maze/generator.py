from maze import Maze
from maze.tiles import Room_tile
from maze.tiles import Wall_tile
import random


class Set:
    def __init__(self) -> None:
        self.next = self
    

    def __add__(self, other):
        self.next = other
    

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Set):
            return False
        
        if self is value:
            return True
        if self.next is self and value.next is value:
            return False
        return self.next == value.next


def cell2wall(x):
    return (x + 1) // 2


def wall2cell(x):
    return x * 2


def gen_sets(x1, y1, x2, y2):
    
    sets = dict()

    for column in range(x1, x2):
        for row in range(y1, y2):
            sets[(column, row)] = Set()
    
    return sets


def gen_walls(x1, y1, x2, y2):
    
    walls = []

    # Generating inner walls of an area
    for column in range(x1, x2):
        for row in range(y1, y2):
            if column > x1:
                walls.append(((column - 1, row), (column, row)))
            if row > y1:
                walls.append(((column, row - 1), (column, row)))
    
    # Checking for outer walls in the border cells
    for column in range(x1, x2):
        if (column, y1 - 1) in Maze.maze:
            walls.append(((column, y1 - 1), (column, y1)))
        if (column, y2 + 1) in Maze.maze:
            walls.append(((column, y2), (column, y2 + 1)))
    for row in range(y1, y2):
        if (x1 - 1, row) in Maze.maze:
            walls.append(((x1 - 1, row), (x1, row)))
        if (x2 + 1, row) in Maze.maze:
            walls.append(((x2, row), (x2 + 1, row)))
    
    return walls


def gen(x1, y1, x2, y2):
    
    wall_x1, wall_x2, wall_y1, wall_y2 = cell2wall(x1), cell2wall(y1), cell2wall(x2), cell2wall(y2)
    sets = gen_sets(wall_x1, wall_y1, wall_x2, wall_y2)
    walls = gen_walls(wall_x1, wall_y1, wall_x2, wall_y2)
    random.shuffle(walls)

    # Generating default cell preset
    for column in range(x1, x2):
        for row in range(y1, y2):
            if column % 2 or row % 2:
                Maze.maze[(column, row)] = Wall_tile(row, column)
            else:
                Maze.maze[(column, row)] = Room_tile(row, column)
    
    # Running Kruskal's algorythm
    for wall in walls:
        if sets[wall[0]] != sets[wall[1]]:
            column = (wall2cell(wall[0][0]) + wall2cell(wall[1][0])) // 2
            row = (wall2cell(wall[0][1]) + wall2cell(wall[1][1])) // 2
            Maze.maze[(column, row)] = Room_tile(row, column)
            _ = sets[wall[0]] + sets[wall[1]]