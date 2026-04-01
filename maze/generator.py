from maze import Maze
from maze.tiles import Room_tile
from maze.tiles import Wall_tile
from maze.directions import directions


Cell = tuple[int, int]


class Set:
    def __init__(self):
        self.next = self
    

    def __add__(self, other: "Set"):
        self.next = other
        return other
    

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Set):
            return False
        
        if self is value:
            return True
        if self.next is self and value.next is value:
            return False
        return self.next == value.next
    

    def __ne__(self, value: object) -> bool:
        return not self == value


def gen(x1: int, y1: int, x2: int, y2: int):
    for column in range(x1, x2):
        for row in range(y1, y2):
            if (column, row) not in Maze.maze:
                neighbours = list(set(sets.get((column + dir[0], row + dir[1]), Set()) for dir in directions))
                if len(neighbours) == 4:
                    Maze.maze[(column, row)] = Room_tile(row, column)
                    _ = neighbours[0] + neighbours[1] + neighbours[2] + neighbours[3]
                else:
                    Maze.maze[(column, row)] = Wall_tile(row, column)


sets: dict[Cell, Set] = dict()