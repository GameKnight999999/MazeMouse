import settings
from maze import Maze
from maze.tiles import Room_tile
from maze.tiles import Wall_tile


def gen_sets(x1, y1, x2, y2):
    for column in range(x1, x2):
        for row in range(y1, y2):
            Maze.sets[(column, row)] = (column, row)


def gen(x1, y1, x2, y2):
    
    gen_sets((x1 + 1) // 2, (y1 + 1) // 2, (x2 + 1) // 2, (y2 + 1) // 2)

    for column in range(x1, x2):
        for row in range(y1, y2):
            if column % 2 or row % 2:
                Maze.maze[(column, row)] = Wall_tile(row, column)
            else:
                Maze.maze[(column, row)] = Room_tile(row, column)