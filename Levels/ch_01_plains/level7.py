# Level 7 of Chapter 1 - Plains : Small Exam Level
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, Lava, Bridge, JumpPad, Ice
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from maincamera import follow_player

class Level7:

    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 150, 560)
        self.ground2 = Ground(150, 800, 90, 75)
        self.jump_pad = JumpPad(185, 770, 50, 25, -1500)
        self.ice = Ice(240, 800, 250, 90)
        self.lava_pool = Lava(490, 815, 280, 90)
        
        self.platform = Bridge(325, 375, 90, 35)
        self.block1 = Ground(415, 300, 125, 125)
        self.block2 = Ground(465, 235, 75, 70)


        self.wall1 = Ground(615, 45, 50, 175)
        self.ground3 = Ground(615, 220, 450, 80)
        self.ice2 = Ice(535,335, 140, 45)
        self.ground4 = Ground(675, 335, 155, 45)
        self.wall2 = Ground(795, 375, 35, 145)
        self.wall3 = Ground(875, 300, 35, 215)
        self.island = Ground(770, 750, 150, 500)
        self.finish_level_trigger = FinishLevelTrigger(845, 650, 40, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.jump_pad, self.ice, self.lava_pool, self.island, self.platform, self.block1, self.block2, self.wall1, self.ground3, self.ice2, self.ground4, self.wall2, self.wall3)

        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.jump_pad, layer = 1)
        self.all_sprites.add(self.ice, layer = 1)
        self.all_sprites.add(self.lava_pool, layer = 1)
        self.all_sprites.add(self.platform, layer = 1)
        self.all_sprites.add(self.block1, layer = 1)
        self.all_sprites.add(self.block2, layer = 1)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.ice2, layer = 1)
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.wall3, layer = 0)
        self.all_sprites.add(self.island, layer = 0)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)


    def update(self, dt):
            apply_gravity(self.player, dt)
            move_and_collide(self.player, self.colliders, dt, self.triggers)
            crouching_adjustment(self.player, self.colliders)
            squash_adjustment(self.player, self.colliders)
            self.player.handle_input()
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
