import pygame
from pygame.locals import *

from sprites import Ground, Player, JumpPad
from physics import apply_gravity, move_and_collide,  crouching_adjustment
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(20, 700, 960, 100)
player = Player(45, 625, 50, 50)

# Test block: short enough to jump over (50px tall)
test_block = Ground(300, 650, 60, 50)
test_block.image.fill((180, 80, 80))   # reddish

test_block2 = Ground(425, 600, 60, 60)
test_block2.image.fill((180, 80, 80))   # reddish

test_block3 = Ground(550, 500, 30, 20)
test_block3.image.fill((180, 80, 80))   # reddish
# Test wall: too tall to jump over (200px tall)
test_wall = Ground(575, 475, 60, 185)
test_wall.image.fill((80, 80, 180))    # bluish

jump_pad = JumpPad(700, 680, 60, 20, launch_vel= -1200)
jump_pad.image.fill((255, 215, 0))   # yellowish

# Colliders list (everything the player can collide with)
colliders = [ground, test_block, test_block2, test_block3, test_wall, jump_pad]



# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(ground, player, test_block, test_block2, test_block3, test_wall, jump_pad)


running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Player input & physics
    player.handle_input()
    apply_gravity(player, dt)
    move_and_collide(player, colliders, dt)
    crouching_adjustment(player, colliders)
    
    #Sky color
    screen.fill((119, 164, 237))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()