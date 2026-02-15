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
        self.crouching = False
        self.full_width = width
        self.full_height = height
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

        # Crouching
        bottom = self.rect.bottom
        if keys[K_c]:
                self.crouching = True
                self.image = pygame.Surface((self.full_width, self.full_height // 2))
                self.image.fill((0, 0, 255))
        elif not self.crouching:
                self.image = pygame.Surface((self.full_width, self.full_height))
                self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(bottomleft = (round(self.pos.x), bottom))
        self.pos.y = float(self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)



class JumpPad (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, launch_vel):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.type = 'jumppad' # Type identifier for jump pad objects
        self.launch_vel = launch_vel

    


class Lava (pygame.sprite.Sprite):
     def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 165, 0))  # Orange color for lava
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'lava' # Type identifier for lava object


class Water (pygame.sprite.Sprite):
     def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'water' # Type identifier for water object
     

class Spike(pygame.sprite.Sprite):
     def __init__(self, x, y, width, height, angle): #angle parameter will make spikes' class universal, as they will have similar physics, no matter the direction they point
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 0, 0), [(0, height), (width // 2, 0), (width, height)])  # Draw a triangle for the spike
        self.image = pygame.transform.rotate(self.image, angle)  # Rotate the spike to the specified angle
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'spike' # Type identifier for spike object