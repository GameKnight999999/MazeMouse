from maze import Maze
from maze.directions import directions
from ui import graphics
from abc import ABC


class Tile(ABC):
    def __init__(self, tile_type: str, row: int, column: int):
        self.tile_type = tile_type
        self.row = row
        self.column = column

    def draw(self):
       pass

    def get_neighb_tile(self, dir_n: int):
        dx, dy = directions[dir_n]
        return Maze.get_tile(self.column + 0.5 + dx, self.row + 0.5 + dy)

    def dist_to_border(self, x: float, y: float, dir_n: int):
        x -= int(x)
        y -= int(y)
        if dir_n == 0:
            return 1 - x
        elif dir_n == 1:
            return y
        elif dir_n == 2:
            return x
        return 1 - y


class Wall_tile(Tile):
    image = graphics.load_image("images/wall.png")

    def __init__(self, row: int, column: int):
        super().__init__("1", row, column)
    
    def draw(self):
        graphics.draw_image(self.image, self.column, self.row)


class Room_tile(Tile):
    def __init__(self, row: int, column: int):
        super().__init__("0", row, column)


class Missing_tile(Tile):
    image = graphics.load_image("images/missing.png")

    def __init__(self, row: int, column: int):
        super().__init__("-1", row, column)
    
    def draw(self):
        graphics.draw_image(self.image, self.column, self.row)