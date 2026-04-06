
import pygame
from pygame.locals import *
from sprites import Player, Ground, Bridge, TipCloud, FinishLevelTrigger, Checkpoint, PressTrap
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from checkpoint import checkpoint_activation
from press_trap import update_press_trap, apply_press_trap_effect
from maincamera import follow_player

class Level39:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(30, 60, 50, 50)
        self.ground = Ground(0, 150, 100, 125)
        self.ceiling = Ground(100, 0, 750, 25)
        self.wall = Ground(800, 25, 50, 600)
        self.floor = Ground(0, 435, 850, 500)
        self.platform = Ground (100, 160, 550, 140)
        self.bridge = Bridge(765, 160, 35, 25)
        self.bridge2 = Bridge(650, 260, 35, 25)
        self.bridge3 = Bridge(750, 360, 50, 25)
        self.checkpoint = Checkpoint(750, 310, 50, 50)
        self.finish_level_trigger = FinishLevelTrigger(30, 335, 50, 100)

        #6 press traps
        self.press_trap1 = PressTrap(175, 25, 85, 35, 180)
        self.press_trap2 = PressTrap(335, 25, 85, 35, 180)
        self.press_trap3 = PressTrap(495, 25, 85, 35, 180)
        self.press_trap4 = PressTrap(490, 300, 85, 35, 180)
        self.press_trap5 = PressTrap(330, 300, 85, 35, 180)
        self.press_trap6 = PressTrap(170, 300, 85, 35, 180)

        self.tip_cloud1 = TipCloud(600, 100, 225, 50, "Like dynamic spikes, press traps \n their movement is based on a timer. \n Ypu'd better not mess with them!")

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.checkpoint, self.press_trap1, self.press_trap2, self.press_trap3, self.press_trap4, self.press_trap5, self.press_trap6)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ceiling, self.wall, self.floor, self.platform, self.bridge, self.bridge2, self.bridge3)

        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.bridge, layer = 1)
        self.all_sprites.add(self.bridge2, layer = 1)
        self.all_sprites.add(self.bridge3, layer = 1)
        self.all_sprites.add(self.checkpoint, layer = 1)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.press_trap1, layer = 1)
        self.all_sprites.add(self.press_trap2, layer = 1)
        self.all_sprites.add(self.press_trap3, layer = 1)
        self.all_sprites.add(self.press_trap4, layer = 1)
        self.all_sprites.add(self.press_trap5, layer = 1)
        self.all_sprites.add(self.press_trap6, layer = 1)
        self.all_sprites.add(self.tip_cloud1, layer = 2)
    def update(self, dt):
        checkpoint_activation(self.player, [self.checkpoint])
        update_press_trap(self.press_trap1, dt)
        update_press_trap(self.press_trap2, dt)
        update_press_trap(self.press_trap3, dt)
        update_press_trap(self.press_trap4, dt)
        update_press_trap(self.press_trap5, dt)
        update_press_trap(self.press_trap6, dt)
    
        for trap in [self.press_trap1, self.press_trap2, self.press_trap3, self.press_trap4, self.press_trap5, self.press_trap6]:
            apply_press_trap_effect(self.player, trap, dt)
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



    