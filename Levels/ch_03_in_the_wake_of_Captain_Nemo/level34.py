# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground,  FinishLevelTrigger, Water, Ladder, TipCloud, Spike, ElevatorUpDown, Fan
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force, climb_ladder, jump_from_the_top_of_ladder
from fans import apply_fan_effect, apply_fan_effect_in_water, apply_fan_effect_left_right
from elevators import updown_elevator_movement
from maincamera import follow_player

class Level34:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(10, 800, 50, 50)
        self.ground = Ground(0, 850, 50, 50)
        self.floor = Ground (0, 850, 200, 150)
        self.ground2 = Ground (0, 750, 50, 50)
        self.water_pool = Water(0, 500, 200, 500)
        self.fan_down = Fan(115, 825, 85, 25, (0, -1))
        self.wall = Ground(200, 200, 50, 750)

        self.platform1 = Ground(125, 200, 100, 50)
        self.ladder = Ladder(100, 200, 25, 100)

        self.elevator = ElevatorUpDown(325, 300, 75,50, 100)
        self.wall2 = Ground(650, 0, 75, 700)
        self.ground3 = Ground(425, 500, 225, 25)
        self.fan_left = Fan(625, 415, 25, 85, (1, 0))

        self.ground4 = Ground(250, 650, 400, 50)
        self.spike_down = Spike(250, 595, 35, 65, 0)
        self.block1 = Ground(425, 600, 50, 50)
        self.spike_up = Spike(535, 525, 35, 60, 180)
        

        self.finish_level_trigger = FinishLevelTrigger(600, 550, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_down, self.spike_up, self.water_pool, self.ladder)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.floor, self.wall, self.fan_down, self.fan_left, self.platform1, self.elevator, self.wall2, self.ground3, self.ground4, self.block1)

        self.all_sprites.add(self.ground, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.floor, layer = 2)
        self.all_sprites.add(self.ground2, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.fan_down, layer = 1)
        self.all_sprites.add(self.wall, layer = 2)
        self.all_sprites.add(self.platform1, layer = 2)
        self.all_sprites.add(self.ladder, layer = 2)

        self.all_sprites.add(self.elevator, layer = 2)
        self.all_sprites.add(self.wall2, layer = 2)
        self.all_sprites.add(self.ground3, layer = 2)
        self.all_sprites.add(self.fan_left, layer = 1)
        self.all_sprites.add(self.ground4, layer = 2)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.block1, layer = 2)
        self.all_sprites.add(self.spike_up, layer = 1)

        

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        apply_fan_effect(self.player, self.fan_down, dt)
        apply_fan_effect_left_right(self.player, self.fan_left, dt)
        apply_fan_effect_in_water(self.player, self.fan_down, dt)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water_pool])
        updown_elevator_movement(self.elevator, 100 ,dt)
        climb_ladder(self.player, [self.ladder])
        jump_from_the_top_of_ladder(self.player, [self.ladder])
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



    