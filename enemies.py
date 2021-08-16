import pygame as pg

class Bomb_ship(pg.sprite.Sprite):
    def __init__(self, center: tuple, win: pg.Surface):
        """
        Bomber enemy, aways acelerates in the direction of the player
        """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # to avoid image curruption when rotating it over and over
        # we will have the original image saved and rotate the original image
        self.image = pg.image.load('images/bomb_ship.png') 
        self.original_image = pg.image.load('images/bomb_ship.png') 
        self.rect = self.image.get_rect()
        
        # ships center coordenates 
        # ship center will be saved on a list of two floats
        # since rect.center holds only int
        # so movements lesser than a pixel can acummulate
        self.center = center
        self.rect.center = center

        # direction the ship is facing
        self.direction = pg.math.Vector2(0,-1) 

        # surface window and window dimensions
        self.win = win
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = win.get_size()

        # aceleration and deceleration
        self.aceleration = 0.001
        
        # max speed the ship can reach
        self.max_speed = 0.3

        # current ship speed vector
        self.speed = pg.math.Vector2(0, 0)
    
        # ticks when the bullet was created
        self.ticks_created = pg.time.get_ticks()

        # time before the bullet disapears
        self.duration = 999999999999999999999999999999

        # rotation speed
        self.rotate_speed = 0.25

        self.image_director = pg.math.Vector2(0, 1)
    
    def rotate(self, angle):
        """
        rotates the Bomb_ship ship by a certain angle
        """
        # rotates director vector
        self.image_director.rotate_ip(angle)

        # angle with the y axis
        angle = self.image_director.angle_to((0,-1))
        
        # rotates the original image to avoid corruption
        self.image = pg.transform.rotate(self.original_image, angle)

        # updates the rect
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def follow(self, dt, target):
        if target != self.center:
            self.direction = (target - pg.Vector2(self.center)).normalize()
            self.rotate(self.rotate_speed*dt)

    # controls and moves the ship
    def update(self, dt, player_pos, bullets):
        # checks if the bullet needs to be destroyed   
        t = pg.time.get_ticks()
        if t - self.ticks_created > self.duration or pg.sprite.spritecollide(self, bullets, True):
            self.kill()

        # rotates the ship direction based on player input
        self.follow(dt, player_pos)

        # ships current aceleration
        self.speed +=  self.direction*self.aceleration*dt 

        # limits the maximum speed
        if self.speed.magnitude() > self.max_speed:
            self.speed = self.speed.normalize()*self.max_speed
        
        # moves the ship's center based on the speed
        self.center += self.speed*dt
    
        # moves the ship to the other side of the screen in case it leaves the screen
        if self.center[0] < 0:
            self.center[0] = self.WINDOW_WIDTH
        elif self.center[0] > self.WINDOW_WIDTH:
            self.center[0] = 0 

        if  self.center[1] < 0:
            self.center[1] = self.WINDOW_HEIGHT
        elif self.center[1] > self.WINDOW_HEIGHT:
            self.center[1] = 0

        # updates the rect center
        self.rect.center = self.center[:]   