import math

def getmx(r):
    if 0 < r < 180:
        return 1
    elif 180 < r < 360:
        return -1
    return 0
def getmy(r):
    if 90 < r < 270:                 
        return 1
    elif 270 < r < 90:
        return -1
    return 0
