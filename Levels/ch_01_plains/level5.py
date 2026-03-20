# Level 5 of Chapter 1 - Plains : Ice and Squash
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Lava, Bridge, JumpPad, Ice
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from maincamera import follow_player


class Level5:

    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.all_sprites = pygame.sprite.LayeredUpdates()
        
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 125, 500)
        self.ice = Ice(125, 750, 250, 500)
        self.island = Ground(375, 750, 175, 500)
        self.jump_pad = JumpPad(462.5, 725, 50, 25, -1800)
        self.lava_pool = Lava(550, 800, 2000, 500)

        self. platform1 = Ground(380, 450, 75, 75)
        self.bridge1 = Bridge(280, 450, 100, 25)
        self.ice2 = Ice(180, 450, 100, 75)
        self.wall1 = Ground(130, 0, 50, 500)

        self.platform2 = Ground(500, 450, 75, 75)
        self.platform3 = Ground(650, 425, 75, 75)
        self.platform4 = Ground(800, 400, 125, 75)

        self.tip_cloud = TipCloud(250, 300, 225, 50, "Press V to squash yourself \n and fit through narrow spaces. \n And then press V again to \n return to normal size!")

        self.finish_flag = FinishLevelTrigger(862.5, 300, 50, 100)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_flag)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ice, self.island, self.jump_pad, self.lava_pool, self.platform1, self.platform2, self.bridge1, self.ice2, self.wall1, self.platform3, self.platform4)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ice, layer = 0)
        self.all_sprites.add(self.island, layer = 0)
        self.all_sprites.add(self.jump_pad, layer = 0)
        self.all_sprites.add(self.lava_pool, layer = 0)
        self.all_sprites.add(self.platform1, layer = 0)
        self.all_sprites.add(self.platform2, layer = 0)
        self.all_sprites.add(self.bridge1, layer = 0)
        self.all_sprites.add(self.ice2, layer = 0)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.platform3, layer = 0)
        self.all_sprites.add(self.platform4, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.finish_flag, layer = 1)
        self.all_sprites.add(self.player, layer = 2)

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
        return self.player.rect.colliderect(self.finish_flag.rect)