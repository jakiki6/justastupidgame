import pygame, os, copy

class Tile(object):
    '''
     701
     6#2
     543
    '''
    id = ""
    mod = ""
    textures = [pygame.surface.Surface((32, 32)) for _ in range(0, 4)]
    tags = ["solid"]
    def __init__(self, x: int, y: int):
        self.x, self.y= x, y
        self.t_x, self.t_y = x, y
        self.a_x, self.a_y, self.a_r = 0, 0, 0
        self.id = self.__class__.id
        self.tags = self.__class__.tags
        self.textures = self.__class__.textures
        self.alive = True
        self.should_tick = True
        self.update_queue = {}
    def onHit(self, tile, side):
        pass
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
    def apply(self):
        for key, val in self.update_queue.items():
            setattr(self, key, val)
        self.update_queue.clear()
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
    def init(cl):
        cl.textures = [pygame.image.load(os.path.join("mods", cl.mod, cl.texture_name)) for _ in range(0, 4)]
    def kill(self):
        self.alive = False
    def get_texture(self):
        return self.textures[0]
    def empty_instance(cl):
        return cl(0, 0)
    def copy(self):
        return self.__class__(self.x, self.y)

class RotateableTile(Tile):
    texture_path = ""
    tags = Tile.tags + ["rotateable"]
    def __init__(self, x: int, y: int, r: float):
        super().__init__(x, y)
        self.r = r
        texture = pygame.image.load(os.path.join("mods", self.__class__.mod, self.__class__.texture_name))
        for r in range(0, 360, 90):
            self.textures[r // 90] = pygame.transform.rotate(texture, r)
    def get_texture(self):
        return self.textures[self.r // 90]
    def empty_instance(cl):
        return cl(0, 0, 0)
    def copy(self):
        return self.__class__(self.x, self.y, self.r)
