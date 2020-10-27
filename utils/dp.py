import pygame

from __main__ import world

def get_pos_x():
    return (pygame.mouse.get_pos()[0] + world.dx) // 32
def get_pos_y():
    return (pygame.mouse.get_pos()[1] + world.dy) // 32

def get_pos_xy():
    return (get_pos_x(), get_pos_y())

def get_dp_x():
    return world.dx % 32
def get_dp_y():
    return world.dy % 32
