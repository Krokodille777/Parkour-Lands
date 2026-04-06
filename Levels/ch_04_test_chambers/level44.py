
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, Button, Door, TrapDoor, JumpPad, Lava, ElevatorLeftRight
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from pushableBlock import push_the_block, block_collisions
from maincamera import follow_player

class Level41:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 550, 500)

        self.box = PushableBlock(300, 665, 85, 85)

        self.ground2 = Ground(550, 600, 550, 500)
        self.tip_cloud = TipCloud(65, 0, 175, 120, "Welcome to the test chambers! \n Each of them equipped with \n a puzzle that you need to solve to \n get to the next one. \n Good luck!")
        self.finish_level_trigger = FinishLevelTrigger(900, 500, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        
        

    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        push_the_block(self.player, self.box,  dt)
        block_collisions(self.box, self.colliders, dt, self.triggers)
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



    