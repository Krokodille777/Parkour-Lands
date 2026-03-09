import pygame
from pygame.locals import *

from sprites import Ground, Player, Fan, JumpPad, Lava, Spike, Bridge, Water, Ladder, Accelerator, Decelerator, Checkpoint, FragileGround, ElevatorUpDown, ElevatorLeftRight, Ice, StartPortal, EndPortal, DynamicSpike
from sprites import DynamicSpikePlatform
from physics import apply_gravity, move_and_collide,  crouching_adjustment, climb_ladder
from physics import jump_from_the_top_of_ladder, buoyant_force, apply_speed_zones
from maincamera import follow_player
from checkpoint import checkpoint_activation
from fragile_ground import fragile_ground_check, respawn_fragile_ground
from elevators import updown_elevator_movement, leftright_elevator_movement
from portals import link_portals, teleport_player, cooldown_timer, teleport_pushable_block
from dynamic_spike import dynamic_spike_movement_based_on_timer
from fans import apply_fan_effect, apply_fan_effect_to_block
from pushableBlock import push_the_block, triggers_check, block_collisions, on_ice, use_jumppad
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(0, 300, 200, 1000)
bridge_upon_lava = Bridge(200, 300, 100, 20)
water_pool = Water(200, 400, 1100, 800)
water_pool.image.fill((0, 101, 255))    # Blue color for water
test_wall = Ground(1300, 200, 40, 1300)
test_wall.image.fill((128, 128, 128))  # Gray color for test wall   



island1 = Ground(200, 1200, 1100, 50)

test_wall2 = Ground(650, 100, 415, 850)
test_wall2.image.fill((128, 128, 128))  # Gray color for test wall2
test_block2 = Ground(500, 425, 150, 50)
fan_down = Fan(510, 450, 125, 25, (0, 1))   # Fan blowing downwards
player = Player(10, 90, 50, 50)
test_block4 = Ground(500, 800, 150, 50)
checkpoint1 = Checkpoint(250, 887, 50, 50)

fan_left = Fan(625, 675, 25, 125, (-1, 0))   # Fan blowing left
test_block4.image.fill((150, 75, 0))   # Brown color for test block 4
fan_right = Fan(200, 1025, 25, 125, (1, 0))   # Fan blowing right
spike_up = Spike(650, 950, 50, 50, 180)
spike_up2 = Spike(702.5, 950, 50, 50, 180)
spike_up3 = Spike(754.5, 950, 50, 50, 180)
spike_up4 = Spike(806.5, 950, 50, 50, 180)
spike_up5 = Spike(858.5, 950, 50, 50, 180)
spike_up6 = Spike(910.5, 950, 50, 50, 180)
spike_up7 = Spike(962.5, 950, 50, 50, 180)
spike_up8 = Spike(1014.5, 950, 50, 50, 180)

spike_down = Spike(650, 1150, 50, 50, 0)
spike_down2 = Spike(702.5, 1150, 50, 50, 0)
spike_down3 = Spike(754.5, 1150, 50, 50, 0)
spike_down4 = Spike(806.5, 1150, 50, 50, 0)
spike_down5 = Spike(858.5, 1150, 50, 50, 0)
spike_down6 = Spike(910.5, 1150, 50, 50, 0)
spike_down7 = Spike(962.5, 1150, 50, 50, 0)
spike_down8 = Spike(1014.5, 1150, 50, 50, 0)


fan_up = Fan(1157.25, 1200, 125, 25, (0, -1))   # Fan blowing upwards
# ice_plate = Ice(550, 700, 230, 50)
# ground_under_ice = Ground(550, 750, 230, 500)
# jump_Pad = JumpPad(1175, 680, 60, 20, launch_vel = -1700)
# jump_Pad.image.fill((255, 255, 0))   # Yellowish

# # Test block: short enough to jump over (50px tall)

# dynamic_spike_platform = DynamicSpikePlatform(75, 700, 77, 30)
# spike1 = DynamicSpike(75, 695, 30, 30, 0)
# spike2 = DynamicSpike(99, 695, 30, 30, 0)
# spike3 = DynamicSpike(122, 695, 30, 30, 0)


# fragilePlatform = FragileGround(875, 675, 50, 50)
test_block = Ground(1050, 275, 125, 25)





# elevatorleftRight1 = ElevatorLeftRight(972, 400, 75, 25, 200)

test_block3 = Ground(200, 515, 200, 150)

orangw_portal = EndPortal(90, 225, 50, 75)


blue_portal = StartPortal(1050, 200, 50, 75)
link_portals(blue_portal, orangw_portal)



