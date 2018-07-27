from settings import *
import pygame as py

class Camera:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def screenrect(self):
        return py.Rect(self.x, self.y, WIDTH, HEIGHT)

    def shift(self, thing):
        thing.rect.x = thing.x - self.x + thing.image_rect.x
        thing.rect.y = thing.y - self.y + thing.image_rect.y

    def shiftRect(self, thing):
        thing.x = thing.x - self.x
        thing.y = thing.y - self.y
        return thing

    def centerOn(self, thing, mapwidth, mapheight):
        if (thing.x > WIDTH/2) and (thing.x < (mapwidth - WIDTH/2 + TILESIZE)):
            self.x = thing.x - WIDTH/2
        if (thing.y > HEIGHT/2) and (thing.y < mapheight - HEIGHT/2 + TILESIZE):
            self.y = thing.y - HEIGHT/2