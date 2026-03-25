import settings
from maze.mice import BFSMouse
from maze.mice import SmartMouse
from maze.cheese import Cheese
from maze.tiles import Room_tile
from maze.tiles import Wall_tile
from maze.tiles import Tile
from maze.tiles import Missing_tile
from maze.generator import gen

maze = dict()
sets = dict()
mice = []
cheese = None


# Рисуем все: и тайлы и мышей
def draw(x1, y1, x2, y2):
    x1, y1 = int(x1) - settings.MARGIN, int(y1) - settings.MARGIN
    x2, y2 = int(x2) + settings.MARGIN, int(y2) + settings.MARGIN
    gen(x1, y1, x2 + 1, y2 + 1)
    for column in range(x1, x2 + 1):
        for row in range(y1, y2 + 1):
            tile = maze.get((column, row), Missing_tile(row, column))
            tile.draw()

    for mouse in mice:
        mouse.draw()
    
    if cheese is not None:
        cheese.draw()


# Получаем тайл по координатам лабиринта
def get_tile(x: float, y: float):
    return maze.get((int(x), int(y)), Missing_tile(int(y), int(x)))


# двигаем, все что движется
# вызов этой функции постоянно в цикле в main.py
def update(delta_time: float):
    for mouse in mice:
        mouse.update(delta_time)


def add_mouse(x: float, y: float):
    global mice
    mice.append(BFSMouse(x, y))


def put_cheese(x: float, y: float):
    global cheese
    x, y = int(x), int(y)
    cheese = Cheese(x, y)
    for mouse in mice:
        mouse.goto_cheese(x, y)