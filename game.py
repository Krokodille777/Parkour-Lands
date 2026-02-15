import pygame
from pygame.locals import *

from sprites import Ground, Player, JumpPad, Lava, Spike, Bridge, Water, Ladder, Accelerator, Decelerator
from physics import apply_gravity, move_and_collide,  crouching_adjustment, climb_ladder
from physics import jump_from_the_top_of_ladder, buoyant_force, apply_speed_zones
from maincamera import follow_player
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(0, 700, 900, 500)
player = Player(45, 625, 50, 50)


jump_Pad = JumpPad(300, 680, 60, 20, launch_vel = -1200)
jump_Pad.image.fill((255, 255, 0))   # Yellowish

# Test block: short enough to jump over (50px tall)
test_block = Ground(720, 650, 60, 50)
test_block.image.fill((180, 80, 80))   # reddish




ladder = Ladder(720, 315, 25, 200)

test_block2 = Ground(480, 310, 180, 80)
accelerator_block = Accelerator(400, 310, 130, 80)
test_block3 = Ground(240, 310, 180, 80)
spike_down = Spike(335, 270, 50, 40, 0)
spike_down2 = Spike(295, 270, 50, 40, 0)
spike_down3 = Spike(255, 270, 50, 40, 0)
decelerator_block = Decelerator(120, 310, 120, 80)
test_block4 = Ground(50, 310, 180, 80)
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
colliders = [ground, test_block, test_block2, test_block3, test_block4, test_block5,  test_wall2, accelerator_block, decelerator_block, bridge_upon_lava, jump_Pad]
triggers = [ladder, spike_left, spike_left2, water_pool, spike_down, spike_down2, spike_down3, accelerator_block, decelerator_block]  # Objects that trigger special interactions (like climbing or damage)
water_group = pygame.sprite.LayeredUpdates()
water_group.add(water_pool, layer = 0)
speed_zones = [accelerator_block, decelerator_block]

# Create sprite groups
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(ground, layer = 0)
all_sprites.add(test_block, layer = 0)
all_sprites.add(test_block2, layer = 0)
all_sprites.add(test_block3, layer = 0)
all_sprites.add(test_block4, layer = 0)
all_sprites.add(test_block5, layer = 0)
all_sprites.add(test_wall2, layer = 0)
all_sprites.add(ladder, layer = 1)
all_sprites.add(bridge_upon_lava, layer = 1)
all_sprites.add(water_pool, layer = 1)
all_sprites.add(spike_left, layer = 0)
all_sprites.add(spike_left2, layer = 0)
all_sprites.add(spike_down, layer = 0)
all_sprites.add(spike_down2, layer = 0)
all_sprites.add(spike_down3, layer = 0)
all_sprites.add(jump_Pad, layer = 1)
all_sprites.add(accelerator_block, layer = 1)
all_sprites.add(decelerator_block, layer = 1)
all_sprites.add(player, layer = 2)


running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Player input & physics
    apply_speed_zones(player, speed_zones)
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