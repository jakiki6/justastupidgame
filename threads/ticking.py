from __main__ import *

import time

def run():
    import pygame
    ticks = 0
    clock = pygame.time.Clock()

    while True:
        if state["paused"]:
            time.sleep(0.2)
            continue
        if ticks % 15 == 0:
            world.tick()
        ticks += 1
        clock.tick(60)
