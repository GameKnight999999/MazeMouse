import settings
from maze.mice import BFSMouse
from maze.mice import SmartMouse
from maze.cheese import Cheese
from maze.tiles import Room_tile, Wall_tile
from maze.tiles import Tile

maze = dict()
sets = dict()
mice = []
cheese = None

size = (len(maze), len(maze[0]))

# Рисуем все: и тайлы и мышей
def draw():
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            maze[row][column].draw()

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