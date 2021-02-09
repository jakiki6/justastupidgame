from utils import utils
import pygame

class World(object):
    def __init__(self, objects=[], dx=0, dy=0):
        self.objects = objects
        self.dx, self.dy = dx, dy
        self.lock = False
    def tick(self):
        self.lock = True
        self.sort()
        for object in self.objects:
            if object.should_tick:
                object.tick(self)
            else:
                object.should_tick = True
            if not object.alive:
                self.objects.remove(object)
        for object in self.objects:
            object.apply()
        self.lock = False
    def render(self, screen):
        for object in self.objects:
            if not object.alive:
                continue
            texture = object.get_texture()
            screen.blit(texture, (object.x * 32 - self.dx, object.y * 32 - self.dy))
    def isColliding(self, x, y):
        for object in self.objects:
            if object.x == x and object.y == y and "solid" in object.tags:
                return True
        return False
    def kill(self, x, y):
        for object in self.objects:
            if object.x == x and object.y == y:
                object.kill()
                self.objects.remove(object)
    def killAll(self):
        for object in self.objects:
            object.kill()
        self.objects.clear()
    def exist(self, x, y):
        return self.get(x, y) != None
    def get(self, x, y):
        for object in self.objects:
            if object.x == x and object.y == y:
                return object
        return None
    def kill_at(self, x, y):
        for object in self.objects:
            if object.x == x and object.y == y:
                object.kill()
                self.objects.remove(object)
    def sort(self):
        mapping = {}
        objs = []
        for object in self.objects:
            if not object.x in mapping.keys():
                mapping[object.x] = []
            mapping[object.x].append(object)
        map = sorted(mapping.items(), key=lambda o: o[0])
        for row in map:
            r = sorted(row[1], key=lambda o: o.y)
            objs += r
        self.objects = objs.copy()
