# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, Water, Ladder, TipCloud, Spike,  Fan
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force, climb_ladder, jump_from_the_top_of_ladder
from fans import apply_fan_effect

from maincamera import follow_player

class Level34:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(10, 800, 50, 50)
        self.ground = Ground(0, 850, 50, 50)
        self.floor = Ground (0, 850, 200, 150)
        self.ground2 = Ground (0, 750, 50, 50)
        self.water_pool = Water(0, 500, 200, 500)
        self.fan_down = Fan(115, 825, 85, 25, (0, -1), 5000, 550)
        self.wall = Ground(200, 200, 50, 750)

        self.floor2 = Ground(250, 175, 300, 25)
        self.ceiling = Ground(550, 50, 100, 25)
        self.fan_up = Fan(560, 75, 65, 25, (0, 1), 33000, 450)
        self.fan_left2 = Fan(625, 200, 25, 85, (-1, 0), 33000, 450)
        self.floor3 = Ground(375, 300, 275, 25)
        self.fan_right = Fan(250, 325, 25, 85, (1, 0), 33000, 450)
        self.floor4 = Ground(250, 410, 200, 25)

        self.platform1 = Ground(125, 200, 100, 50)
        self.ladder = Ladder(100, 200, 25, 100)

        self.wall2 = Ground(650, 0, 75, 700)
        self.ground3 = Ground(425, 500, 225, 25)
        self.fan_left = Fan(625, 415, 25, 85, (-1, 0), 33000, 450)

        self.ground4 = Ground(250, 650, 400, 50)
        self.spike_down = Spike(250, 595, 35, 65, 0)
        self.block1 = Ground(350, 600, 50, 50)
        self.spike_up = Spike(535, 525, 35, 60, 180)
        
        self.tip_cloud1 = TipCloud(100, 300, 250, 35, "Use the fan to reach the ladder!!")
        self.finish_level_trigger = FinishLevelTrigger(600, 550, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_down, self.spike_up, self.water_pool, self.ladder)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.floor, self.wall, self.fan_down, self.fan_left, self.platform1, self.wall2, self.ground3, self.ground4, self.block1, self.fan_up, self.fan_left2, self.fan_right, self.floor2, self.floor3, self.floor4, self.ceiling)

        self.all_sprites.add(self.ground, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.floor, layer = 2)
        self.all_sprites.add(self.ground2, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.fan_down, layer = 1)
        self.all_sprites.add(self.wall, layer = 2)
        self.all_sprites.add(self.platform1, layer = 2)
        self.all_sprites.add(self.ladder, layer = 2)
        self.all_sprites.add(self.wall2, layer = 2)
        self.all_sprites.add(self.ground3, layer = 2)
        self.all_sprites.add(self.fan_left, layer = 1)
        self.all_sprites.add(self.ground4, layer = 2)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.block1, layer = 2)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.tip_cloud1, layer = 4)
        self.all_sprites.add(self.fan_up, layer = 1)
        self.all_sprites.add(self.fan_left2, layer = 1)
        self.all_sprites.add(self.fan_right, layer = 1)
        self.all_sprites.add(self.floor2, layer = 2)
        self.all_sprites.add(self.floor3, layer = 2)
        self.all_sprites.add(self.floor4, layer = 2)
        self.all_sprites.add(self.ceiling, layer = 2)

        

    def update(self, dt):

        self.player.handle_input()
        apply_gravity(self.player, dt)
        player_in_water = self.player.rect.colliderect(self.water_pool.rect)
        apply_fan_effect(self.player, self.fan_down, dt, water_multiplier=2 if player_in_water else 1.0)
        apply_fan_effect(self.player, self.fan_left, dt, water_multiplier = 0.5)
        apply_fan_effect(self.player, self.fan_up, dt, water_multiplier=0.5)
        apply_fan_effect(self.player, self.fan_left2, dt, water_multiplier=0.5)
        apply_fan_effect(self.player, self.fan_right, dt, water_multiplier=0.5)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water_pool])
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



    
