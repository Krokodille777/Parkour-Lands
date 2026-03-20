# Level 6 of Chapter 1 - Plains : Crouching
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from maincamera import follow_player

class Level6:

    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground1 = Ground(0, 750, 1000, 500)
        self.island1 = Ground(150, 100, 700, 615)
        self.tip_cloud1 = TipCloud(450, 500, 300, 150, "Press C to crouch! \n To return to normal size, press C again!. \n While in tight place, you can't \n jump or turn back to normal size!")

        self.finish_level_trigger = FinishLevelTrigger(950, 650, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground1, self.island1)

        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.ground1, layer = 0)
        self.all_sprites.add(self.island1, layer = 0)
        self.all_sprites.add(self.tip_cloud1, layer = 1)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)

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