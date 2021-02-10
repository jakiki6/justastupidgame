from __main__ import *
from utils.dp import *

def run():
    import pygame
    import tile.tile as tile_types

    clock = pygame.time.Clock()
    ticks = 0

    pygame.font.init()
    font = pygame.font.SysFont('Roboto', 16)

    screen = pygame.display.set_mode((640, 480))

    r = 0
    t = 0

    csize = 5

    textures = {}
    textures["paused"] = pygame.image.load("textures/paused.png")
    textures["cleaning"] = pygame.image.load("textures/locked.png")

    mov = [0, 0]
    mov_speed = 5

    mbd = [False, False]
    mto = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    t = (t + 1) % len(tiles)
                elif event.button == 3:
                    mbd[1] = True
                    mto = -1
                elif event.button == 4:
                    r = (r + 90) % 360
                elif event.button == 5:
                    r = (r - 90) % 360
                else:
                    mbd[0] = True
                    mto = -1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button > 5:
                    mbd[0] = False
                elif event.button == 3:
                    mbd[1] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state["cleaning"] = True
                elif event.key == pygame.K_ESCAPE:
                    state["paused"] = not state["paused"]
                elif event.key == pygame.K_w:
                    mov[1] = -mov_speed
                elif event.key == pygame.K_s:
                    mov[1] = mov_speed
                elif event.key == pygame.K_a:
                    mov[0] = -mov_speed
                elif event.key == pygame.K_d:
                    mov[0] = mov_speed
                elif event.key == pygame.K_c:
                    for x in range(get_pos_x() - csize, get_pos_x() + csize):
                        for y in range(get_pos_y() - csize, get_pos_y() + csize):
                            if "rotatable" in tiles[t].tags:
                                world.objects.append(tiles[t](x, y, r))
                            else:
                                world.objects.append(tiles[t](x, y))
                elif event.key == pygame.K_n:
                    t = (t - 1) % len(tiles)
                elif event.key == pygame.K_m:
                    t = (t + 1) % len(tiles)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    mov[1] = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    mov[0] = 0

        if mbd[0] and mto <= 0:
            world.kill_at(*get_pos_xy())
            if "rotatable" in tiles[t].tags:
                world.objects.append(tiles[t](*get_pos_xy(), r))
            else:
                world.objects.append(tiles[t](*get_pos_xy()))
        if mbd[1] and mto <= 0:
            world.kill_at(*get_pos_xy())

        if mto == -1:
            mto = 20
        elif mto > 0:
            mto -= 1

        world.dx += mov[0]
        world.dy += mov[1]

        screen.fill((0, 0, 0))

        dx, dy = get_dp_x(), get_dp_y()

        for x in range(0, 700, 32):
            pygame.draw.line(screen, (25, 25, 25), (x - dx, 0), (x - dx, 480), 1)
        for y in range(0, 500, 32):
            pygame.draw.line(screen, (25, 25, 25), (0, y - dy), (640, y - dy), 1)

        world.render(screen)
        if state["paused"]:
            screen.blit(textures["paused"], (0, 0))
        if 0 <= pygame.mouse.get_pos()[0] // 32 * 32 <= 640 and 0 <= pygame.mouse.get_pos()[1] // 32 * 32 <= 480:
            instance = tiles[t].empty_instance(tiles[t])
            if "rotatable" in instance.tags:
                instance.r = r
            texture = instance.get_texture().copy()
            texture.fill((255, 255, 255, 90), None, pygame.BLEND_RGBA_MULT)
            screen.blit(texture, (get_pos_x() * 32 - world.dx, get_pos_y() * 32 - world.dy))

        screen.blit(font.render(f"FPS: {clock.get_fps() * 10 // 1 / 10}", True, (255, 255, 255)), (0, 18))
        screen.blit(font.render(f"Pos: {world.dx // 32} {world.dy // 32}", True, (255, 255, 255)), (0, 18 + 16))
        screen.blit(font.render(f"Tiles: {len(world.objects)}", True, (255, 255, 255)), (0, 18 + 32))

        if state["cleaning"]:
            screen.blit(textures["cleaning"], (0, 0))
            pygame.display.flip()
            while world.lock:
                time.sleep(0.1)
            world.killAll()
            state["cleaning"] = False

        pygame.display.flip()
        clock.tick(60)