# elevatorupDown1 = ElevatorUpDown(500, 300, 75, 25, 200)


# ladder1 = Ladder(250, 515, 20, 150)





# lava_pool = Lava(780, 800, 320, 500)
# lava_pool.image.fill((250, 112, 47))    # Orange color for lava



# Colliders list (everything the player can collide with)
colliders = [ground, test_block3, test_block2, test_wall2, test_block4, test_wall, test_block, island1, bridge_upon_lava, fan_down, fan_left, fan_right, fan_up]  # Add all solid objects here
triggers = [spike_down, spike_down2, spike_down3, spike_down4, spike_down5, spike_down6, spike_down7, spike_down8, spike_up, spike_up2, spike_up3, spike_up4, spike_up5, spike_up6, spike_up7, spike_up8, water_pool]   # Objects that trigger special interactions (like climbing or damage)
dynamic_colliders = [fan_down, fan_left, fan_right, fan_up]  # Moving solids like elevators go here

water_group = pygame.sprite.LayeredUpdates()
fragile_grounds = []
ice_plate_group = pygame.sprite.LayeredUpdates()
portals = pygame.sprite.LayeredUpdates()
portals.add(blue_portal, layer = 0)
portals.add(orangw_portal, layer = 0)
# ice_plate_group.add(ice_plate, layer = 0)
water_group.add(water_pool, layer = 0)
# speed_zones = [accelerator_block, decelerator_block]
checkpoint_group = pygame.sprite.LayeredUpdates()
dspikes = []
fans = [fan_down, fan_left, fan_right, fan_up]
checkpoint_group.add(checkpoint1, layer = 1)

# Create sprite groups
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(ground, layer = 1)
all_sprites.add(island1, layer = 0)
# all_sprites.add(ground_under_ice, layer = 0)
all_sprites.add(test_block, layer = 0)
all_sprites.add(test_block2, layer = 1)
all_sprites.add(test_block4, layer = 1)
all_sprites.add(test_wall, layer = 0)
all_sprites.add(test_block3, layer = 1)
all_sprites.add(blue_portal, layer = 1)
all_sprites.add(orangw_portal, layer = 1)
# all_sprites.add(fragilePlatform, layer = 0)
# all_sprites.add(ladder1, layer = 1)
all_sprites.add(bridge_upon_lava, layer = 1)
all_sprites.add(spike_down, layer = 1)
all_sprites.add(spike_down2, layer = 1)
all_sprites.add(spike_down3, layer = 1)
all_sprites.add(spike_down4, layer = 1)
all_sprites.add(spike_down5, layer = 1)
all_sprites.add(spike_down6, layer = 1)
all_sprites.add(spike_down7, layer = 1)
all_sprites.add(spike_down8, layer = 1)
all_sprites.add(water_pool, layer = 0)
all_sprites.add(fan_down, layer = 1)
all_sprites.add(fan_left, layer = 1)
all_sprites.add(fan_right, layer = 1)
all_sprites.add(fan_up, layer = 1)
# all_sprites.add(dynamic_spike_platform, layer = 1)
# all_sprites.add(spike1, layer = 0)
# all_sprites.add(spike2, layer = 0)
# all_sprites.add(spike3, layer = 0)
# all_sprites.add(dynamic_spike_platform2, layer = 1)
# all_sprites.add(spike11, layer = 0)
# all_sprites.add(spike21, layer = 0)
# all_sprites.add(spike31, layer = 0)
# all_sprites.add(dynamic_spike_platform3, layer = 1)
# all_sprites.add(spike12, layer = 0)
# all_sprites.add(spike22, layer = 0)
# all_sprites.add(spike32, layer = 0)
# all_sprites.add(lava_pool, layer = 1)
all_sprites.add(spike_up, layer = 1)
all_sprites.add(spike_up2, layer = 1)
all_sprites.add(spike_up3, layer = 1)
all_sprites.add(spike_up4, layer = 1)
all_sprites.add(spike_up5, layer = 1)
all_sprites.add(spike_up6, layer = 1)
all_sprites.add(spike_up7, layer = 1)
all_sprites.add(spike_up8, layer = 1)
# all_sprites.add(jump_Pad, layer = 1)
# all_sprites.add(accelerator_block, layer = 0)
# all_sprites.add(decelerator_block, layer = 0)
all_sprites.add(checkpoint1, layer = 0)
# all_sprites.add(ice_plate, layer = 0)
all_sprites.add(player, layer = 2)
# all_sprites.add(test_wall1, layer = 0)
all_sprites.add(test_wall2, layer = 0)
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
    for fan in fans:
        apply_fan_effect(player, fan, dt)
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
