# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, Water, Spike
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force

from maincamera import follow_player

class Level33:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(10, 300, 50, 50)
        self.ground = Ground(0, 0, 100, 250)
        self.ground2 = Ground(0, 350, 100, 650)
        self.floor = Ground(100, 900, 900, 150)
        self.ceiling = Ground(100, 0, 900, 50)
        self.water_pool = Water(0, 10, 1000, 1000)
        

        self.block1 = Ground(275, 225, 125, 125)
        self.block2 = Ground(275, 675, 125, 125)
        self.block3 = Ground(625, 50, 125, 35)
        self.spike_up = Spike(625, 85, 125, 65, 180)
        self.block4 = Ground(625, 450, 125, 125)
        self.block5 = Ground(625, 865, 125, 35)
        self.spike_down = Spike(625, 800, 125, 65, 0)

        self.ground3 = Ground(950, 0, 100, 550)
        self.finish_level_trigger = FinishLevelTrigger(1000, 550, 50, 100)
        self.ground4 = Ground(950, 650, 100, 350)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.water_pool, self.spike_up, self.spike_down,)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.floor, self.ceiling, self.block1, self.block2, self.block3, self.block4, self.block5,  self.ground3, self.ground4)

        self.all_sprites.add(self.ground, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 2)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.ground2, layer = 2)
        self.all_sprites.add(self.floor, layer = 2)
        self.all_sprites.add(self.ceiling, layer = 2)
        self.all_sprites.add(self.block1, layer = 2)
        self.all_sprites.add(self.block2, layer = 2)
        self.all_sprites.add(self.block3, layer = 2)
        self.all_sprites.add(self.block4, layer = 2)
        self.all_sprites.add(self.block5, layer = 2)
        self.all_sprites.add(self.spike_up, layer = 2)
        self.all_sprites.add(self.spike_down, layer = 2)
        self.all_sprites.add(self.ground3, layer = 2)
        self.all_sprites.add(self.ground4, layer = 2)
  

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water_pool])
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



    