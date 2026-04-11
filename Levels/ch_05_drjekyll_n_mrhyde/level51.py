
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Door, Button, TrapDoor, AlterStand, AlterPlayer
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, frozen_adjustment, switch_to_alter_player, switch_to_normal_player
from button_door_trap import press_button, link_button_to_door, open_door_trapdoor
from maincamera import follow_player, follow_alter_player

class Level51:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 600, 50, 50)
        self.ground = Ground(0, 650, 1000, 500)
        self.alter_stand = AlterStand(30, 275, 65, 25)
        self.hyde = AlterPlayer(60, 250, 50, 50)
        self.ground2 = Ground(0, 300, 1000, 200)

        self.block = Ground(1500, 500, 50, 50)
        self.button = Button(900, 275, 75, 35)
        self.door = Door(900, 500, 50, 150)
        self.door.linked_button = self.button
        self.tip_cloud = TipCloud(300, 300, 175, 120, "Press 1 for Jekyll \n Press 2 for Hyde")
        self.finish_level_trigger = FinishLevelTrigger(950, 550, 50, 100)

        self.trap_door = TrapDoor(500, 1750, 50, 25)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.button, self.trap_door)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.door, self.trap_door, self.alter_stand, self.player, self.hyde)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.button, layer = 1)
        self.all_sprites.add(self.door, layer = 2)
        self.all_sprites.add(self.alter_stand, layer = 1)
        self.all_sprites.add(self.hyde, layer = 2)
        self.all_sprites.add(self.trap_door, layer = 1) 

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

        frozen_adjustment(self.player, self.colliders)
        frozen_adjustment(self.hyde, self.colliders)

        apply_gravity(active_player, dt)
        move_and_collide(active_player, self.colliders, dt, self.triggers)
        crouching_adjustment(active_player, self.colliders)
        squash_adjustment(active_player, self.colliders)

        press_button([self.player, self.hyde], [], [self.button])
        link_button_to_door([self.button], [self.door])
        open_door_trapdoor([self.door], [self.trap_door])

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



    
