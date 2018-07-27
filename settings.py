import pygame as pg

TITLE = "Noo, w godzinę to zrobimy"
FPS = 60
WIDTH = 1080
HEIGHT = 720

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
SHOWCOLLISIONS = False
MAPWIDTH = 0
MAPHEIGHT = 0

BULLET_IMG = pg.image.load('data/bullet.png')
ENEMY_IMG = pg.image.load("data/enemy.png")
TANK_IMG = pg.image.load("data/czolg.png")