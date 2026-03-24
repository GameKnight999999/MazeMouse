from maze import Maze
from maze.directions import directions
from maze.tiles import Wall_tile
from maze.tiles import Room_tile
from ui import graphics
from abc import ABC
from abc import abstractmethod
from collections import deque
import random
import settings


class Mouse(ABC):
    def __init__(self, x, y, dir = 0):
        self.x, self.y = x, y
        self.size = 1 / 4 # доля тайла, тайлы 1x1
        self.speed = settings.MIN_MOUSE_SPEED + random.random() * (settings.MAX_MOUSE_SPEED * settings.MIN_MOUSE_SPEED) # тайлов в секунду
        self.dir = dir
    

    @property
    def cur_tile(self):
        return Maze.get_tile(self.x, self.y)


    def draw(self):
        graphics.draw_circle("yellow", self.x, self.y, self.size)


    @abstractmethod
    def update(self, delta_time):
        # Ничего не умеет вообще
        pass


class SmartMouse(Mouse, ABC):
    def __init__(self, x, y, dir=0):
        super().__init__(x, y, dir)
        self.target = None
        self.path = None
        self.next = self.cur_tile


    def update(self, delta_time):
        if self.path is None:
            return
        
        if self.cur_tile == self.next and self.cur_tile.dist_to_border(self.x, self.y, self.dir) < 0.5:
            if self.cur_tile.column == self.target[0] and self.cur_tile.row == self.target[1]:
                self.path = None
                new_cheese = None
                while not isinstance(new_cheese, Room_tile):
                    new_cheese = random.choice(random.choice(Maze.maze))
                Maze.put_cheese(new_cheese.column, new_cheese.row)
            else:
                self.dir = next(self.path, self.dir)
                self.next = self.cur_tile.get_neighb_tile(self.dir)
        
        dx, dy = directions[self.dir]
        self.x += dx * self.speed * delta_time
        self.y += dy * self.speed * delta_time
    

    @abstractmethod
    def find_path(self):
        pass


    def goto_cheese(self, x_cheese, y_cheese):
        self.target = (x_cheese, y_cheese)
        self.next = self.cur_tile
        self.find_path()


# немного интеллекта
class Mouse2(Mouse):
    def update(self, delta_time):
        dx, dy = directions[self.dir]
        self.x += dx * self.speed * delta_time
        self.y += dy * self.speed * delta_time
        next_tile = self.cur_tile.get_neighb_tile(self.dir)
        if self.cur_tile.dist_to_border(self.x, self.y, self.dir) < 0.2 and (
                next_tile is None or isinstance(next_tile, Wall_tile)):
            self.dir = (self.dir - 1) % 4


class DFSMouse(SmartMouse):
    def find_path(self):
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
        
        rev_path = dfs(self.cur_tile)
        if rev_path is None:
            self.path = rev_path
        else:
            self.path = reversed(rev_path)


class BFSMouse(SmartMouse):
    def find_path(self):
        if self.target is None:
            return
        
        queue = deque()
        visited = set()
        queue.append((self.cur_tile, []))
        while queue:
            tile, path = queue.popleft()
            visited.add(tile)

            if tile.column == self.target[0] and tile.row == self.target[1]:
                self.path = iter(path)
                return
            
            for dir in range(len(directions)):
                newtile = tile.get_neighb_tile(dir)
                if isinstance(newtile, Room_tile) and newtile not in visited:
                    queue.append((newtile, path + [dir]))
