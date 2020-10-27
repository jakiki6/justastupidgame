import json, webbrowser
from tile.tile import Tile, RotateableTile
from utils import utils
import math

with open("mod.json") as file:
    data = json.load(file)
    namespace = data["namespace"]
    _mod = data["mod"]

class Mover(RotateableTile):
    mod = _mod
    id = namespace + ":mover"
    texture_name = "tiles/mover.png"
    def tick(self, world):
        super().tick(world)
        self.t_x = self.x
        self.t_y = self.y
        x, y = utils.move(self.x, self.y, self.r)
        tx, ty = utils.move(self.x, self.y, self.r)
        sm = []
        while world.exist(tx, ty):
            obj = world.get(tx, ty)
#            print(self.x, self.y, tx, ty, *utils.move(tx, ty, self.r))
            if "moveable" in obj.tags:
                obj2 = world.get(*utils.move(obj.x, obj.y, self.r))
                if obj2 == None:
                    sm.append(obj)
                    break
                elif "moveable" in obj2.tags:
                    sm.append(obj)                    
                else:
                    sm.clear()
                    break
            else:
                break                       # @#! WHY WHHHHYYYYY
            tx, ty = utils.move(tx, ty, self.r)
        for o in sm:
            o.x, o.y = utils.move(o.x, o.y, self.r)
        if not world.isColliding(x, y):
            self.x = x
            self.y = y

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
        self.x, self.y = utils.move(self.x, self.y, self.r)
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
    tags = ["solid", "moveable"]

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

def get_tiles():
    return [Mover, RickRoller, SolidBlock, MoveableBlock, LevelFinish]
