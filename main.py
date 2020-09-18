import pygame, os, sys, time
from world.world import World

clock = pygame.time.Clock()
ticks = 0

tiles = []

for moddir in [f.path for f in os.scandir("mods") if f.is_dir()]:
    sys.path.append(os.path.abspath(moddir))
    os.chdir(moddir)
    mod = __import__("mod")
    mod_tiles = __import__("tiles")
    for tile in mod_tiles.get_tiles():
        tiles.append(tile)
    os.chdir("..")
    os.chdir("..")
    del(sys.path[-1])
    print("Loaded from {}".format(moddir))

world = World([tiles[1](0, 0, 90), tiles[0](5, 0, 270)])

screen = pygame.display.set_mode((640, 480))

while True:
    if ticks % 40 == 0:
        world.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    screen.fill((0, 0, 0))
    world.render(screen)
    pygame.display.flip()
    clock.tick(60)
    ticks += 1
