#Building levels, according to rrr.png

import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Lava
from physics import apply_gravity, move_and_collide
from maincamera import follow_player


class Level2:

    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground1 = Ground(0, 750, 300, 500)
        self.lava_pool1 = Lava(300, 900, 150, 500)
        self.island1 = Ground(450, 700, 150, 550)
        self.tip_cloud1 = TipCloud(450, 600, 200, 100, "Press Space/W/Up to Jump")
        self.lava_pool2 = Lava(600, 900, 150, 500)
        self.ground2 = Ground(750, 750, 300, 500)
        self.finish_level_trigger = FinishLevelTrigger(950, 650, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground1, self.lava_pool1, self.island1, self.lava_pool2, self.ground2)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ground1)
        self.all_sprites.add(self.lava_pool1)
        self.all_sprites.add(self.island1)
        self.all_sprites.add(self.tip_cloud1)
        self.all_sprites.add(self.lava_pool2)
        self.all_sprites.add(self.ground2)
        self.all_sprites.add(self.finish_level_trigger)

        

    def update(self, dt):
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt , self.triggers)
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