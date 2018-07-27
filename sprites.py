import pygame as pg
import math
from settings import *

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.walls, game.static
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('data/wall.png')
        self.image_rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisionRect = self.rect.copy()

    def update(self):
        pass

class Water(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.waterTiles, game.static
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('data/water.png')
        self.image_rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisionRect = self.rect.copy()        

    def update(self):
        pass

class Tank(pg.sprite.Sprite):
    def __init__(self, game, x, y, angle = 0, ai = True, name = "Random Tank"):
        self.groups = game.allSprites, game.entities, game.mortal
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        img = ""
        if ai:
            img = ENEMY_IMG
        else:
            img = TANK_IMG
        self.image_orig = img
        self.image = self.image_orig.copy()
        self.image_rect = self.image.get_rect()
        self.rect = self.image_orig.get_rect()
        self.x = x
        self.y = y
        self.angle = angle
        self.vel = 0
        self.collisionRect = self.rect.copy()
        self.ai = ai
        self.name = name

    def feedInputs(self, angleChange, acceleration):
        self.angleChange = angleChange
        self.acceleration = acceleration

    def aiLogic(self):
        self.acceleration = 100 * self.game.dt
        self.angleChange = 3 * self.game.dt
        self.shoot()

    def inWater(self):
        for tile in self.game.waterTiles:
            if tile.rect.colliderect(self.rect):
                return True
        return False

    def tankHeading(self):
        xr=-math.sin(-self.angle)
        yr=math.cos(-self.angle)
        return [xr,yr]

    def myCollision(self, angle, rect1, rect2):
        if rect1.colliderect(rect2):
            dx, dy = 0, 0
            if rect1.collidepoint(rect2.topleft):
                dy = rect2.top - rect1.bottom
                dx = rect2.left - rect1.right
            if rect1.collidepoint(rect2.topright):
                dy = rect2.top - rect1.bottom
                dx = rect2.right - rect1.left
            if rect1.collidepoint(rect2.bottomleft):
                dy = rect2.bottom - rect1.top
                dx = rect2.left - rect1.right
            if rect1.collidepoint(rect2.bottomright):
                dy = rect2.bottom - rect1.top
                dx = rect2.right - rect1.left
            if abs(dx) > abs(dy):
                return (0, dy)
            else:
                return (dx, 0)

    def update(self):
        if self.ai:
            self.aiLogic()
        if self.inWater():
            self.angleChange /= 2
            self.vel *= 0.90
        self.angle += self.angleChange
        self.vel += self.acceleration
        self.vel *= 0.98
        heading = self.tankHeading()
        newPos = [self.x - heading[0]*self.game.dt*self.vel, self.y - heading[1]*self.game.dt*self.vel]
        self.collisionRect.topleft = newPos
        collision = False
        for wall in self.game.walls:
            if wall.collisionRect.colliderect(self.collisionRect):
                dx, dy = self.myCollision(int(math.degrees(self.angle))%360, wall.collisionRect, self.collisionRect)
                self.x, self.y = newPos[0] - dx, newPos[1] - dy
                collision = True
                self.vel *= 0.8
                self.collisionRect.topleft = (self.x, self.y)
        if not collision:
            self.x, self.y = newPos
        self.image = pg.transform.rotate(self.image_orig, math.degrees(self.angle))
        self.image_rect = self.image.get_rect(center=(self.image_orig.get_rect().center)) # jezu jakie brzydkie
        for bullet in self.game.bullets:
            if bullet.collisionRect.colliderect(self.collisionRect):
                print(self.name + " shot by " + bullet.name)
                self.kill()
    
    def shoot(self):
        heading = self.tankHeading()
        x = self.x + self.image_rect.centerx/2 - heading[0] * self.collisionRect.w
        y = self.y + self.image_rect.centery/2 - heading[1] * self.collisionRect.h
        vx, vy = heading[0]*(500+self.vel), heading[1]*(500+self.vel)
        Bullet(self.game, x, y, self.angle, vx, vy, self.name)
        

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y, angle, vx, vy, name, lifespan=1):
        self.groups = game.allSprites, game.bullets, game.entities, game.mortal
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifespan = lifespan
        self.image_orig = BULLET_IMG
        self.rect = self.image_orig.get_rect()
        self.collisionRect = self.rect.copy()
        self.image = pg.transform.rotate(self.image_orig, math.degrees(angle))
        self.image_rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.name = name

    def update(self):
        self.x -= self.vx * self.game.dt
        self.y -= self.vy * self.game.dt
        self.rect.x, self.rect.y = self.x, self.y
        self.collisionRect.x, self.collisionRect.y = self.x, self.y
        self.lifespan -= self.game.dt
        for wall in self.game.walls:
            if wall.collisionRect.colliderect(self.collisionRect):
                self.kill()
        if self.lifespan <= 0:
            self.kill()