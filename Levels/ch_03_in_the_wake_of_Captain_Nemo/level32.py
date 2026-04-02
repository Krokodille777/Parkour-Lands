# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, Water
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force

from maincamera import follow_player

class Level32:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(30, 70, 50, 50)
        self.ground = Ground(0, 150, 150, 1000)
        self.water_pool = Water(150, 160, 800, 850)
        self.ground2 = Ground(325, 0, 425, 700)
        self.wall = Ground (950, 0, 50, 1025)
        self.depth = Ground(150, 1010, 800, 250)
        self.island = Ground(875, 150, 75, 25)

        self.finish_level_trigger = FinishLevelTrigger(900, 50, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.water_pool)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.wall, self.depth, self.island)

        self.all_sprites.add(self.ground, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.ground2, layer = 2)
        self.all_sprites.add(self.wall, layer = 2)
        self.all_sprites.add(self.depth, layer = 2)
        self.all_sprites.add(self.island, layer = 2)
        

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



    