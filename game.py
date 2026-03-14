import pygame
from pygame.locals import *

from sprites import Ground, Player, Fan, JumpPad, Lava, Spike, Bridge, Water, Ladder, Accelerator, Decelerator, Checkpoint, FragileGround, ElevatorUpDown, ElevatorLeftRight, Ice, StartPortal, EndPortal, DynamicSpike
from sprites import DynamicSpikePlatform, Door, TrapDoor, Button, PushableBlock, AlterCreator, AlterPlayer, AlterRemover, PressTrap, SwingingVine
from physics import apply_gravity, move_and_collide,  crouching_adjustment, climb_ladder, squash_adjustment
from physics import jump_from_the_top_of_ladder, buoyant_force, apply_speed_zones
from maincamera import follow_player
from checkpoint import checkpoint_activation
from fragile_ground import fragile_ground_check, respawn_fragile_ground
from elevators import updown_elevator_movement, leftright_elevator_movement
from portals import link_portals, teleport_player, cooldown_timer, teleport_pushable_block
from dynamic_spike import dynamic_spike_movement_based_on_timer
from fans import apply_fan_effect, apply_fan_effect_to_block
from pushableBlock import push_the_block, triggers_check, block_collisions
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor
from press_trap import update_press_trap
pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()
player = Player(60, 250, 50, 50)
# Create sprite instances
ground = Ground(0, 700, 400, 900)

press_trap1 = PressTrap(250, 525, 150, 75, 180)


# Colliders list (everything the player can collide with)
colliders = [ground]  # Add all solid objects here
triggers = [press_trap1]   # Objects that trigger special interactions (like climbing or damage)
dynamic_colliders = []  # Moving solids like elevators go here
boxes = []
buttons = []

doors = []
trapdoors = []
water_group = pygame.sprite.LayeredUpdates()
fragile_grounds = []
ice_plate_group = pygame.sprite.LayeredUpdates()
portals = pygame.sprite.LayeredUpdates()
# portals.add(blue_portal, layer = 0)
# portals.add(orangw_portal, layer = 0)
# ice_plate_group.add(ice_plate, layer = 0)
# water_group.add(water_pool, layer = 0)
# speed_zones = [accelerator_block, decelerator_block]
checkpoint_group = pygame.sprite.LayeredUpdates()
dspikes = []
fans = []
# checkpoint_group.add(checkpoint1, layer = 1)

# Create sprite groups
all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(ground, layer = 1)
# all_sprites.add(island1, layer = 0)
# # all_sprites.add(ground_under_ice, layer = 0)
# all_sprites.add(test_block, layer = 0)
# all_sprites.add(test_block2, layer = 1)
# all_sprites.add(test_block4, layer = 1)
# all_sprites.add(test_block5, layer = 1)
# all_sprites.add(test_wall, layer = 0)
# all_sprites.add(test_block3, layer = 1)
# # all_sprites.add(blue_portal, layer = 1)
# # all_sprites.add(orangw_portal, layer = 1)
# # all_sprites.add(fragilePlatform, layer = 0)
# # all_sprites.add(ladder1, layer = 1)
# # all_sprites.add(bridge_upon_lava, layer = 1)
# # all_sprites.add(spike_down, layer = 1)
# # all_sprites.add(spike_down2, layer = 1)
# # all_sprites.add(spike_down3, layer = 1)
# # all_sprites.add(spike_down4, layer = 1)
# # all_sprites.add(spike_down5, layer = 1)
# # all_sprites.add(spike_down6, layer = 1)
# # all_sprites.add(spike_down7, layer = 1)
# # all_sprites.add(spike_down8, layer = 1)
# all_sprites.add(lava_pool, layer = 0)
# # all_sprites.add(water_pool, layer = 0)
# # all_sprites.add(fan_down, layer = 1)
# # all_sprites.add(fan_left, layer = 1)
# all_sprites.add(fan_right, layer = 1)
# all_sprites.add(button1, layer = 1)
# all_sprites.add(door1, layer = 1)
# all_sprites.add(trapdoor1, layer = 1)
# all_sprites.add(box, layer = 1)
# all_sprites.add(fan_up, layer = 1)
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
# all_sprites.add(spike_up, layer = 1)
# all_sprites.add(spike_up2, layer = 1)
# all_sprites.add(spike_up3, layer = 1)
# all_sprites.add(spike_up4, layer = 1)
# all_sprites.add(spike_up5, layer = 1)
# all_sprites.add(spike_up6, layer = 1)
# all_sprites.add(spike_up7, layer = 1)
# all_sprites.add(spike_up8, layer = 1)
# all_sprites.add(jump_Pad, layer = 1)
# all_sprites.add(accelerator_block, layer = 0)
# # all_sprites.add(decelerator_block, layer = 0)
# all_sprites.add(checkpoint1, layer = 0)
# all_sprites.add(ice_plate, layer = 0)
all_sprites.add(press_trap1, layer = 1)
all_sprites.add(player, layer = 2)
# all_sprites.add(test_wall1, layer = 0)
# all_sprites.add(test_wall2, layer = 0)
# # all_sprites.add(elevatorupDown1, layer = 0)
# # all_sprites.add(elevatorleftRight1, layer = 0)

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
    update_press_trap(press_trap1, dt)
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
    for b in boxes:
        push_the_block(player, b, dt)
        for fan in fans:
            apply_fan_effect_to_block(b, fan, dt)
        block_collisions(b, colliders, dt, triggers)
        triggers_check(b, triggers)
        for portal in portals:
            teleport_pushable_block(b, portal)
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
    squash_adjustment(player, colliders)
    climb_ladder(player, triggers)
    jump_from_the_top_of_ladder(player, triggers)
    buoyant_force(player, triggers) 
    press_button(player, boxes, buttons)
    link_button_to_door(buttons, doors)
    link_button_to_trapdoor(buttons, trapdoors)
    open_door_trapdoor(doors, trapdoors)
    checkpoint_activation(player, checkpoint_group)
    # fragile_ground_check(player, fragile_grounds, colliders, dt)
    respawn_fragile_ground(colliders, all_sprites, fragile_grounds, dt)
    

    # Press X to reset the level. It my happen if the player gets stuck or a valuable item gets lost in an unreachable place, so it's good to have a quick way to reset the level without closing the game.
    # it also relates to pushable blocks, as they can get pushed into unreachable places and cause softlocks, so being able to reset the level without closing the game is very helpful for testing and gameplay.
    




    offset_x, offset_y = follow_player(player, screen.get_width(), 2000, screen.get_height(), 1500)  # Assuming world width is 2000px and height is 1000px
    #Sky color
    screen.fill((119, 164, 237))
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

            
    pygame.display.flip()

pygame.quit()
