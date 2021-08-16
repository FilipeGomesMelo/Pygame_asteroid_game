import pygame as pg
import random
import math
import copy

class asteroid(pg.sprite.Sprite):
    def __init__(self, center: tuple, size: int, direction: pg.Vector2, win: pg.Surface):
        """
        asteroid class
        """
        # Call the parent class (Sprite) constructor
        super().__init__()

        sizes = [40, 60, 80, 100]
        speeds = [0.16, 0.12, 0.08, 0.05]

        self.radius = sizes[size]/2
        self.size = size
        self.speed = speeds[size]

        # bullet image and rect
        self.image = pg.image.load(f'images/Asteroid_{size+1}.png')
        self.rect = self.image.get_rect()

        # starting coordenates
        self.center = copy.copy(center)
        self.rect.center = copy.copy(center)

        # direction Vector2
        self.direction = copy.copy(direction)

        # window and window dimensions
        self.win = win
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = win.get_size()

    def update(self, dt, bullets, asteroids):
        if pg.sprite.spritecollide(self, bullets, True):
            if self.size > 0: 
                angle = random.random()*100
                aux = pg.Vector2(math.sin(angle), math.cos(angle))
                aux2 = self.center+self.radius*self.direction.rotate(90)
                asteroids.add(asteroid(aux2, self.size-1, aux, self.win))
                angle = random.random()*100
                aux2 = self.center+self.radius*self.direction.rotate(-90)
                asteroids.add(asteroid(aux2, self.size-1, -aux, self.win))
            self.kill()

        # updates the bullet center
        self.center += self.direction*self.speed*dt
        
        for ast in asteroids:
            if ast == self: continue
            v1 = pg.Vector2(self.center)
            v2 = pg.Vector2(ast.center)
            sizes = [40, 60, 80, 100]
            nv = v2-v1
            if 0 != nv.length() < sizes[self.size]/2+sizes[ast.size]/2:
                self.center = -nv.normalize()*(sizes[self.size]/2+sizes[ast.size]/2+5)+v2
                
                previous_self = self.direction

                if not(-90 < self.direction.angle_to(-nv) < 90):
                    try:
                        self.direction = self.direction.reflect(nv)
                    except:
                        pass
                elif self.direction+ast.direction != (0,0):
                    self.direction = (self.direction+ast.direction).normalize()

                if not(-90 < ast.direction.angle_to(nv) < 90):
                    try:
                        ast.direction = ast.direction.reflect(nv)
                    except:
                        pass
                elif ast.direction+previous_self != (0,0):
                    ast.direction = (ast.direction+previous_self).normalize()

        # moves the bullet to the other side of the screen in case it leaves the screen
        if self.center[0] < self.radius and self.direction.x < 0:
            self.direction.x = -self.direction.x
        elif self.center[0] > self.WINDOW_WIDTH-self.radius and self.direction.x > 0:
            self.direction.x = -self.direction.x 

        if  self.center[1] < self.radius and self.direction.y < 0:
            self.direction.y = -self.direction.y
        elif self.center[1] > self.WINDOW_HEIGHT-self.radius and self.direction.y > 0:
            self.direction.y = -self.direction.y

        # updates the rect center
        self.rect.center = self.center