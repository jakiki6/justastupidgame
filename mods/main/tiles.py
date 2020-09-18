import json, webbrowser
from tile.tile import Tile
from utils import utils
import math

with open("mod.json") as file:
    data = json.load(file)
    namespace = data["namespace"]
    mod = data["mod"]

class Mover(Tile):
    mod = mod
    id = namespace + ":mover"
    texture_name = "tiles/mover.png"
    def tick(self, world):
        super().tick(world)
        self.t_x = self.x
        self.t_y = self.y
        self.x += round(utils.getmx(self.r) * 1)
        self.y += round(utils.getmy(self.r) * 1)

class RickRoller(Mover):
    mod = mod
    id = namespace + ":rickroller"
    texture_name = "tiles/rickroller.png"
    def onHit(self, tile, side):
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.alive = False
def get_tiles():
    return [Mover, RickRoller]
