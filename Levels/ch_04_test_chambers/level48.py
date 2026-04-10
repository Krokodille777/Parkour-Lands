
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, PushableBlock, Fan, Ladder, Door, TrapDoor, JumpPad, Button, Bridge
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from pushableBlock import push_the_block, block_collisions
from button_door_trap import press_button, link_button_to_door, open_door_trapdoor
from fans import apply_fan_effect, apply_fan_effect_to_block
from maincamera import follow_player

class Level48:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(500, 250, 50, 50)
        self.ground = Ground(0, 750, 1000, 500)

        self.box = PushableBlock(900, 465, 85, 85)

        self.ground2 = Ground(750, 600, 250, 500)
        self.ground3 = Ground(875, 550, 125, 50)


        self.fan_up = Fan(0, 750, 100, 50, (0, -1), 10000, 500)
        self.box2 = PushableBlock(15, 665, 85, 85)

        self.island = Ground(230, 400, 100, 25)
        self.jump_pad = JumpPad(255, 375, 50, 25, -1200)
        self.ladder = Ladder(335, 400, 35, 265)

        self.floor = Ground(0, 200, 150, 50)
        self.bridge = Bridge(150, 200, 50, 15)
        self.button1 = Button(25, 165, 15, 35)
        self.button2 = Button(135, 165, 15, 35)

        self.floor2 = Ground(675, 350, 325, 50)
        self.ceiling = Ground(775, 225, 225, 25)
        self.door = Door(780, 250, 50, 100)
        self.door2 = Door(880, 250, 50, 100)
        self.door.linked_button = self.button1
        self.door2.linked_button = self.button2
        self.finish_level_trigger = FinishLevelTrigger(950, 250, 50, 100)
        self.trapdoor = TrapDoor(11825, 350, 50, 25)
        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.button1, self.button2, self.ladder)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box, self.ground3, self.island, self.jump_pad, self.box2, self.fan_up, self.floor, self.bridge, self.floor2, self.ceiling, self.door, self.door2, self.trapdoor)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.island, layer = 0)
        self.all_sprites.add(self.jump_pad, layer = 2)
        self.all_sprites.add(self.box2, layer = 2)
        self.all_sprites.add(self.fan_up, layer = 1)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.bridge, layer = 0)
        self.all_sprites.add(self.button1, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.floor2, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.door, layer = 1)
        self.all_sprites.add(self.door2, layer = 1)
        self.all_sprites.add(self.ladder, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)


    def update(self, dt):
        self.player.handle_input()
        self.box.handle_input()
        self.box2.handle_input()
        apply_gravity(self.player, dt)
        apply_fan_effect(self.player, self.fan_up, dt)
        apply_fan_effect_to_block(self.box, self.fan_up, dt)
        apply_fan_effect_to_block(self.box2, self.fan_up, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        press_button([self.player], self.colliders, [self.button1, self.button2])
        link_button_to_door([self.button1], [self.door])
        link_button_to_door([self.button2], [self.door2])

        open_door_trapdoor([self.door], [self.trapdoor])
        open_door_trapdoor([self.door2], [self.trapdoor])

        push_the_block(self.player, self.box,  dt)
        push_the_block(self.player, self.box2,  dt)
       
        block_collisions(self.box, self.colliders, dt, self.triggers)
        block_collisions(self.box2, self.colliders, dt, self.triggers)
        climb_ladder(self.player, [self.ladder])
        jump_from_the_top_of_ladder(self.player, [self.ladder])
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



    