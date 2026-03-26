import pygame

import settings
from ui import screen

Image = pygame.Surface
Color = pygame.Color | str | tuple[int, int, int]
flip = pygame.display.flip


def fill(color: Color):
    screen.fill(color)


# принимает размеры картинки в координатах лабиринта
def load_image(path: str):
    return pygame.image.load(path)


# клиенты будут передавать координаты лабиринта
def draw_image(image: Image, x: float, y: float, size: tuple[float, float] =(1, 1)):
    x, y = maze2screenp(x, y)
    size = maze2screens(size[0]), maze2screens(size[1])
    screen.blit(pygame.transform.scale(image, size), (x, y))


# клиенты будут передавать координаты лабиринта
def draw_circle(color: Color, x: float, y: float, r: float):
    x, y = maze2screenp(x, y)
    pygame.draw.circle(screen, color, (x, y), r * settings.tile_size)


def screen2mazep(x: float, y: float):
    return x / settings.tile_size - settings.view_left_top[0], \
           y / settings.tile_size - settings.view_left_top[1]


def maze2screenp(x: float, y: float):
    return (x + settings.view_left_top[0]) * settings.tile_size, \
           (y + settings.view_left_top[1]) * settings.tile_size


def screen2mazes(s: float):
    return s / settings.tile_size


def maze2screens(s: float):
    return s * settings.tile_size
