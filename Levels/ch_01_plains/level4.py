# Level 4 of Chapter 1 - Plains : Jump Pads
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Lava, Bridge, JumpPad
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from maincamera import follow_player

class Level4:

    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground1 = Ground(0, 750, 300, 500)
        self.lava_pool1 = Lava(300, 850, 150, 500)
        self.island1 = Ground(450, 750, 100, 500)
        self.tip_cloud1 = TipCloud(450, 600, 200, 100, "Use Jump Pads to \n jump higher!")
        self.bridge = Bridge(550, 750, 100, 20)
        self.island2 = Ground(650, 750, 100, 500)

        self.ground2 = Ground(750, 775, 200, 500)

        self.jump_pad = JumpPad(850, 755, 50, 20, -1600)
        self.wall1 = Ground(900, -300, 20, 1200)

        self.platform1 = Ground(650, 300, 100, 50)
        self.platform2 = Ground(450, 300, 100, 50)
        self.platform3 = Ground(250, 300, 100, 50)
        self.finish_level_trigger = FinishLevelTrigger(275, 200, 50, 100)



        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground1, self.lava_pool1, self.island1, self.bridge, self.island2, self.ground2, self.wall1, self.platform1, self.platform2, self.platform3, self.jump_pad)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ground1)
        self.all_sprites.add(self.lava_pool1)
        self.all_sprites.add(self.island1)
        self.all_sprites.add(self.tip_cloud1)
        self.all_sprites.add(self.bridge)
        self.all_sprites.add(self.island2)
        self.all_sprites.add(self.ground2)
        self.all_sprites.add(self.finish_level_trigger)
        self.all_sprites.add(self.wall1)
        self.all_sprites.add(self.platform1)
        self.all_sprites.add(self.platform2)
        self.all_sprites.add(self.platform3)
        self.all_sprites.add(self.jump_pad)

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