import pygame as pg
import Players

# intiates o Pygame
pg.init()

# window dimensions
WINDOW_WIDTH = 672
WINDOW_HEIGHT = 672

# window setup
win = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Space Asteroid thing")

# game clock
clock = pg.time.Clock()

# player object
player = Players.Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), win)

# creating player sprite group and adding the player
player_group = pg.sprite.Group()
player_group.add(player)

# creating a player bullets sprite group
player_bullets = pg.sprite.Group()

# font for fps
font = pg.font.Font(None, 30)

# main game loop
def main():
    # ticks on the last frame to calculate dt
    ticks_last_frame = 0

    while True:
        # close the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        # close the window by pressing ESC
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.quit()
        
        # calculates dt to make movement contius over time
        t = pg.time.get_ticks()
        dt = (t - ticks_last_frame)
        ticks_last_frame = t

        # update player and player bullets
        player_group.update(dt, player_bullets)
        player_bullets.update(dt)

        # draws everithing on screen
        draw_all()

def draw_all():
    # fill screen
    win.fill((40, 40, 40))
    
    # draw player bullets and player
    player_bullets.draw(win)
    player_group.draw(win)
    
    # show fps on screen
    fps = font.render(str(int(clock.get_fps())), True, 'WHITE')
    win.blit(fps, (50,50))

    # updates the screen
    pg.display.flip()
    clock.tick(60)

main()