# REQUIRES installed pygame

import pygame as pg
import sys
from settings import *
from sprites import *
from camera import Camera

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.camera = Camera()

    def new(self):
        self.allSprites = pg.sprite.Group()
        self.static = pg.sprite.Group()
        self.entities = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.waterTiles = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mortal = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.inView = pg.sprite.Group()
        self.playerTank = Tank(self, 300.0, 300.0, 0, False, "Player")

    def quit(self):
        pg.quit()
        sys.exit()
        
    def run(self):
        # Game Loop
        self.loadMap("map1")
        while True:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        print("ITSWORKING")
        self.allSprites.update()
        self.camera.centerOn(self.playerTank, MAPWIDTH, MAPHEIGHT)
        for sprite in self.allSprites:
            self.camera.shift(sprite)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.playerTank.shoot()
                if event.key == pg.K_F1:
                    global SHOWCOLLISIONS
                    SHOWCOLLISIONS = not SHOWCOLLISIONS
        pressed = pg.key.get_pressed()
        angle, acceleration = 0, 0
        if pressed[pg.K_LEFT]:
            angle = self.dt * 3
        if pressed[pg.K_RIGHT]:
            angle = -self.dt * 3
        if pressed[pg.K_DOWN]:
            acceleration = -500*self.dt
        if pressed[pg.K_UP]:
            acceleration = 1000*self.dt
        self.playerTank.feedInputs(angle, acceleration)

    def loadMap(self, mapName):
        with open("data/" + mapName + ".txt", 'r') as f:
            y = -1
            x = -1
            for line in f:
                y += 1
                x = -1
                for byte in line:
                    x += 1
                    if byte == "W":
                        Water(self, x, y)
                    if byte == "O":
                        Wall(self, x, y)
                    if byte == "E":
                        Tank(self, x * TILESIZE, y * TILESIZE)
            global MAPWIDTH
            global MAPHEIGHT
            MAPWIDTH = x*TILESIZE
            MAPHEIGHT = y*TILESIZE

    def drawGrid(self):
        startx = int(-self.camera.x)%TILESIZE
        starty = int(-self.camera.y)%TILESIZE
        for x in range(startx, WIDTH, TILESIZE):
            pg.draw.line(self.screen, (50, 50, 50), (x, 0), (x, HEIGHT))
        for y in range(starty, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, (50, 50, 50), (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill((10, 20, 10))
        self.drawGrid()
        if SHOWCOLLISIONS:
            for entity in self.entities:
                pg.draw.rect(self.screen, (200, 200, 0), self.camera.shiftRect(entity.collisionRect))
        self.static.draw(self.screen)
        self.entities.draw(self.screen)
        pg.display.flip()

g = Game()
#g.showStartScreen()
while True:
    g.new()
    g.run()
#   g.showGameOverScreen()

pg.quit()
