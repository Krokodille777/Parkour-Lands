# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, JumpPad, Spike, Bridge
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment

from maincamera import follow_player

class Level22:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(40, 650, 50, 50)
        self.ground = Ground(0, 750, 800, 500)
        self.spike_down = Spike(125, 710, 35, 40, 0)
        self.jump_pad = JumpPad(625, 740, 50, 25, -2500)
        self.bridge = Bridge(0, 625, 500, 20)
        self.block3 = Ground(475, 645, 50, 35)
        self.jump_pad2 = JumpPad(55, 600, 50, 25, -1700)
        self.wall = Ground(-5, 0, 50, 500)
        self.block = Ground(0, 300, 35, 45)
        self.block2 = Ground(110, 210, 500, 320)
        self.platform = Ground(605, 210, 200, 50)

        self.spike_up1 = Spike(605, 260, 35, 50, 180)
        self.spike_up2 = Spike(640, 260, 35, 50, 180)
        self.spike_up3 = Spike(675, 260, 35, 50, 180)
        self.wall2 = Ground(710, 260, 75, 500)
        self.finish_level_trigger = FinishLevelTrigger(700, 115, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_up2, self.spike_up1, self.spike_up3, self.spike_down)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.wall, self.block, self.block2, self.block3, self.platform, self.wall2, self.bridge, self.jump_pad, self.jump_pad2)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_up1, layer = 1)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.spike_up3, layer = 1)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.block, layer = 0)
        self.all_sprites.add(self.block2, layer = 0)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.jump_pad, layer = 0)
        self.all_sprites.add(self.jump_pad2, layer = 0)
        self.all_sprites.add(self.bridge, layer = 0)
        self.all_sprites.add(self.block3, layer = 0)

        
        

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
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


