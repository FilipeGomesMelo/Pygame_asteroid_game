import pygame as pg
import Bullets 

#####################################
# player class                      #
# might use for enemie ships later  #
#####################################
class Player(pg.sprite.Sprite):
    def __init__(self, center, win):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # to avoid image curruption when rotating it over and over
        # we will have the original image saved and rotate the original image
        self.image = pg.image.load('images/arrow_ship.png') 
        self.original_image = pg.image.load('images/arrow_ship.png') 
        self.rect = self.image.get_rect()
        
        # ships center coordenates 
        # ship cennter will be saved on a list of two floats
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
        self.aceleration = 0.0005
        self.drag = 0.00025

        # max speed the ship can reach
        self.max_speed = 0.3

        # current ship speed vector
        self.speed = pg.math.Vector2(0, 0)

        # rotation speed
        self.rotate_speed = 0.25
    
        # bullet list
        self.bullets = []

        # ticks from the last time the player made a shot
        self.ticks_last_shot = 0

        # time cooldown between shots
        self.shot_cooldown = 200

        # limits of bullets the player can have on screen
        self.bullet_limit = 3
    
    # rotates the player by a certain angle
    def rotate(self, angle):
        # rotates director vector
        self.direction.rotate_ip(angle)

        # angle with the y axis
        angle = self.direction.angle_to((0,-1))

        # rotates the original image to avoid corruption
        self.image = pg.transform.rotate(self.original_image, angle)

        # updates the rect
        self.rect = self.image.get_rect(center=self.rect.center)

    # controls and moves the ship
    def update(self, dt, bullets_group):
        # pressed keys
        keys = pg.key.get_pressed()

        # rotates the ship direction based on player input
        self.rotate((keys[pg.K_d]-keys[pg.K_a])*self.rotate_speed*dt)

        # ships current aceleration
        acelerate = pg.math.Vector2(0,0)
        if keys[pg.K_w]:
            acelerate = self.direction*self.aceleration*dt   
        
        # if the player is not acelerating, the ship decelerates
        if acelerate.magnitude() == 0 and self.speed.magnitude() != 0:
            decelerate = self.speed.normalize()*self.drag*dt
            if self.speed.magnitude() < decelerate.magnitude():
                self.speed = self.speed*0
            else:
                self.speed -= decelerate

        # the ship acelerates
        elif acelerate.magnitude() != 0:
            self.speed += acelerate

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

        # calcula o tempo desde o ultimo tiro
        t = pg.time.get_ticks()
        dt_shot = (t - self.ticks_last_shot)

        # creates new bullets
        if dt_shot >= self.shot_cooldown and keys[pg.K_SPACE] and len(bullets_group)+1 <= self.bullet_limit:
            bullets_group.add(Bullets.Bullet(self.rect.center+self.direction*10, self.direction, self.win))
            self.ticks_last_shot = t      