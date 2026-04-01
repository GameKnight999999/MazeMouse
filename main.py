import settings
from maze import Maze
from ui import events
from ui import graphics

running = True
clock = events.Clock()
move = False
mouse_pressed = False

while running:
    for event in events.get_event_queue():
        if event.type == events.QUIT:
           running = False
        
        elif event.type == events.KEYDOWN:
            if event.key == events.K_F3:
                settings.debug = not settings.debug
        
        elif event.type == events.MOUSEBUTTONDOWN:
            if event.button == 1:
                move = False
                mouse_pressed = True
                if settings.debug:
                    tile = Maze.get_tile(*graphics.screen2mazep(*event.pos))
                    print(tile.column, tile.row)
            elif event.button == 3:
                Maze.put_cheese(*graphics.screen2mazep(*event.pos))
        
        elif event.type == events.MOUSEMOTION:
            move = True
            if mouse_pressed:
                settings.view_left_top[0] += graphics.screen2mazes(event.rel[0])
                settings.view_left_top[1] += graphics.screen2mazes(event.rel[1])
        
        elif event.type == events.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pressed = False
                if not move:
                    Maze.add_mouse(*graphics.screen2mazep(*event.pos))
        
        elif event.type == events.MOUSEWHEEL:
            mouse_pos = events.get_mouse_pos()
            pos = graphics.screen2mazep(*mouse_pos)

            settings.tile_size *= 1 + .1 * event.y
            settings.tile_size = max(min(settings.tile_size, settings.MAX_TILE_SIZE), settings.MIN_TILE_SIZE)
            
            pos_new = graphics.screen2mazep(*mouse_pos)
            settings.view_left_top[0] += pos_new[0] - pos[0]
            settings.view_left_top[1] += pos_new[1] - pos[1]

    graphics.fill("black")
    # рисуем лабиринт
    Maze.draw(*graphics.screen2mazep(0, 0), *graphics.screen2mazep(*graphics.screen.get_size()))
    graphics.flip()
    dt = clock.tick() / 1000
    # обновляем весь лабиринт
    Maze.update(dt)
