from watchdog.watchdog import Watchdog
watchdog = Watchdog()
watchdog.start()

import pygame, os, sys, time
from world.world import World
import tile.tile as tile_types


clock = pygame.time.Clock()
ticks = 0

tiles = []

for moddir in [f.path for f in os.scandir("mods") if f.is_dir()]:
    sys.path.append(os.path.abspath(moddir))
    os.chdir(moddir)
    mod = __import__("mod")
    mod_tiles = __import__("tiles")
    os.chdir("..")
    os.chdir("..")
    for tile in mod_tiles.get_tiles():
        tile.init(tile)
        tiles.append(tile)
    sys.apth = sys.path[:-1]
    print("Loaded from {}".format(moddir))

world = World()
from utils.dp import *


screen = pygame.display.set_mode((640, 480))

r = 0
t = 0
paused = False

textures = {}
textures["paused"] = pygame.image.load("textures/paused.png")

mov = [0, 0]
mov_speed = 5

while True:
    if ticks % 15 == 0:
        if not paused:
            world.tick()
        watchdog.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                t = (t + 1) % len(tiles)
            elif event.button == 3:
                world.kill(*get_pos_xy())
            elif event.button == 4:
                r = (r + 90) % 360
            elif event.button == 5:
                r = (r - 90) % 360
            else:
                if world.exist(*get_pos_xy()):
                    world.get(*get_pos_xy()).kill()
                if "rotateable" in tiles[t].tags:
                    world.objects.append(tiles[t](*get_pos_xy(), r))
                else:
                    world.objects.append(tiles[t](*get_pos_xy()))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.killAll()
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_w:
                mov[1] = -mov_speed
            elif event.key == pygame.K_s:
                mov[1] = mov_speed
            elif event.key == pygame.K_a:
                mov[0] = -mov_speed
            elif event.key == pygame.K_d:
                mov[0] = mov_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                mov[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                mov[0] = 0

    world.dx += mov[0]
    world.dy += mov[1]

    screen.fill((0, 0, 0))
    world.render(screen)
    if paused:
        screen.blit(textures["paused"], (0, 0))
    if 0 <= pygame.mouse.get_pos()[0] // 32 * 32 <= 640 and 0 <= pygame.mouse.get_pos()[1] // 32 * 32 <= 480:
        instance = tiles[t].empty_instance(tiles[t])
        if "rotateable" in instance.tags:
            instance.r = r
        texture = instance.get_texture().copy()
        texture.fill((255, 255, 255, 90), None, pygame.BLEND_RGBA_MULT)
        screen.blit(texture, (get_pos_x() * 32 - world.dx, get_pos_y() * 32 - world.dy))
    pygame.display.flip()
    clock.tick(60)
    ticks += 1
