import json, webbrowser
from tile.tile import Tile
from utils import utils
import math

with open("mod.json") as file:
    data = json.load(file)
    namespace = data["namespace"]
    _mod = data["mod"]

class Mover(Tile):
    mod = _mod
    id = namespace + ":mover"
    texture_name = "tiles/mover.png"
    def tick(self, world):
        super().tick(world)
        self.t_x = self.x
        self.t_y = self.y
        x, y = utils.move(self.x, self.y, self.r)
        tx, ty = utils.move(self.x, self.y, self.r)
        while world.exist(tx, ty):
            obj = world.get(tx, ty)
#            print(self.x, self.y, tx, ty, *utils.move(tx, ty, self.r))
            if "moveable" in obj.tags:
                obj2 = world.get(*utils.move(tx, ty, self.r))
                if obj2 == None:
                    obj.x, obj.y = utils.move(tx, ty, self.r)
                    break
                elif "moveable" in obj2.tags:
                    obj.x, obj.y = utils.move(tx, ty, self.r)
            else:
                break                       # @#! WHY WHHHHYYYYY
            tx, ty = utils.move(tx, ty, self.r)
        if not world.isColliding(x, y):
            self.x = x
            self.y = y

class RickRoller(Tile):
    mod = _mod
    id = namespace + ":rickroller"
    texture_name = "tiles/rickroller.png"
    def tick(self, world):
        self.t_x = self.x
        self.t_y = self.y 
        self.x, self.y = utils.move(self.x, self.y, self.r)
        super().tick(world)
    def onOverlay(self, tile):
        if tile == self:
            return
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.kill()

class SolidBlock(Tile):
    mod = _mod
    id = namespace + ":solidblock"
    texture_name = "tiles/solidblock.png"

class MoveableBlock(Tile):
    mod = _mod
    id = namespace + ":moveableblock"
    texture_name = "tiles/moveableblock.png"
    tags = ["solid", "moveable"]

def get_tiles():
    return [Mover, RickRoller, SolidBlock, MoveableBlock]
