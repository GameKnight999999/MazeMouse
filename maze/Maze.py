import settings
from math import floor
from maze.mice import BFSMouse
from maze.mice import SmartMouse
from maze.mice import Mouse
from maze.mice import Mouse2
from maze.cheese import Cheese
from maze.tiles import Tile
from maze.tiles import Missing_tile
from maze.generator import gen
import random

maze: dict[tuple[int, int], Tile] = dict()
mice: list[Mouse] = []
cheese = None


def draw(x1: float, y1: float, x2: float, y2: float):
    x1, y1 = floor(x1) - settings.MARGIN, floor(y1) - settings.MARGIN
    x2, y2 = floor(x2) + settings.MARGIN, floor(y2) + settings.MARGIN
    gen(x1, y1, x2 + 1, y2 + 1)
    for column in range(x1, x2 + 1):
        for row in range(y1, y2 + 1):
            tile = maze.get((column, row), Missing_tile(row, column))
            tile.draw()

    for mouse in mice:
        mouse.draw()
    
    if cheese is not None:
        cheese.draw()


def get_tile(x: float, y: float):
    return maze.get((floor(x), floor(y)), Missing_tile(int(y), int(x)))


def update(delta_time: float):
    for mouse in mice:
        mouse.update(delta_time)


def add_mouse(x: float, y: float):
    global mice
    if random.random() < .2:
        mice.append(Mouse2(x, y))
    mice.append(BFSMouse(x, y))


def put_cheese(x: float, y: float):
    global cheese
    x, y = floor(x), floor(y)
    cheese = Cheese(x, y)
    for mouse in mice:
        if isinstance(mouse, SmartMouse):
            mouse.goto_cheese(x, y)