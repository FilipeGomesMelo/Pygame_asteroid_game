import pygame as pg
from copy import copy


class Bullet(pg.sprite.Sprite):
    def __init__(self, position: tuple, direction: pg.Vector2, win: pg.Surface):
        """
        Standard bullet class
        """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # bullet image and rect
        self.image = pg.image.load('images/bullet.png') 
        self.original_image = pg.image.load('images/bullet.png') 
        self.rect = self.image.get_rect()

        # starting coordenates
        self.center = position
        self.rect.center = position

        # direction Vector2
        self.direction = copy(direction)

        # window and window dimensions
        self.win = win
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = win.get_size()

        # speed
        self.speed = 0.5

        # radius
        self.radius = 4

        # ticks when the bullet was created
        self.ticks_created = pg.time.get_ticks()

        # time before the bullet disapears
        self.duration = 500
    
    def update(self, dt):
        # checks if the bullet needs to be destroyed   
        t = pg.time.get_ticks()
        if t - self.ticks_created > self.duration:
            self.kill()

        # updates the bullet center
        self.center += self.direction*self.speed*dt
        
        # moves the bullet to the other side of the screen in case it leaves the screen
        if self.center[0] < 0:
            self.center[0] = self.WINDOW_WIDTH
        elif self.center[0] > self.WINDOW_WIDTH:
            self.center[0] = 0 

        if  self.center[1] < 0:
            self.center[1] = self.WINDOW_HEIGHT
        elif self.center[1] > self.WINDOW_HEIGHT:
            self.center[1] = 0

        # updates the rect center
        self.rect.center = self.center
