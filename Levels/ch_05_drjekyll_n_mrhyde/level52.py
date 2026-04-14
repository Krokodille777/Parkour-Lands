
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, AlterStand, AlterPlayer
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, frozen_adjustment, switch_to_alter_player, switch_to_normal_player
from pushableBlock import push_the_block, block_collisions
from maincamera import follow_player, follow_alter_player

class Level52:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 700, 50, 50)
        self.ground = Ground(0, 750, 1000, 500)




        self.alter_stand = AlterStand(375, 250, 125, 25)
        self.hyde = AlterPlayer(400, 200, 50, 50)
        self.wall = Ground(500, 0, 50, 300)
        self.platform2 = Ground(375, 275, 125, 25)

        self.box2 = PushableBlock(515, 665, 85, 85)
        self.ground2 = Ground(600, 550, 215, 350)

       
        self.finish_level_trigger = FinishLevelTrigger(745, 450, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.alter_stand, self.player, self.hyde,  self.platform2,  self.box2, self.wall)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.alter_stand, layer = 1)
        self.all_sprites.add(self.hyde, layer = 2)
        self.all_sprites.add(self.platform2, layer = 1)

        self.all_sprites.add(self.box2, layer = 1)
        self.all_sprites.add(self.wall, layer = 1)



    def _active_player(self):
        return self.hyde if not self.hyde.frozen else self.player

    def _handle_switch_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_1]:
            switch_to_normal_player(self.player, self.hyde)
        elif keys[K_2]:
            switch_to_alter_player(self.player, self.hyde)

    def update(self, dt):
        self._handle_switch_input()
        
        active_player = self._active_player()

        active_player.handle_input(dt)
        self.box2.handle_input(dt)
        frozen_adjustment(self.player, self.colliders)
        frozen_adjustment(self.hyde, self.colliders)

        apply_gravity(active_player, dt)
        move_and_collide(active_player, self.colliders, dt, self.triggers)
        crouching_adjustment(active_player, self.colliders)
        squash_adjustment(active_player, self.colliders)


        push_the_block(active_player, self.box2, dt)
        block_collisions(self.box2, self.colliders, dt, self.triggers)

    def draw(self, screen):
        active_player = self._active_player()
        if active_player is self.hyde:
            offset_x, offset_y = follow_alter_player(
            self.hyde,
            screen.get_width(),
            self.WORLD_WIDTH,
            screen.get_height(),
            self.WORLD_HEIGHT,
        )
        else:
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
        return self._active_player().rect.colliderect(self.finish_level_trigger.rect)



    
