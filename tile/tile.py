import pygame, os

class Tile(object):
    '''
     701
     6#2
     543
    '''
    id = ""
    mod = ""
    texture_name = ""
    solid = True
    def __init__(self, x: int, y: int, r: float):
        self.x, self.y, self.r = x, y, r
        self.t_x, self.t_y, self.t_r = x, y, r
        self.a_x, self.a_y, self.a_r = 0, 0, 0
        self.id = self.__class__.id
        self.solid = self.__class__.solid
        self.alive = True
    def onHit(self, tile, side):
        pass # return modified tile
    def onOverlay(self, tile):
        pass
    def tick(self, world):
        for obj in world.objects:
            for x in range(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):
                    if obj.x == x and obj.y == y:
                        if x == self.x and y == self.y:
                            self.onOverlay(obj)
                        else:
                            self.onHit(obj, self.getSide(x, y))
    def getSide(self, x, y):
        if x == self.x and y == self.y - 1:
            return 0
        if x == self.x + 1 and y == self.y - 1:
            return 1
        if x == self.x + 1 and y == self.y:
            return 2
        if x == self.x + 1 and y == self.y + 1:
            return 3
        if x == self.x and y == self.y + 1:
            return 4
        if x == self.x - 1 and y == self.y + 1:
            return 5
        if x == self.x - 1 and y == self.y:
            return 6
        if x == self.x - 1 and y == self.y - 1:
            return 7
        else:
            return -1
    def init(self):
        self.__class__.texture = pygame.image.load(os.path.join("mods", self.__class__.mod, self.__class__.texture_name))
