# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, Water, Bridge, Spike, Checkpoint, DynamicSpike, DynamicSpikePlatform, Fan, Lava, FinishLevelTrigger
from physics import apply_gravity, move_and_collide,  crouching_adjustment, squash_adjustment, buoyant_force

from dynamic_spike import dynamic_spike_movement_based_on_timer
from checkpoint import checkpoint_activation
from fans import apply_fan_effect
from maincamera import follow_player

class Level37:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(20, 0, 50, 50)
        self.ground = Ground(0, 50, 50, 500)
        self.bridge = Bridge(50, 50, 85, 25)
        self.ground2 = Ground(250, 0, 485, 300)
        self.checkpoint = Checkpoint (200, 200, 50, 50)
        self.block = Ground(200, 250, 50, 50)
        self.fan_right = Fan(50, 375, 25, 65, (1, 0), 10000, 750)


        self.dsp1 = DynamicSpikePlatform(225, 290, 75,35)
        self.dsu1 = DynamicSpike(225, 310, 25, 25, 180)
        self.dsu2 = DynamicSpike(250, 310, 25, 25, 180)
        self.dsu3 = DynamicSpike(275, 310, 25, 25, 180)
        self.dsp2 = DynamicSpikePlatform(350, 290, 75,35)
        self.dsu4 = DynamicSpike(350, 310, 25, 25, 180)
        self.dsu5 = DynamicSpike(375, 310, 25, 25, 180)
        self.dsu6 = DynamicSpike(400, 310, 25, 25, 180)

        self.dsp3 = DynamicSpikePlatform(250, 475, 75,35)
        self.dsd1 = DynamicSpike(250, 465, 25, 25, 0)
        self.dsd2 = DynamicSpike(275, 465, 25, 25, 0)
        self.dsd3 = DynamicSpike(300, 465, 25, 25, 0)
        self.floor = Ground(0, 500, 500, 500)
        self.lava = Lava (500, 510, 200, 500)
        self.wall1 = Ground(600, 300, 50, 100)
        self.block2 = Ground(650, 300, 85, 45)
        self.spike_right = Spike(735, 300, 35, 35, -90)
        self.ground3 = Ground(700, 500, 150, 500)
        self.wall2 = Ground(850, 0, 150, 800)
        self.fan_up = Fan(800, 475, 50, 25, (0, -1), 7000, 550)
        self.wall3 = Ground(710, 175, 25, 125)
        self.ceiling = Ground(710, 0, 175, 85)

        self.water1 = Water(50, 135, 685, 375)
        self.water2 = Water(735, 175, 115, 325)
        self.finish_level_trigger = FinishLevelTrigger(735, 85, 125, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.checkpoint, self.water1, self.water2, self.dsu1, self.dsu2, self.dsu3, self.dsu4, self.dsu5, self.dsu6, self.dsd1, self.dsd2, self.dsd3, self.spike_right,)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.bridge, self.ground2, self.block, self.fan_right, self.dsp1, self.dsp2, self.dsp3, self.floor, self.lava, self.wall1, self.block2,  self.ground3, self.wall2, self.fan_up, self.wall3, self.ceiling)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.player, layer = 4)
        self.all_sprites.add(self.bridge, layer = 0)
        self.all_sprites.add(self.ground2, layer = 2)
        self.all_sprites.add(self.checkpoint, layer = 2)
        self.all_sprites.add(self.block, layer = 2)
        self.all_sprites.add(self.fan_right, layer = 2)
        self.all_sprites.add(self.dsp1, layer = 3)
        self.all_sprites.add(self.dsu1, layer = 2)
        self.all_sprites.add(self.dsu2, layer = 2)
        self.all_sprites.add(self.dsu3, layer = 2)
        self.all_sprites.add(self.dsp2, layer = 3)
        self.all_sprites.add(self.dsu4, layer = 2)
        self.all_sprites.add(self.dsu5, layer = 2)
        self.all_sprites.add(self.dsu6, layer = 2)
        self.all_sprites.add(self.dsp3, layer = 3)
        self.all_sprites.add(self.dsd1, layer = 2)
        self.all_sprites.add(self.dsd2, layer = 2)
        self.all_sprites.add(self.dsd3, layer = 2)
        self.all_sprites.add(self.floor, layer = 2)
        self.all_sprites.add(self.lava, layer = 2)
        self.all_sprites.add(self.wall1, layer = 2)
        self.all_sprites.add(self.block2, layer = 2)
        self.all_sprites.add(self.spike_right, layer = 2)
        self.all_sprites.add(self.ground3, layer = 2)
        self.all_sprites.add(self.wall2, layer = 2)
        self.all_sprites.add(self.fan_up, layer = 2)
        self.all_sprites.add(self.wall3, layer = 2)
        self.all_sprites.add(self.ceiling, layer = 2)
        self.all_sprites.add(self.water1, layer = 1)
        self.all_sprites.add(self.water2, layer = 1)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
 
 
        

    def update(self, dt):    
        
        player_in_water1 = self.player.rect.colliderect(self.water1.rect)
        player_in_water2 = self.player.rect.colliderect(self.water2.rect)
        water_multiplier = 0.5 if player_in_water1 or player_in_water2 else 1.0
        apply_fan_effect(self.player, self.fan_right, dt, water_multiplier=water_multiplier)
        apply_fan_effect(self.player, self.fan_up, dt, water_multiplier=water_multiplier)
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        
        checkpoint_activation(self.player, [self.checkpoint])
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water1, self.water2])


        for ds in [self.dsu1, self.dsu2, self.dsu3, self.dsu4, self.dsu5, self.dsu6, self.dsd1, self.dsd2, self.dsd3]:
            dynamic_spike_movement_based_on_timer(ds, dt)
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



    