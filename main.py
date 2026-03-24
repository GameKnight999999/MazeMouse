import settings
from maze import Maze
from ui import events
from ui import graphics

FPS = 60
running = True
clock = events.Clock()

while running:
    for event in events.get_event_queue():
        if event.type == events.QUIT:
           running = False
        elif event.type == events.MOUSEBUTTONDOWN:
            if event.button == 1:
                Maze.add_mouse(*graphics.screen2mazep(*event.pos))
            elif event.button == 3:
                Maze.put_cheese(*graphics.screen2mazep(*event.pos))
        
    
    pressed = events.get_pressed()
    if pressed[events.K_RIGHT]:
        settings.view_left_top[0] -= settings.CAM_SPEED
    if pressed[events.K_LEFT]:
        settings.view_left_top[0] += settings.CAM_SPEED
    if pressed[events.K_DOWN]:
        settings.view_left_top[1] -= settings.CAM_SPEED
    if pressed[events.K_UP]:
        settings.view_left_top[1] += settings.CAM_SPEED
    settings.view_left_top[0] = min(max(settings.view_left_top[0], graphics.screen.get_width() - graphics.maze2screens(Maze.size[0])), 0)
    settings.view_left_top[1] = min(max(settings.view_left_top[1], graphics.screen.get_height() - graphics.maze2screens(Maze.size[1])), 0)

    graphics.fill("black")
    # рисуем лабиринт
    Maze.draw()
    graphics.flip()
    clock.tick(FPS)
    # обновляем весь лабиринт
    Maze.update(1 / FPS)
