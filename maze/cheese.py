from ui import graphics


class Cheese():
    def __init__(self, x, y):
        self.x, self.y = x + .5, y + .5
        self.size = 1 / 5

    def draw(self):
        graphics.draw_circle("red", self.x, self.y, self.size)