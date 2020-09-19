from utils import utils
import pygame

class World(object):
    def __init__(self, objects=[]):
        self.objects = objects
    def tick(self):
        for object in self.objects:
            object.tick(self)
            if not object.alive:
                self.objects.remove(object)
    def render(self, screen):
        for object in self.objects:
            texture = pygame.transform.rotate(object.texture, (object.r + 180) % 360)
            screen.blit(texture, (object.x * 32, object.y * 32))
    def isColliding(self, x, y):
        for object in self.objects:
            if object.x == x and object.y == y:
                return True
        return False
