import pygame

from pygame.locals import *

#Class for ground and platforms

class Ground (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "ground"

#Class for player

class Player (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel_y = 0
        self.on_ground = False
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "player"