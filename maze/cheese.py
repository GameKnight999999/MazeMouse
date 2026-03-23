from ui import graphics
from maze.mice import Mouse


class Cheese(Mouse):
    def __init__(self, x, y):
        super().__init__(x, y)