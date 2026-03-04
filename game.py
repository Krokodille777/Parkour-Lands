import pygame
from pygame.locals import *

from sprites import Ground, Player, JumpPad, Lava, Spike, Bridge, Water, Ladder, Accelerator, Decelerator, Checkpoint, FragileGround
from physics import apply_gravity, move_and_collide,  crouching_adjustment, climb_ladder
from physics import jump_from_the_top_of_ladder, buoyant_force, apply_speed_zones
from maincamera import follow_player
from checkpoint import checkpoint_activation
from fragile_ground import fragile_ground_check, respawn_fragile_ground
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(0, 700, 912, 500)
player = Player(45, 625, 50, 50)


jump_Pad = JumpPad(300, 680, 60, 20, launch_vel = -1500)
jump_Pad.image.fill((255, 255, 0))   # Yellowish

# Test block: short enough to jump over (50px tall)

fragilePlatform = FragileGround(1112, 400, 100, 20)

test_block = Ground(1312, 400, 150, 50)
spike_left = Spike(1350, 370, 40, 50, 90)
spike_left2 = Spike(1350, 340, 40, 50, 90)
test_wall2 = Ground(1400, 300, 50, 150)

test_block3 = Ground(230, 230, 180, 80)
spike_up = Spike(335, 310, 50, 40, 180)
spike_up2 = Spike(295, 310, 50, 40, 180)
spike_up3 = Spike(255, 310, 50, 40, 180)




ladder1 = Ladder(850, 410, 20, 290)
bridge_upon_lava = Bridge(725, 400, 100, 20)
checkpoint1 = Checkpoint(728, 350, 50, 50)
# water_pool = Water(912, 750, 400, 500)
# water_pool.image.fill((0, 101, 255))    # Blue color for water

test_wall = Ground(890, 400, 50, 300)
test_wall.image.fill((128, 128, 128))  # Gray color for test wall

lava_pool = Lava(912, 750, 400, 500)
lava_pool.image.fill((250, 112, 47))    # Orange color for lava



# Colliders list (everything the player can collide with)
colliders = [ground, test_block3, jump_Pad, lava_pool, test_wall, bridge_upon_lava, test_block, test_wall2, fragilePlatform]
triggers = [ladder1, spike_up, spike_up2, spike_up3, spike_left, spike_left2, ]  # Objects that trigger special interactions (like climbing or damage)
dynamic_colliders = [fragilePlatform]  # Colliders that can change state (like breaking)

water_group = pygame.sprite.LayeredUpdates()
fragile_grounds = [fragilePlatform]
water_group.add(lava_pool, layer = 0)
# speed_zones = [accelerator_block, decelerator_block]
checkpoint_group = pygame.sprite.LayeredUpdates()

checkpoint_group.add(checkpoint1, layer = 0)

# Create sprite groups
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(ground, layer = 0)
all_sprites.add(test_block, layer = 0)
all_sprites.add(test_wall, layer = 0)
all_sprites.add(test_block3, layer = 0)
all_sprites.add(fragilePlatform, layer = 0)
all_sprites.add(ladder1, layer = 1)
all_sprites.add(bridge_upon_lava, layer = 1)
all_sprites.add(spike_left, layer = 0)
all_sprites.add(spike_left2, layer = 0)
# all_sprites.add(water_pool, layer = 1)
all_sprites.add(lava_pool, layer = 1)
all_sprites.add(spike_up, layer = 0)
all_sprites.add(spike_up2, layer = 0)
all_sprites.add(spike_up3, layer = 0)
all_sprites.add(jump_Pad, layer = 1)
# all_sprites.add(accelerator_block, layer = 0)
# all_sprites.add(decelerator_block, layer = 0)
all_sprites.add(checkpoint1, layer = 0)
all_sprites.add(player, layer = 2)
all_sprites.add(test_wall2, layer = 0)


running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Player input & physics
    player.handle_input()
    # apply_speed_zones(player, speed_zones)
    apply_gravity(player, dt)
    move_and_collide(player, colliders, dt, triggers)
    crouching_adjustment(player, colliders)
    climb_ladder(player, triggers)
    jump_from_the_top_of_ladder(player, triggers)
    buoyant_force(player, triggers) 
    checkpoint_activation(player, checkpoint_group)
    fragile_ground_check(player, fragile_grounds, colliders, dt)
    respawn_fragile_ground(colliders, all_sprites, fragile_grounds, dt)



    offset_x, offset_y = follow_player(player, screen.get_width(), 2000, screen.get_height(), 1500)  # Assuming world width is 2000px and height is 1000px
    #Sky color
    screen.fill((119, 164, 237))
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

            
    pygame.display.flip()

pygame.quit()