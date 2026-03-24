import pygame
from pygame.constants import * # pyright: ignore[reportWildcardImportFromLibrary]

Clock = pygame.time.Clock

Event = pygame.event.EventType
get_event_queue = pygame.event.get

get_mouse_pos = pygame.mouse.get_pos