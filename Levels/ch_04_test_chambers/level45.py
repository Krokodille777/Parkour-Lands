
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, Door, PushableBlock, Button, Ladder, Bridge, Fan, Lava, TrapDoor, Spike
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from button_door_trap import press_button, link_button_to_trapdoor, open_door_trapdoor
from fans import  apply_fan_effect_to_block
from pushableBlock import push_the_block, block_collisions
from maincamera import follow_player

class Level45:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(150, 700, 50, 50)
        self.ground = Ground(0, 750, 250, 500)
        self.lava = Lava(250, 850, 450, 500)
        self.ledge = Bridge(450, 845, 50, 75)
        self.trapdoor = TrapDoor(250, 750, 450, 25)
        self.button = Button(715, 715, 100, 35)
        self.trapdoor.linked_button = self.button
        self.box1 = PushableBlock(720, 665, 85, 85)
        self.ground2 = Ground(700, 750, 300, 500)


        self.wall = Ground(0, 300, 50, 450)
        self.ladder = Ladder(55, 500, 35, 100)
        self.ceiling = Ground(50, 300, 325, 35)
        self.floor = Ground(85, 500, 255, 25)
        self.wall2 = Ground(340, 335, 35, 250 )
        self.button2 = Button(305, 400, 35, 75)
        self.button3 = Button(150, 465, 75, 35)
        self.button4 = Button(235, 465, 75, 35)


        self.box2 = PushableBlock(390, 195, 85, 85)
        self.corridor_wall = Bridge(480, 245, 35, 75)
        self.trapdoor2 = TrapDoor(375,295, 105, 25)
        self.trapdoor2.linked_button = self.button2
        self.fan_right = Fan(375, 345, 15, 75, (1, 0), 25000, 2500)
        self.corridoe_ceiling = Bridge(480, 300, 150, 25)
        self.corridor_floor=Bridge(375, 425, 150, 25)
        self.trapdoor3 = TrapDoor(610, 340, 25, 75)
        self.ground3 = Ground(675, 300, 350, 200)
        self.spike_left = Spike(635, 340, 40, 40, 90)
        self.spike_left2 = Spike(635, 380, 40, 40, 90)
        self.trapdoor3.linked_button = self.button3
        self.corridor_wall2 = Bridge(580, 300, 55, 40)
        self.fan_left = Fan(645, 450, 35, 75, (-1, 0), 25000, 2500)
        self.corridor_floor2  = Bridge(525, 535, 150, 25)
        self.corridor_wall3 = Bridge(395, 450, 25, 175)
        self.trapdoor4 = TrapDoor(420, 535, 105, 25)
        self.trapdoor4.linked_button = self.button4
        self.door = Door(500, 1700, 50, 100)

        self.finish_level_trigger = FinishLevelTrigger(900, 500, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.lava, self.spike_left, self.spike_left2, self.ladder, self.button, self.button2, self.button3, self.button4)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box1, self.ledge, self.trapdoor, self.wall, self.ceiling, self.floor, self.wall2, self.box2, self.corridor_wall, self.trapdoor2, self.fan_right, self.corridoe_ceiling, self.corridor_floor, self.trapdoor3, self.ground3, self.corridor_wall2, self.fan_left, self.corridor_floor2, self.corridor_wall3, self.trapdoor4)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.box1, layer = 2)
        self.all_sprites.add(self.ledge, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.lava, layer = 0)
        self.all_sprites.add(self.button, layer = 1)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.ladder, layer = 1)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.button3, layer = 1)
        self.all_sprites.add(self.button4, layer = 1)
        self.all_sprites.add(self.box2, layer = 2)
        self.all_sprites.add(self.corridor_wall, layer = 0)
        self.all_sprites.add(self.trapdoor2, layer = 1)
        self.all_sprites.add(self.fan_right, layer = 0)
        self.all_sprites.add(self.corridoe_ceiling, layer = 0)
        self.all_sprites.add(self.corridor_floor, layer = 0)
        self.all_sprites.add(self.trapdoor3, layer = 1)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.spike_left, layer = 0)
        self.all_sprites.add(self.spike_left2, layer = 0)
        self.all_sprites.add(self.corridor_wall2, layer = 0)
        self.all_sprites.add(self.fan_left, layer = 0)
        self.all_sprites.add(self.corridor_floor2, layer = 0)
        self.all_sprites.add(self.corridor_wall3, layer = 0)
        self.all_sprites.add(self.trapdoor4, layer = 1)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        
        

    def update(self, dt):
        self.player.handle_input()
        self.box2.handle_input(dt)
        apply_gravity(self.player, dt)
        apply_fan_effect_to_block(self.box2, self.fan_right, dt)
        apply_fan_effect_to_block(self.box2, self.fan_left, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        climb_ladder(self.player, [self.ladder])
        jump_from_the_top_of_ladder(self.player, [self.ladder])


        press_button([self.player], self.colliders, [self.button, self.button2, self.button3, self.button4])
        link_button_to_trapdoor([self.button], [self.trapdoor])
        link_button_to_trapdoor([self.button2], [self.trapdoor2])
        link_button_to_trapdoor([self.button3], [self.trapdoor3])
        link_button_to_trapdoor([self.button4], [self.trapdoor4])
        open_door_trapdoor([self.door], [self.trapdoor])
        open_door_trapdoor([self.door], [self.trapdoor2])
        open_door_trapdoor([self.door], [self.trapdoor3])
        open_door_trapdoor([self.door], [self.trapdoor4])

        push_the_block(self.player, self.box1,  dt)
       
        block_collisions(self.box1, self.colliders, dt, self.triggers)
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



    