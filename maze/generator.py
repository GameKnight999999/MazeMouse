from maze import Maze
from maze.tiles import Room_tile
from maze.tiles import Wall_tile
from maze.directions import directions
import random


Cell = tuple[int, int]


class Set:
    @property
    def top(self) -> "Set":
        if self.next is self:
            return self
        return self.next.top


    def __init__(self):
        self.next = self
    

    def __add__(self, other: "Set"):
        self.top.next = other
    

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Set):
            return False
        
        return self.top is value.top
    

    def __ne__(self, value: object) -> bool:
        return not self == value


def cell2wall(x: int):
    return (x + 1) // 2


def wall2cell(x: int):
    return x * 2


def gen_cells(x1: int, y1: int, x2: int, y2: int):
    
    cells: list[Cell] = []

    for column in range(x1, x2):
        for row in range(y1, y2):
            if (column, row) not in sets:
                sets[(column, row)] = Set()
                cells.append((column, row))
    
    return cells


def gen_walls(cells: list[Cell]):
    
    walls: list[tuple[Cell, Cell]] = []

    for cell in cells:
        for dir in directions:
            if (cell[0] + dir[0], cell[1] + dir[1]) in sets:
                wall = (cell, (cell[0] + dir[0], cell[1] + dir[1]))
                if wall not in walls and wall[::-1] not in walls:
                    walls.append(wall)
    
    return walls


def gen(x1: int, y1: int, x2: int, y2: int):
    
    wall_x1, wall_y1, wall_x2, wall_y2 = cell2wall(x1), cell2wall(y1), cell2wall(x2), cell2wall(y2)
    cells = gen_cells(wall_x1, wall_y1, wall_x2, wall_y2)
    walls = gen_walls(cells)
    random.shuffle(walls)

    # Generating default cell preset
    for cell in cells:
        column, row = wall2cell(cell[0]), wall2cell(cell[1])
        Maze.maze[(column, row)] = Room_tile(row, column)
        Maze.maze[(column - 1, row - 1)] = Wall_tile(row - 1, column - 1)
    
    # Running Kruskal's algorythm
    for wall in walls:
        column = (wall2cell(wall[0][0]) + wall2cell(wall[1][0])) // 2
        row = (wall2cell(wall[0][1]) + wall2cell(wall[1][1])) // 2
        if sets[wall[0]] != sets[wall[1]]:
            Maze.maze[(column, row)] = Room_tile(row, column)
            _ = sets[wall[0]] + sets[wall[1]]
        else:
            Maze.maze[(column, row)] = Wall_tile(row, column)


sets: dict[Cell, Set] = dict()