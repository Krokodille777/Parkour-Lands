# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, Water, Spike, Checkpoint, Fan
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force
from checkpoint import checkpoint_activation
from fans import apply_fan_effect
from maincamera import follow_player

class Level35:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(30, 70, 50, 50)
        self.ground = Ground(125, 0, 175, 590)
        self.ground2 = Ground(300, 0, 225, 400)
        self.ground3 = Ground(475, 0, 175, 500)
        self.water_pool = Water(0, 200, 900, 715)
        self.wall1 = Ground(0, 160, 50, 840)
        self.wall2 = Ground( 200, 160, 50, 540)
        self.floor = Ground(0, 790, 1000, 125)
        self.ceiling1 = Ground(200, 590, 100, 50)
        self.fan_right = Fan(50, 715, 25, 75, (1, 0), 3500, 750)
        self.small_wall = Ground(275, 400, 25, 200)
        self.small_wall2 = Ground(475, 400, 25, 200)
        self.checkpoint= Checkpoint(375, 450, 50, 50)

        self.ceiling2 = Ground(475, 500, 225, 125)
        self.spike_up = Spike(525, 625, 25, 25, 180)
        self.spike_down = Spike(600, 765, 25, 25, 0)
        self.spike_up2 = Spike(660, 625, 25, 25, 180)
        self.spike_down2 = Spike(660, 765, 25, 25, 0)
        self.fan_up = Fan(730, 765, 75,25, (0, 1), 2000, 700)

        self.wall3= Ground(650, 50, 50, 500)
        self.wall4 = Ground(850, 50, 200, 1000)
        self.spike_left = Spike(700, 500, 25, 25, 270)
        self.spike_right = Spike(825, 500, 25, 25, 90)
        self.spike_left2 = Spike(700, 350, 25, 25, 270)
        self.spike_right2 = Spike(825, 350, 25, 25, 90)
        self.finish_level_trigger = FinishLevelTrigger(700, 100, 150, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.water_pool, self.spike_down, self.spike_down2, self.spike_left, self.spike_right, self.spike_left2, self.spike_right2, self.checkpoint)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.ground3, self.wall1, self.wall2, self.wall3, self.wall4, self.floor, self.ceiling1, self.ceiling2, self.small_wall, self.small_wall2, self.fan_right, self.fan_up)

        self.all_sprites.add(self.ground, layer = 2)
        self.all_sprites.add(self.ground2, layer = 2)
        self.all_sprites.add(self.ground3, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.spike_up, layer = 2)
        self.all_sprites.add(self.spike_up2, layer = 2)
        self.all_sprites.add(self.spike_down, layer = 2)
        self.all_sprites.add(self.spike_down2, layer = 2)
        self.all_sprites.add(self.spike_left, layer = 2)
        self.all_sprites.add(self.spike_right, layer = 2)
        self.all_sprites.add(self.spike_left2, layer = 2)
        self.all_sprites.add(self.spike_right2, layer = 2)
        self.all_sprites.add(self.checkpoint, layer = 1)
        self.all_sprites.add(self.wall1, layer = 2)
        self.all_sprites.add(self.wall2, layer = 2)
        self.all_sprites.add(self.wall3, layer = 2)
        self.all_sprites.add(self.wall4, layer = 2)
        self.all_sprites.add(self.floor, layer = 2)
        self.all_sprites.add(self.ceiling1, layer = 2)
        self.all_sprites.add(self.ceiling2, layer = 2)
        self.all_sprites.add(self.small_wall, layer = 2)
        self.all_sprites.add(self.small_wall2, layer = 2)
        self.all_sprites.add(self.fan_right, layer = 2)
        self.all_sprites.add(self.fan_up, layer = 2)

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        player_in_water = self.player.rect.colliderect(self.water_pool.rect)
        water_multiplier = 0.5 if player_in_water else 1.0
        apply_fan_effect(self.player, self.fan_right, dt, water_multiplier=water_multiplier)
        apply_fan_effect(self.player, self.fan_up, dt, water_multiplier=water_multiplier)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water_pool])
        checkpoint_activation(self.player, [self.checkpoint])

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



    
