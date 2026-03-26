# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Spike, Ladder, Lava
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder

from maincamera import follow_player

class Level23:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 700, 50, 50)
        self.ground = Ground(0, 750, 750, 500)
        self.lava_pool = Lava(740, 750, 500, 500)
        self.ladder1 = Ladder(500, 550, 50, 200)
        self.platform_left1 = Ground(350, 550, 150, 35)
        self.spike_up1 = Spike(350, 585, 35, 50, 180)
        self.platform_right1 = Ground(550, 550, 150, 35)
        self.spike_up2 = Spike(665, 585, 35, 50, 180)
        self.ladder_left = Ladder(350, 350, 50, 200)
        self.platform_left2 = Ground(150, 350, 100, 35)
        self.ladder_right = Ladder(650, 350, 50, 200)
        self.platform_right2 = Ground(800, 350, 100, 35)
        self.platform_mid = Ground(400, 350, 250, 35)
        self.finish_level_trigger = FinishLevelTrigger(840, 250, 50, 100)
        self.tip_cloud = TipCloud(740, 550, 200, 100, "Use the ladders \n to climb up higher")

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_up1, self.spike_up2, self.ladder1, self.ladder_left, self.ladder_right)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.lava_pool, self.platform_left1, self.platform_right1, self.platform_left2, self.platform_right2, self.platform_mid)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.spike_up1, layer = 1)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.lava_pool, layer = 0)
        self.all_sprites.add(self.ladder1, layer = 0)
        self.all_sprites.add(self.platform_left1, layer = 0)
        self.all_sprites.add(self.platform_right1, layer = 0)
        self.all_sprites.add(self.ladder_left, layer = 0)
        self.all_sprites.add(self.platform_left2, layer = 0)
        self.all_sprites.add(self.ladder_right, layer = 0)
        self.all_sprites.add(self.platform_right2, layer = 0)
        self.all_sprites.add(self.platform_mid, layer = 0)

        self.ladders = [self.ladder1, self.ladder_left, self.ladder_right]

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        climb_ladder(self.player, self.ladders)
        jump_from_the_top_of_ladder(self.player, self.ladders)

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


