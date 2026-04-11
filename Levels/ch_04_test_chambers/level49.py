
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, Bridge, FinishLevelTrigger, Door, TrapDoor, PushableBlock, Button, JumpPad, StartPortal, EndPortal, ControllableFan
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from pushableBlock import push_the_block, block_collisions
from portals import teleport_player, link_portals, teleport_pushable_block, cooldown_timer
from button_door_trap import press_button, link_button_to_fan, activate_fan_from_button, link_button_to_trapdoor, open_door_trapdoor
from controllableFan import  control_fan_from_button
from maincamera import follow_player

class Level49:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 400, 500)

        self.box = PushableBlock(305, 280, 85, 85)

        self.ground2 = Ground(400, 900, 140, 500)
        self.trapdoor = TrapDoor(785, 750, 75, 20)
        self.blue_portal = StartPortal(400, 800, 45, 100)
        self.jump_pad = JumpPad(540, 875, 45, 40, -1000)
        self.ground3 = Ground(540, 915, 400, 310)
        self.ground4 = Ground(585, 750, 200, 500)
        self.ground5 = Ground(785, 1000, 75, 300)
        self.ground6 = Ground(860, 750, 140, 500)
        self.door = Door (1555, 650, 50, 100)
        self.button2 = Button(205, 365, 75, 35)

        self.room_wall = Bridge(150, 0, 50, 450)
        self.room_floor = Bridge(150, 400, 400, 50)
        self.room_wall2 = Bridge(500, 0, 50, 450)
        self.button1 = Button(305, 365, 75, 35)
        self.orange_portal = EndPortal(445, 300, 50, 100)
        link_portals(self.blue_portal, self.orange_portal)
        self.rock = Ground(550, 0, 450, 650)
        self.wall2 = Ground(935, 650, 75, 100)
        self.cfan_left = ControllableFan(860, 655, 75, 90, (-1, 0), 25000, 350)


        self.trapdoor.linked_button = self.button2
      
        self.door.linked_button = self.button2
        self.cfan_left.linked_button = self.button1
        self.tip_cloud = TipCloud(65, 450, 175, 120, "Click the button \n to activate the fan!")
        self.finish_level_trigger = FinishLevelTrigger(790, 825, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.blue_portal, self.orange_portal, self.button1, self.button2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.jump_pad, self.ground3, self.ground4, self.ground5, self.ground6, self.box, self.room_wall, self.room_floor, self.room_wall2, self.rock, self.wall2, self.trapdoor, self.door, self.cfan_left)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.tip_cloud, layer = 3)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.blue_portal, layer = 1)
        self.all_sprites.add(self.jump_pad, layer = 1)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.ground5, layer = 0)
        self.all_sprites.add(self.ground6, layer = 0)
        self.all_sprites.add(self.door, layer = 1)
        self.all_sprites.add(self.button1, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.room_wall, layer = 0)
        self.all_sprites.add(self.room_floor, layer = 0)
        self.all_sprites.add(self.room_wall2, layer = 0)
        self.all_sprites.add(self.orange_portal, layer = 1)
        self.all_sprites.add(self.rock, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.cfan_left, layer = 1)
        
        

    def update(self, dt):
        self.player.handle_input()
        self.box.handle_input(dt)
        apply_gravity(self.player, dt)
        control_fan_from_button([self.button1], [self.cfan_left], self.player, self.box, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        teleport_player(self.player, self.blue_portal)
        teleport_player(self.player, self.orange_portal)
        teleport_pushable_block(self.box, self.blue_portal)
        teleport_pushable_block(self.box, self.orange_portal)
        cooldown_timer(self.blue_portal, dt)
        cooldown_timer(self.orange_portal, dt)
        
        press_button([self.player], self.colliders, [self.button1, self.button2])
        link_button_to_trapdoor([self.button2], [self.trapdoor])
        link_button_to_fan([self.button1], [self.cfan_left])
        open_door_trapdoor([self.door], [self.trapdoor])
        activate_fan_from_button([self.button1], [self.cfan_left])
        push_the_block(self.player, self.box,  dt)
        block_collisions(self.box, self.colliders, dt, self.triggers)
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



    