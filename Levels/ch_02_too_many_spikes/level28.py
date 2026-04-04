# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, ElevatorUpDown, Lava, FinishLevelTrigger
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from elevators import updown_elevator_movement
from maincamera import follow_player

class Level28:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 150, 500)

        self.lava_pool = Lava(150, 1050, 775, 500)

        self.elevator_left = ElevatorUpDown(175, 800, 100, 25, 175)
        self.elevator_mid = ElevatorUpDown(425, 800, 100, 25, 120)
        self.elevator_right = ElevatorUpDown(675, 800, 100, 25, 200)

        self.ground2 = Ground(925, 750, 100, 500)
        
        
        self.finish_level_trigger = FinishLevelTrigger(950, 650, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.lava_pool,  self. ground2, self.elevator_left, self.elevator_mid, self.elevator_right)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.lava_pool, layer = 0)
        self.all_sprites.add(self.elevator_left, layer = 1)
        self.all_sprites.add(self.elevator_mid, layer = 1)
        self.all_sprites.add(self.elevator_right, layer = 1)
        self.all_sprites.add(self.ground2, layer = 0)

    def update(self, dt):
        updown_elevator_movement(self.elevator_left, 175, dt)
        updown_elevator_movement(self.elevator_mid, 120, dt)
        updown_elevator_movement(self.elevator_right, 200, dt)
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


