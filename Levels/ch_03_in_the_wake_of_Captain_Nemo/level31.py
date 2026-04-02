# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Water, Ladder
from physics import apply_gravity, move_and_collide, climb_ladder, jump_from_the_top_of_ladder, crouching_adjustment, squash_adjustment, buoyant_force

from maincamera import follow_player

class Level31:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 150, 500)
        self.ladder1 = Ladder(150, 750, 50, 300)
        self.water_pool = Water(150, 800, 700, 500)
        self.ladder2 = Ladder(800, 750, 50, 300)
        self.ground2 = Ground(850, 750, 150, 500)
        self.tip_cloud = TipCloud(300, 450, 200, 200, "The whole chapter is about water. \n Water, unlike lava, allows you to cross it \n without taking damage. \n However, while in water your movement is much more sluggish and you will be affected by buoyancy. \n Good luck!")
        self.finish_level_trigger = FinishLevelTrigger(900, 650, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.water_pool, self.ladder1, self.ladder2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.ladder1, layer = 2)
        self.all_sprites.add(self.ladder2, layer = 2)
        

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water_pool])
        climb_ladder(self.player, [self.ladder1, self.ladder2])
        jump_from_the_top_of_ladder(self.player, [self.ladder1, self.ladder2])
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



    