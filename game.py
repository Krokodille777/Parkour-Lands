import pygame
from pygame.locals import *

from sprites import Ground, Player, JumpPad, Lava, Spike, Bridge, Water, Ladder
from physics import apply_gravity, move_and_collide,  crouching_adjustment, climb_ladder
from physics import jump_from_the_top_of_ladder, buoyant_force
from maincamera import follow_player
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(20, 700, 900, 500)
player = Player(45, 625, 50, 50)

# Test block: short enough to jump over (50px tall)
test_block = Ground(720, 650, 60, 50)
test_block.image.fill((180, 80, 80))   # reddish




ladder = Ladder(720, 315, 25, 200)


test_block5 = Ground(780, 310, 180, 80)

# Test wall: too tall to jump over (200px tall)


test_wall2 = Ground(925, 150, 60, 185)
test_wall2.image.fill((80, 80, 180))    # bluish



bridge_upon_lava = Bridge(912, 730, 100, 20)

water_pool = Water(912, 750, 400, 500)
water_pool.image.fill((0, 101, 255))    # Blue color for water


spike_left = Spike(880, 260, 50, 60, 90)
spike_left2 = Spike(880, 220, 50, 60, 90)

                    

# Colliders list (everything the player can collide with)
colliders = [ground, test_block, test_block5,  test_wall2,    bridge_upon_lava]
triggers = [ladder, spike_left, spike_left2, water_pool]  # Objects that trigger special interactions (like climbing or damage)
water_group = pygame.sprite.LayeredUpdates()
water_group.add(water_pool, layer = 0)


# Create sprite groups
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(ground, layer = 0)
all_sprites.add(test_block, layer = 0)
all_sprites.add(test_block5, layer = 0)
all_sprites.add(test_wall2, layer = 0)
all_sprites.add(ladder, layer = 1)
all_sprites.add(bridge_upon_lava, layer = 1)
all_sprites.add(water_pool, layer = 1)
all_sprites.add(spike_left, layer = 1)
all_sprites.add(spike_left2, layer = 1)
all_sprites.add(player, layer = 2)


running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Player input & physics
    player.handle_input()
    apply_gravity(player, dt)
    move_and_collide(player, colliders, dt, triggers)
    crouching_adjustment(player, colliders)
    climb_ladder(player, triggers)
    jump_from_the_top_of_ladder(player, water_group)
    buoyant_force(player, triggers) 
    offset_x, offset_y = follow_player(player, screen.get_width(), 2000, screen.get_height(), 1500)  # Assuming world width is 2000px and height is 1000px
    #Sky color
    screen.fill((119, 164, 237))
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))
    pygame.display.flip()

pygame.quit()