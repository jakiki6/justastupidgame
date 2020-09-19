import math

def getmx(r):
    if r == 90:
        return 1
    elif r == 270:
        return -1
    return 0
def getmy(r):
    if r == 0:
        return 1
    elif r == 180:
        return -1
    return 0
def move(x, y, r):
    return (round(x + getmx(r)), round(y + getmy(r)))
