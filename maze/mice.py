from maze import Maze
from maze.directions import directions
from maze.tiles import Wall_tile, Room_tile
from ui import graphics
from abc import ABC, abstractmethod
import random
import settings


class Mouse(ABC):
    def __init__(self, x, y, dir = 0):
        self.x, self.y = x, y
        self.size = 1 / 20 # доля тайла, тайлы 1x1
        self.speed = random.random() * settings.MAX_MOUSE_SPEED # тайлов в секунду
        self.dir = dir


    def draw(self):
        graphics.draw_circle("yellow", self.x, self.y, self.size)


    @abstractmethod
    def update(self, delta_time):
        # Ничего не умеет вообще
        pass


# немного интеллекта
class Mouse2(Mouse):
    def update(self, delta_time):
        cur_tile = Maze.get_tile(self.x, self.y)
        dx, dy = directions[self.dir]
        self.x += dx * self.speed * delta_time
        self.y += dy * self.speed * delta_time
        next_tile = cur_tile.get_neighb_tile(self.dir)
        if cur_tile.dist_to_border(self.x, self.y, self.dir) < 0.2 and (
                next_tile is None or isinstance(next_tile, Wall_tile)):
            self.dir = (self.dir - 1) % 4


class SmartMouse(Mouse):
    def __init__(self, x, y, dir=0):
        super().__init__(x, y, dir)
        self.target = None
        self.path = None
        self.next = Maze.get_tile(self.x, self.y)


    def update(self, delta_time):
        if self.path is None:
            return
        cur_tile = Maze.get_tile(self.x, self.y)
        dx, dy = directions[self.dir]
        self.x += dx * self.speed * delta_time
        self.y += dy * self.speed * delta_time
        if cur_tile == self.next and cur_tile.dist_to_border(self.x, self.y, self.dir) < 0.5:
            if cur_tile.column == self.target[0] and cur_tile.row == self.target[1]:
                self.path = None
                new_cheese = None
                while not isinstance(new_cheese, Room_tile):
                    new_cheese = random.choice(random.choice(Maze.maze))
                Maze.put_cheese(new_cheese.column, new_cheese.row)
            else:
                self.dir = next(self.path, self.dir)
                self.next = cur_tile.get_neighb_tile(self.dir)
    

    def __find_path(self):
        if self.target is None:
            return
        
        visited = set()
        def dfs(tile):
            visited.add(tile)
            if tile.column == self.target[0] and tile.row == self.target[1]:
                return []
            for dir in range(len(directions)):
                next_tile = tile.get_neighb_tile(dir)
                if isinstance(next_tile, Room_tile) and next_tile not in visited:
                    res = dfs(next_tile)
                    if res is not None:
                        res.append(dir)
                        return res
            return None
        
        rev_path = dfs(Maze.get_tile(self.x, self.y))
        if rev_path is None:
            self.path = rev_path
        else:
            self.path = reversed(rev_path)
    

    def goto_cheese(self, x_cheese, y_cheese):
        self.target = (x_cheese, y_cheese)
        self.__find_path()