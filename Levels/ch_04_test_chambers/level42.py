
import pygame
from pygame.locals import *
from sprites import Player, Ground,FinishLevelTrigger, PushableBlock, JumpPad, Bridge
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from pushableBlock import push_the_block, block_collisions
from maincamera import follow_player

class Level42:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 650, 50, 50)
        self.ground = Ground(0, 750, 850, 500)

        

        self.ground2 = Ground(850, 600, 550, 500)

        self.ground3 = Ground(0, 300, 125, 375)
        self.platform = Bridge(125, 650, 85, 25)
        self.jump_pad = JumpPad(130, 625, 65, 25, -1500)
        self.box = PushableBlock(60, 215, 85, 85)
        self.finish_level_trigger = FinishLevelTrigger(900, 500, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box, self.jump_pad, self.platform, self.ground3)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.jump_pad, layer = 0)
        self.all_sprites.add(self.player, layer = 3)
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



    