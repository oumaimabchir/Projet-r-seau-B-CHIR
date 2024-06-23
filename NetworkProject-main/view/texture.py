import pygame as pg
from GameControl.setting import Setting
PATH = "./NetworkProject-main/assets/graphics/"
setting = Setting.getSettings()

def loadGrassImage():
    grass =pg.image.load(PATH + "grass.png").convert_alpha()
    return grass

def loadFlowerImage():
    flower = pg.image.load(PATH + "flower.png").convert_alpha()
    return flower

def loadMap():
    map = pg.image.load(PATH + "map.jpeg").convert_alpha()
    map = pg.transform.scale(map, (setting.SurfaceWidth(), setting.SurfaceHeight()))
    return map

    return purpleRight
def loadPurpleLeft():
    purpleLeft = pg.image.load(PATH + "Purple.png").convert_alpha()
    return purpleLeft

def loadGreenLeft():
    greenLeft = pg.image.load(PATH + "Green.png").convert_alpha()
    return greenLeft

def loadBlueLeft():
    blueLeft = pg.image.load(PATH + "Blue.png").convert_alpha()
    return blueLeft

def loadRedLeft():
    redLeft = pg.image.load(PATH + "Red.png").convert_alpha()
    return redLeft

def loadPurpleRight():
    purpleRight = pg.image.load(PATH + "Purple-modified.png").convert_alpha()
    return purpleRight

def loadGreenRight():
    greenRight = pg.image.load(PATH + "Green-modified.png").convert_alpha()
    return greenRight

def loadBlueRight():
    blueRight = pg.image.load(PATH + "Blue-modified.png").convert_alpha()
    return blueRight

def loadRedRight():
    redRight = pg.image.load(PATH + "Red-modified.png").convert_alpha()
    return redRight


def loadFoodImage():
    food = pg.image.load(PATH + "food.png").convert_alpha()
    return food
""" 
def loadExplosionImage():
    explosion1 = pg.image.load(PATH + "Ex1.png").convert_alpha()
    explosion2 = pg.image.load(PATH + "Ex2.png").convert_alpha()
    explosion3 = pg.image.load(PATH + "Ex3.png").convert_alpha()
    explosion4 = pg.image.load(PATH + "Ex4.png").convert_alpha()
    explosion5 = pg.image.load(PATH + "Ex5.png").convert_alpha()
    explosion6 = pg.image.load(PATH + "Ex6.png").convert_alpha()
    explosion7 = pg.image.load(PATH + "Ex7.png").convert_alpha()
    explosion8 = pg.image.load(PATH + "Ex8.png").convert_alpha()
    image = {
        1: explosion1
        ,2: explosion2
        ,3: explosion3
        ,4: explosion4
        ,5: explosion5
        ,6: explosion6
        ,7: explosion7
        ,8: explosion8
    }
    return image

def loadSpawnImage():
    spawn1 = pg.image.load(PATH + "Spawn.png").convert_alpha()
    spawn2 = pg.image.load(PATH + "Spawn2.png").convert_alpha()
    spawn3 = pg.image.load(PATH + "Spawn3.png").convert_alpha()
    spawn4 = pg.image.load(PATH + "Spawn4.png").convert_alpha()
    spawn5 = pg.image.load(PATH + "Spawn5.png").convert_alpha()
    spawn6 = pg.image.load(PATH + "Spawn6.png").convert_alpha()
    spawn7 = pg.image.load(PATH + "Spawn7.png").convert_alpha()
    spawn8 = pg.image.load(PATH + "Spawn8.png").convert_alpha()
    image = {
        1: spawn1
        ,2: spawn2
        ,3: spawn3
        ,4: spawn4
        ,5: spawn5
        ,6: spawn6
        ,7: spawn7
        ,8: spawn8
    }
    return image
"""
def loadDarkGrassImage():
    darkGrass = pg.image.load(PATH + "darkGrass.png").convert_alpha()
    return darkGrass

def loadDarkFlowerImage():
    darkFlower = pg.image.load(PATH + "flowerBright.png").convert_alpha()
    return darkFlower

def loadGrassBrightImage():
    grassBright = pg.image.load(PATH + "grassBright.png").convert_alpha()
    return grassBright

def loadFlowerBrightImage():
    flowerBright = pg.image.load(PATH + "flowerBright.png").convert_alpha()
    return flowerBright