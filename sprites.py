import pygame

from pygame.locals import *

#Class for ground and platforms

class Ground (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((56, 156, 79))  # Black color for ground
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'ground' # Type identifier for ground objects

#Class for player

class Player (pygame.sprite.Sprite):
    SPEED = 400
    JUMP_VEL = -700

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "player"

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        self.vel.x = 0
        if keys[K_LEFT] or keys[K_a]:
            self.vel.x = -self.SPEED
        if keys[K_RIGHT] or keys[K_d]:
            self.vel.x = self.SPEED

        # Jumping
        if (keys[K_SPACE] or keys[K_UP] or keys[K_w]) and self.on_ground:
            self.vel.y = self.JUMP_VEL
            self.on_ground = False