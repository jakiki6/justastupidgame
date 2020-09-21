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
    os.chdir("..")
    os.chdir("..")
    for tile in mod_tiles.get_tiles():
        tile.init(tile(0, 0, 0))
        tiles.append(tile)
    sys.apth = sys.path[:-1]
    print("Loaded from {}".format(moddir))

world = World()

screen = pygame.display.set_mode((640, 480))

r = 0
t = 0
paused = False

textures = {}
textures["paused"] = pygame.image.load("textures/paused.png")

while True:
    if ticks % 40 == 0 and not paused:
        world.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                t = (t + 1) % len(tiles)
            elif event.button == 3:
                world.kill(pygame.mouse.get_pos()[0] // 32, pygame.mouse.get_pos()[1] // 32)
            elif event.button == 4:
                r = (r + 90) % 360
            elif event.button == 5:
                r = (r - 90) % 360
            else:
                if world.exist(pygame.mouse.get_pos()[0] // 32, pygame.mouse.get_pos()[1] // 32):
                    world.get(pygame.mouse.get_pos()[0] // 32, pygame.mouse.get_pos()[1] // 32).kill()
                world.objects.append(tiles[t](pygame.mouse.get_pos()[0] // 32, pygame.mouse.get_pos()[1] // 32, r))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.killAll()
            elif event.key == pygame.K_ESCAPE:
                paused = not paused
    screen.fill((0, 0, 0))
    world.render(screen)
    if paused:
        screen.blit(textures["paused"], (0, 0))
    if 0 <= pygame.mouse.get_pos()[0] // 32 * 32 <= 640 and 0 <= pygame.mouse.get_pos()[1] // 32 * 32 <= 480:
        texture = pygame.transform.rotate(tiles[t].texture, (r + 180) % 360)
        texture.fill((255, 255, 255, 90), None, pygame.BLEND_RGBA_MULT)
        screen.blit(texture, (pygame.mouse.get_pos()[0] // 32 * 32, pygame.mouse.get_pos()[1] // 32 * 32))
    pygame.display.flip()
    clock.tick(60)
    ticks += 1
