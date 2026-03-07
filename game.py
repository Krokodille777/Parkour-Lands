import pygame
from pygame.locals import *

from sprites import Ground, Player, JumpPad, Lava, Spike, Bridge, Water, Ladder, Accelerator, Decelerator, Checkpoint, FragileGround, ElevatorUpDown, ElevatorLeftRight, Ice, StartPortal, EndPortal, DynamicSpike
from sprites import DynamicSpikePlatform
from physics import apply_gravity, move_and_collide,  crouching_adjustment, climb_ladder
from physics import jump_from_the_top_of_ladder, buoyant_force, apply_speed_zones
from maincamera import follow_player
from checkpoint import checkpoint_activation
from fragile_ground import fragile_ground_check, respawn_fragile_ground
from elevators import updown_elevator_movement, leftright_elevator_movement
from portals import link_portals, teleport_player, cooldown_timer
from dynamic_spike import dynamic_spike_movement_based_on_timer
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(0, 700, 550, 500)
island1 = Ground(1100, 700, 200, 500)
player = Player(10, 625, 50, 50)

ice_plate = Ice(550, 700, 230, 50)
ground_under_ice = Ground(550, 750, 230, 500)
jump_Pad = JumpPad(1175, 680, 60, 20, launch_vel = -1700)
jump_Pad.image.fill((255, 255, 0))   # Yellowish

# # Test block: short enough to jump over (50px tall)

dynamic_spike_platform = DynamicSpikePlatform(75, 700, 77, 30)
spike1 = DynamicSpike(75, 695, 30, 30, 0)
spike2 = DynamicSpike(99, 695, 30, 30, 0)
spike3 = DynamicSpike(122, 695, 30, 30, 0)

dynamic_spike_platform2 = DynamicSpikePlatform(323, 700, 77, 30)
spike11 = DynamicSpike(323, 695, 30, 30, 0)
spike21 = DynamicSpike(346, 695, 30, 30, 0)
spike31 = DynamicSpike(369, 695, 30, 30, 0)

dynamic_spike_platform3 = DynamicSpikePlatform(1098, 115, 77, 50)
spike12 = DynamicSpike(1098, 145, 30, 30, 180)
spike22 = DynamicSpike(1121, 145, 30, 30, 180)
spike32 = DynamicSpike(1144, 145, 30, 30, 180)

fragilePlatform = FragileGround(875, 675, 50, 50)

test_block = Ground(950, 275, 125, 25)
test_block2 = Ground(1050, 115, 200, 50)
# spike_left = Spike(1350, 370, 40, 50, 90)
# spike_left2 = Spike(1350, 340, 40, 50, 90)
# test_wall2 = Ground(1400, 300, 50, 150)

# elevatorleftRight1 = ElevatorLeftRight(972, 400, 75, 25, 200)

test_block3 = Ground(270, 515, 225, 150)

orangw_portal = EndPortal(350, 395, 50, 75)


blue_portal = StartPortal(950, 200, 50, 75)
link_portals(blue_portal, orangw_portal)

# spike_up = Spike(335, 310, 50, 40, 180)
# spike_up2 = Spike(295, 310, 50, 40, 180)
# spike_up3 = Spike(255, 310, 50, 40, 180)

# elevatorupDown1 = ElevatorUpDown(500, 300, 75, 25, 200)


ladder1 = Ladder(250, 515, 20, 150)
bridge_upon_lava = Bridge(1000, 700, 100, 20)
checkpoint1 = Checkpoint(10, 525, 50, 50)
# water_pool = Water(912, 750, 400, 500)
# water_pool.image.fill((0, 101, 255))    # Blue color for water

test_wall = Ground(1250, 200, 50, 500)
test_wall.image.fill((128, 128, 128))  # Gray color for test wall   

lava_pool = Lava(780, 800, 320, 500)
lava_pool.image.fill((250, 112, 47))    # Orange color for lava



# Colliders list (everything the player can collide with)
colliders = [ground, test_block3, test_block2, test_wall, test_block, dynamic_spike_platform, dynamic_spike_platform2, dynamic_spike_platform3, jump_Pad, island1, bridge_upon_lava, lava_pool, ice_plate, ground_under_ice, fragilePlatform]  # Add all solid objects here
triggers = [lava_pool, ladder1, spike1, spike2, spike3, spike11, spike21, spike31, spike12, spike22, spike32]  # Objects that trigger special interactions (like climbing or damage)
dynamic_colliders = [spike1, spike2, spike3, spike11, spike21, spike31, spike12, spike22, spike32]  # Moving solids like elevators go here

