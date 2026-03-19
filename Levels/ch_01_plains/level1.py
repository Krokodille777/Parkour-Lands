import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger
from physics import apply_gravity, move_and_collide

from maincamera import follow_player

class Level1:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 2000, 500)
        self.tip_cloud = TipCloud(300, 600, 200, 100, "Welcome to Parkour Lands! \n A/D or arrows to move")
        self.finish_level_trigger = FinishLevelTrigger(1800, 650, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        
        

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
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



    