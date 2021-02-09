import json, webbrowser
from tile.tile import Tile, RotateableTile
from utils import utils
import math, pygame, os

with open("mod.json") as file:
    data = json.load(file)
    namespace = data["namespace"]
    _mod = data["mod"]

class Mover(RotateableTile):
    mod = _mod
    id = namespace + ":mover"
    texture_name = "tiles/mover.png"
    tags = RotateableTile.tags + ["moveable"]
    def tick(self, world):
        super().tick(world)
        self.t_x = self.x
        self.t_y = self.y

        cm, sm = Mover.can_move(self.x, self.y, self.r, world)
        if not cm:
            return
                
        for o in sm:
            o.update_queue["x"], o.update_queue["y"] = utils.move(o.x, o.y, self.r)
        self.update_queue["x"], self.update_queue["y"] = utils.move(self.x, self.y, self.r)

    def can_move(_x, _y, _r, world):
        x, y = utils.move(_x, _y, _r)
        tx, ty = utils.move(_x, _y, _r)
        sm = []
        while world.exist(tx, ty):
            obj = world.get(tx, ty)  
            if "moveable" in obj.tags:
                obj2 = world.get(*utils.move(obj.x, obj.y, _r))
                if (isinstance(obj2, Mover)):
                    if obj2.r == _r:
                        c, m = Mover.can_move(obj2.x, obj2.y, obj2.r, world)
                        if not c:
                            return False, []
                        sm += m
                        return True, sm
                if obj2 == None:
                    sm.append(obj)
                    return True, sm
                elif "moveable" in obj2.tags:
                    sm.append(obj)
                else:
                    return False, []
            else:
                return False, []
            tx, ty = utils.move(tx, ty, _r)
        return True, sm

class RickRoller(RotateableTile):
    mod = _mod
    id = namespace + ":rickroller"
    texture_name = "tiles/rickroller.png"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._die = False
    def tick(self, world):
        if self._die:
            self.kill()
            super().tick(world)
            return
        self.t_x = self.x
        self.t_y = self.y
        self.update_queue["x"], self.update_queue["y"] = utils.move(self.x, self.y, self.r)
        super().tick(world)
    def onOverlay(self, tile):
        if tile == self:
            return
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self._die = True

class SolidBlock(Tile):
    mod = _mod
    id = namespace + ":solidblock"
    texture_name = "tiles/solidblock.png"

class MoveableBlock(Tile):
    mod = _mod
    id = namespace + ":moveableblock"
    texture_name = "tiles/moveableblock.png"
    tags = ["moveable", "solid"]

class LevelFinish(Tile):
    mod = _mod
    id = namespace + ":levelfinish"
    texture_name = "tiles/levelfinish.png"
    def tick(self, world):
        super().tick(world)
        self.world = world
    def onHit(self, tile, side):
        try:
            self.world.objects.clear()
        except:
            pass

class Rotater(Tile):
    tags = RotateableTile.tags

    mod = _mod
    id = namespace + ":rotater"
    texture_name = "tiles/rotater.png"

    textures = [pygame.surface.Surface((32, 32)) for _ in range(0, 2)]
    def __init__(self, x: int, y: int, r: float):
        super().__init__(x, y)
        self.r = r  
        texture = pygame.image.load(os.path.join("mods", self.__class__.mod, self.__class__.texture_name))
        self.textures[0] = texture.copy()
        self.textures[1] = pygame.transform.flip(texture, True, False)

    def onHit(self, tile, side):
        if side % 2:
            return
        if not "rotateable" in tile.tags:
            return
        if tile.id == self.id:
            return
        if self.r // 180:
            tile.update_queue["r"] = (tile.r + 90) % 360
        else:
            tile.update_queue["r"] = (tile.r - 90) % 360

    def get_texture(self):
        return self.textures[self.r // 180 > 0]
    def empty_instance(cl):
        return cl(0, 0, 0)

class Cloner(RotateableTile):
    mod = _mod
    id = namespace + ":cloner"
    texture_name = "tiles/cloner.png"

    tags = RotateableTile.tags + ["moveable"]

    def tick(self, world):
        super().tick(world)
        bx, by = utils.move(self.x, self.y, (self.r - 180) % 360)
        tx, ty = utils.move(self.x, self.y, self.r)
        if world.exist(bx, by) and not world.exist(tx, ty):
            obj = world.get(bx, by)
            obj2 = obj.copy()
            obj2.x, obj2.y = tx, ty
            obj2.should_tick = False
            world.objects.append(obj2)

def get_tiles():
    return [Mover, RickRoller, SolidBlock, MoveableBlock, LevelFinish, Rotater, Cloner]
