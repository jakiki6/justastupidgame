
state = {}
state["paused"] = False
state["cleaning"] = False

import os, sys, threading, time
from world.world import World
import tile.tile as tile_types

ticks = 0

tiles = []

for moddir in [f.path for f in os.scandir("mods") if f.is_dir()]:
    sys.path.append(os.path.abspath(moddir))
    os.chdir(moddir)
    mod = __import__("mod")
    mod_tiles = __import__("tiles")
    os.chdir("..")
    os.chdir("..")
    for tile in mod_tiles.get_tiles():
        tile.init(tile)
        tiles.append(tile)
    sys.apth = sys.path[:-1]
    print("Loaded from {}".format(moddir))

world = World()

from threads import ticking_run, render_run

tickingThread = threading.Thread(target=ticking_run, daemon=True)
renderThread = threading.Thread(target=render_run, daemon=True)

tickingThread.start()
renderThread.start()

from watchdog.watchdog import Watchdog
watchdog = Watchdog([tickingThread, renderThread])
watchdog.start()

while True:
    time.sleep(1)