water_group = pygame.sprite.LayeredUpdates()
fragile_grounds = [fragilePlatform]
ice_plate_group = pygame.sprite.LayeredUpdates()
portals = pygame.sprite.LayeredUpdates()
portals.add(blue_portal, layer = 0)
portals.add(orangw_portal, layer = 0)
ice_plate_group.add(ice_plate, layer = 0)
# water_group.add(water_pool, layer = 0)
# speed_zones = [accelerator_block, decelerator_block]
checkpoint_group = pygame.sprite.LayeredUpdates()
dspikes = [spike1, spike2, spike3, spike11, spike21, spike31, spike12, spike22, spike32]
checkpoint_group.add(checkpoint1, layer = 0)

# Create sprite groups
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(ground, layer = 1)
all_sprites.add(island1, layer = 0)
all_sprites.add(ground_under_ice, layer = 0)
all_sprites.add(test_block, layer = 0)
all_sprites.add(test_block2, layer = 0)
all_sprites.add(test_wall, layer = 0)
all_sprites.add(test_block3, layer = 0)
all_sprites.add(blue_portal, layer = 0)
all_sprites.add(orangw_portal, layer = 0)
all_sprites.add(fragilePlatform, layer = 0)
all_sprites.add(ladder1, layer = 1)
all_sprites.add(bridge_upon_lava, layer = 1)
# all_sprites.add(spike_left, layer = 0)
# all_sprites.add(spike_left2, layer = 0)
# all_sprites.add(water_pool, layer = 1)
all_sprites.add(dynamic_spike_platform, layer = 1)
all_sprites.add(spike1, layer = 0)
all_sprites.add(spike2, layer = 0)
all_sprites.add(spike3, layer = 0)
all_sprites.add(dynamic_spike_platform2, layer = 1)
all_sprites.add(spike11, layer = 0)
all_sprites.add(spike21, layer = 0)
all_sprites.add(spike31, layer = 0)
all_sprites.add(dynamic_spike_platform3, layer = 1)
all_sprites.add(spike12, layer = 0)
all_sprites.add(spike22, layer = 0)
all_sprites.add(spike32, layer = 0)
all_sprites.add(lava_pool, layer = 1)
# all_sprites.add(spike_up, layer = 0)
# all_sprites.add(spike_up2, layer = 0)
# all_sprites.add(spike_up3, layer = 0)
all_sprites.add(jump_Pad, layer = 1)
# all_sprites.add(accelerator_block, layer = 0)
# all_sprites.add(decelerator_block, layer = 0)
all_sprites.add(checkpoint1, layer = 0)
all_sprites.add(ice_plate, layer = 0)
all_sprites.add(player, layer = 2)
# all_sprites.add(test_wall1, layer = 0)
# all_sprites.add(test_wall2, layer = 0)
# all_sprites.add(elevatorupDown1, layer = 0)
# all_sprites.add(elevatorleftRight1, layer = 0)

running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Move elevators before resolving player collisions so the player can ride them naturally
    for elevator in dynamic_colliders:
        prev_x, prev_y = elevator.rect.x, elevator.rect.y
        if isinstance(elevator, ElevatorUpDown):
            updown_elevator_movement(elevator, elevator.range, dt)
        elif isinstance(elevator, ElevatorLeftRight):
            leftright_elevator_movement(elevator, elevator.range, dt)
        elevator.delta_x = elevator.rect.x - prev_x
        elevator.delta_y = elevator.rect.y - prev_y

        
    for dspike in dspikes:
        dynamic_spike_movement_based_on_timer(dspike, dt)
    # If the player was standing on a moving elevator last frame, carry them along with it
    if player.on_ground and player.ground in dynamic_colliders:
        player.pos.x += player.ground.delta_x
        player.pos.y += player.ground.delta_y
        player.rect.x = round(player.pos.x)
        player.rect.y = round(player.pos.y)

    # Player input & physics
    player.handle_input(dt)
    # apply_speed_zones(player, speed_zones)
    apply_gravity(player, dt)
    move_and_collide(player, colliders, dt, triggers)
    for portal in portals:
        teleport_player(player, portal)
    for portal in portals:
        cooldown_timer(portal, dt)
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
