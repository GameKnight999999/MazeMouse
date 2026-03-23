import settings
from maze.mice import Mouse2
from maze.cheese import Cheese
from maze.tiles import Room_tile, Wall_tile

maze = []
mouse = None
cheese = None
##########################################################
# Грузим карту
with open(settings.map_file) as f:
    map_txt = f.readlines()
# Строим карту из настоящих объектных тайлов
for row, line in enumerate(map_txt):
    maze.append([])
    for column, tile_type in enumerate(line[:-1]):
        if tile_type == "0":
            maze[row].append(Room_tile(row, column))
        else:
            maze[row].append(Wall_tile(row, column))
###########################################################


# Рисуем все: и тайлы и мышей
def draw():
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            maze[row][column].draw()

    if mouse is not None:
        mouse.draw()
    
    if cheese is not None:
        cheese.draw()


# Получаем тайл по координатам лабиринта
def get_tile(x, y):
    if 0 <= y < len(maze) and 0 <= x < len(maze[int(y)]):
        tile_column, tile_row = int(x), int(y)
        return maze[tile_row][tile_column]
    else:
        return None


# двигаем, все что движется
# вызов этой функции постоянно в цикле в main.py
def update(delta_time):
    if mouse is not None:
        mouse.update(delta_time)


def add_mouse(x, y):
    global mouse
    mouse = Mouse2(x, y)


def add_cheese(x, y):
    global cheese
    cheese = Cheese(x, y)