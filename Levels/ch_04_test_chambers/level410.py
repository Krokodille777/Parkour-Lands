
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, Water, TrapDoor, Door, Button, Spike, DynamicSpike, DynamicSpikePlatform, Checkpoint, PressTrap, StartPortal, EndPortal, Bridge, ControllableFan, Fan
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force
from pushableBlock import push_the_block, block_collisions
from portals import teleport_player, link_portals, teleport_pushable_block, cooldown_timer
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor, link_button_to_fan, activate_fan_from_button
from controllableFan import control_fan_from_button
from fans import apply_fan_effect, apply_fan_effect_to_block
from dynamic_spike import dynamic_spike_movement_based_on_timer
from press_trap import update_press_trap, apply_press_trap_effect
from checkpoint import checkpoint_activation
from maincamera import follow_player

class Level410:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(10, 50, 50, 50)
        self.ground = Ground(0, 100, 100, 50)
        self.water = Water(0, 110, 900, 890 )
        self.bottom = Ground(0, 900, 1000, 100)

        self.floor = Bridge(0 , 875, 225, 25)
        self.box = PushableBlock(25, 805, 65, 65)
        self.ceiling = Bridge(0, 725, 125, 25)
        self.press_trap = PressTrap(125, 725, 100, 50, 180)
        self.orange_portal = EndPortal(137.5, 800, 50, 75)

        self.checkpoint = Checkpoint(350, 850, 50, 50)

        self.button_for_trapdoor = Button(450, 865, 75, 35)

        self.cage_wall = Bridge(525, 750, 50, 150)
        self.trapDoor = TrapDoor(575, 755, 65, 25)
        self.trapDoor.linked_button = self.button_for_trapdoor
        self.cage_ceiling = Bridge(640, 750, 360, 50)
        self.finish_level_trigger = FinishLevelTrigger(890, 800, 50, 100)

        self.floor2 = Ground(625, 670, 150, 25)
        self.ceiling2 = Ground(675, 570, 65, 25)
        self.door = Door(650, 570, 25, 100)
        self.blue_portal = StartPortal(675, 595, 50, 75)

        self.corridor_wall = Bridge(415, 150, 50, 100)
        self.cf_right = ControllableFan(465, 155, 35, 75, (1, 0), 15000, 500)

        self.cf_left = ControllableFan(855, 300, 35, 75, (-1, 0), 35000, 700)

        self.corridor_floor = Bridge(410, 250, 325, 35)
        self.dsp1 = DynamicSpikePlatform(515, 250, 50, 35)
        self.dsu1 = DynamicSpike(515, 265, 25, 25, 180)
        self.dsu2 = DynamicSpike(540, 265, 25, 25, 180)
        self.corridor_floor2 = Bridge(400, 375, 500, 35)
        self.dsp2 = DynamicSpikePlatform(515, 375, 50, 35)
        self.dsd1 = DynamicSpike(515, 370, 25, 25, 0)
        self.dsd2 = DynamicSpike(540, 370, 25, 25, 0)
        self.corridor_wall3 = Bridge(400, 200, 25, 150)
        self.button_door = Button(425, 300, 35, 75)
        self.box2 = PushableBlock(510, 185, 65, 65)

        self.ground2 = Ground(400, 100, 300, 50)
        self.fan_up = Fan(750, 150, 75, 35, (0, 1), 1500, 500)
        self.corridor_wall2 = Bridge(890, 150, 50, 600)
        self.spike_left = Spike(865, 180, 25, 25, 90)
        self.spike_left2 = Spike(865, 205, 25, 25, 90)
        self.spike_left3 = Spike(865, 230, 25, 25, 90)
        self.button_cfan_right = Button(425, 65, 75, 35)
        self.button_cfan_left = Button(525, 65, 75, 35)
        self.wall = Bridge(700, 0, 300, 150)
        
        self.cf_left.linked_button = self.button_cfan_left
        self.cf_right.linked_button = self.button_cfan_right
        self.door.linked_button = self.button_door

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.orange_portal, self.press_trap, self.checkpoint, self.blue_portal, self.spike_left, self.spike_left2, self.spike_left3, self.dsd1, self.dsd2,  self.dsu1, self.dsu2, self.button_cfan_left, self.button_cfan_right, self.button_door, self.button_for_trapdoor)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box, self.wall,  self.floor, self.floor2, self.ceiling, self.ceiling2, self.bottom, self.cage_wall, self.cage_ceiling, self.trapDoor, self.door, self.corridor_wall, self.corridor_wall2, self.corridor_wall3, self.corridor_floor, self.corridor_floor2, self.dsp1, self.dsp2, self.box2, self.fan_up, self.cf_left, self.cf_right)

        self.all_sprites.add(self.ground, layer = 1)
        self.all_sprites.add(self.ground2, layer = 1)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.orange_portal, layer = 1)
        self.all_sprites.add(self.press_trap, layer = 1)
        self.all_sprites.add(self.checkpoint, layer = 1)
        self.all_sprites.add(self.blue_portal, layer = 1)
        self.all_sprites.add(self.cage_wall, layer = 1)
        self.all_sprites.add(self.cage_ceiling, layer = 1)
        self.all_sprites.add(self.trapDoor, layer = 1)
        self.all_sprites.add(self.floor2, layer = 1)
        self.all_sprites.add(self.ceiling2, layer = 1)
        self.all_sprites.add(self.door, layer = 1)
        self.all_sprites.add(self.cf_left, layer = 1)
        self.all_sprites.add(self.cf_right, layer = 1)
        self.all_sprites.add(self.corridor_wall, layer = 1)
        self.all_sprites.add(self.corridor_wall2, layer = 1)
        self.all_sprites.add(self.corridor_wall3, layer = 1)
        self.all_sprites.add(self.corridor_floor, layer = 1)
        self.all_sprites.add(self.corridor_floor2, layer = 1)
        self.all_sprites.add(self.dsp1, layer = 2)
        self.all_sprites.add(self.dsu1, layer = 1)
        self.all_sprites.add(self.dsu2, layer = 1)
        self.all_sprites.add(self.dsp2, layer = 2)
        self.all_sprites.add(self.dsd1, layer = 1)
        self.all_sprites.add(self.dsd2, layer = 1)
        self.all_sprites.add(self.button_door, layer = 1)
        self.all_sprites.add(self.box2, layer = 2)
        self.all_sprites.add(self.fan_up, layer = 1)
        self.all_sprites.add(self.spike_left, layer = 1)
        self.all_sprites.add(self.spike_left2, layer = 1)
        self.all_sprites.add(self.spike_left3, layer = 1)
        self.all_sprites.add(self.button_cfan_left, layer = 1)
        self.all_sprites.add(self.button_cfan_right, layer = 1)
        self.all_sprites.add(self.wall, layer = 1)
        self.all_sprites.add(self.water, layer = 0)
        self.all_sprites.add(self.bottom, layer = 1)
        self.all_sprites.add(self.button_for_trapdoor, layer = 1)
        self.all_sprites.add(self.floor, layer = 1)
        self.all_sprites.add(self.ceiling, layer = 1)
  

    def update(self, dt):
        self.player.handle_input()
        self.box.handle_input(dt)
        self.box2.handle_input(dt)
        player_in_water = self.player.rect.colliderect(self.water.rect)
        for ds in [self.dsu1, self.dsu2, self.dsd1, self.dsd2]:
            dynamic_spike_movement_based_on_timer(ds, dt)
        apply_gravity(self.player, dt)
        apply_press_trap_effect(self.player, self.press_trap, dt)
        apply_fan_effect(self.player, self.fan_up, dt, water_multiplier=0.5 if player_in_water else 1.0)
        apply_fan_effect_to_block(self.box2, self.fan_up, dt)
        control_fan_from_button(
            [self.button_cfan_left],
            [self.cf_left],
            self.player,
            [self.box2],
            dt,
            water_areas=[self.water],
        )
        control_fan_from_button(
            [self.button_cfan_right],
            [self.cf_right],
            self.player,
            [self.box2],
            dt,
            water_areas=[self.water],
        )
        link_portals(self.blue_portal, self.orange_portal)
        teleport_player(self.player, self.blue_portal)
        teleport_pushable_block(self.box, self.blue_portal)
        cooldown_timer(self.blue_portal, dt)
        teleport_player(self.player, self.orange_portal)
        teleport_pushable_block(self.box, self.orange_portal)
        cooldown_timer(self.orange_portal, dt)
        

        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water])
        press_button([self.player], [self.box2, self.box], [self.button_door, self.button_for_trapdoor, self.button_cfan_left, self.button_cfan_right])
        link_button_to_door([self.button_door], [self.door])
        link_button_to_trapdoor([self.button_for_trapdoor], [self.trapDoor])
        link_button_to_fan([self.button_cfan_left], [self.cf_left])
        link_button_to_fan([self.button_cfan_right], [self.cf_right])
        open_door_trapdoor([self.door], [self.trapDoor])
        activate_fan_from_button([self.button_cfan_left], [self.cf_left])
        activate_fan_from_button([self.button_cfan_right], [self.cf_right])

        checkpoint_activation(self.player, [self.checkpoint])
        update_press_trap(self.press_trap, dt)
        
                           
        push_the_block(self.player, self.box,  dt)
        block_collisions(self.box, self.colliders, dt, self.triggers)
        block_collisions(self.box2, self.colliders, dt, self.triggers)
    def draw(self, screen):
        offset_x, offset_y = follow_player(
            self.player,
            screen.get_width(),
            self.WORLD_WIDTH,
            screen.get_height(),
            self.WORLD_HEIGHT,
        )
        screen.fill((119, 164, 237))
        for sprite in self.all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

    def is_finished(self):
        return self.player.rect.colliderect(self.finish_level_trigger.rect)



    
