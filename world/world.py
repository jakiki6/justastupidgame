from utils import utils
import pygame

class World(object):
    def __init__(self, objects=[]):
        self.objects = objects
    def tick(self):
        for object in self.objects:
            object.tick(self)
    def render(self, screen):
        for object in self.objects:
            texture = pygame.transform.rotate(object.texture, object.r)
            screen.blit(texture, (object.x * 64, object.y * 64))
