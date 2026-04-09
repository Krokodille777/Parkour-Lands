
import pygame
from pygame.locals import *
from sprites import Player, Ground,FinishLevelTrigger, PushableBlock, FragileGround, TipCloud, Bridge, Button, Door, TrapDoor
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from pushableBlock import push_the_block, block_collisions, respawn_block
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor
from fragile_ground import fragile_ground_check, respawn_fragile_ground, trigger_fragile_ground
from maincamera import follow_player

class Level43:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 650, 50, 50)
        self.ground = Ground(0, 750, 1000, 500)
        self.button = Button(725, 715, 75, 35)
        self.ground2 = Ground(850, 700, 50, 50)
        self.ground3 = Ground(900, 675, 175, 75)
        self.door = Door(905, 575, 50, 100)
        self.door.linked_button = self.button
        self.wall = Ground(900, 0, 75, 575)



        self.platform = Bridge(10, 625, 85, 25)
        self.button2 = Button(15, 590, 75, 35)
        self.fg = FragileGround(110, 650, 50, 50)


        self.wall2 = Ground(290, 300, 50, 85)
        self.block1 = Ground(285, 385, 60, 35)
        self.trapdoor = TrapDoor(345, 390, 110, 25)
        self.trapdoor.linked_button = self.button2  
        self.block2= Ground(440, 385, 60, 35)
        self.wall3 = Ground(445, 300, 50, 85)
        self.box = PushableBlock(350, 185, 85, 85)
        self.tip_cloud = TipCloud(65, 0, 175, 120, "To unlock the door (or trapdoor), \n the button should be pressed.")
        self.finish_level_trigger = FinishLevelTrigger(1025, 575, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.button, self.button2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box, self.platform, self.ground3, self.door, self.wall, self.fg, self.wall2, self.block1, self.trapdoor, self.block2, self.wall3)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.button, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.fg, layer = 1)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.wall2, layer = 1)
        self.all_sprites.add(self.block1, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.block2, layer = 1)
        self.all_sprites.add(self.wall3, layer = 1)
        self.all_sprites.add(self.door, layer = 1)
        
        

    def update(self, dt):
        trigger_fragile_ground(self.player, self.box, [self.fg])
        fragile_ground_check(self.player, self.box, [self.fg] ,self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites, [self.fg], dt)
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        push_the_block(self.player, self.box,  dt)
        block_collisions(self.box, self.colliders, dt, self.triggers)
        press_button([self.player], self.colliders, [self.button, self.button2])
        link_button_to_door([self.button], [self.door])
        link_button_to_trapdoor([self.button2], [self.trapdoor])
        open_door_trapdoor([self.door], [self.trapdoor])

        respawn_block(self.box, self.colliders, self.triggers, dt)

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



    