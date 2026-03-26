# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, Spike, Ice, Ladder, Checkpoint, Lava
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from checkpoint import checkpoint_activation
from maincamera import follow_player

class Level25:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 700, 50, 50)
        self.ice1 = Ice(0, 750, 500, 500)
        self.block1 = Ground(425, 675, 75, 75)
        self.spike_left = Spike(365, 675, 75, 60, 90)
        self.checkpoint1 = Checkpoint(450, 625, 50, 50)
        self.lava_pool = Lava(500, 770, 500, 500)
        self.ladder = Ladder(550, 475, 50, 200)
        self.ice2 = Ice(200, 475, 300, 50)
        self.spike_down = Spike(337.5, 435, 25, 40, 0)
        self.island1 = Ground(50, 500, 150, 50)
        self.wall1 = Ground(0, 0, 50,700)
        self.ladder2 = Ladder(130, 275, 50, 150)
        self.ground = Ground(180, 275, 300, 50)
        self.ceilinng = Ground(200, 100, 250, 85)
        self.spike_up = Spike(215, 180, 35, 50, 180)
        self.spike_up2 = Spike(290, 180, 35, 50, 180)
        self.spike_up3 = Spike(365, 180, 35, 50, 180)
        self.ground2 = Ground(600, 175, 125, 1300)
        self.spike_left2 = Spike(565, 275, 50, 35, 90)
        self.checkpoint2 = Checkpoint(650, 125, 50, 50)
        self.island2 = Ground(900, 700, 100, 60)
        self.spike_down2 = Spike(900, 660, 25, 40, 0)
        self.wall2 = Ground(1000, 0, 100, 1500)

        self.finish_level_trigger = FinishLevelTrigger(950, 600, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.checkpoint1, self.ladder, self.ladder2, self.checkpoint2, self.spike_down, self.spike_down2, self.spike_up, self.spike_up2, self.spike_up3, self.spike_left, self.spike_left2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ice1, self.block1, self.ice2, self.lava_pool, self.island1, self.wall1, self.ground, self.ceilinng, self.ground2, self.island2, self.wall2)
     



        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.ice1, layer = 0)
        self.all_sprites.add(self.block1, layer = 0)
        self.all_sprites.add(self.lava_pool, layer = 1)
        self.all_sprites.add(self.ladder, layer = 0)
        self.all_sprites.add(self.ice2, layer = 0)
        self.all_sprites.add(self.island1, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.ladder2, layer = 0)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ceilinng, layer = 2)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.spike_up3, layer = 1)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.spike_left, layer = 1)
        self.all_sprites.add(self.spike_left2, layer = 1)
        self.all_sprites.add(self.checkpoint1, layer = 1)
        self.all_sprites.add(self.checkpoint2, layer = 1)
        self.all_sprites.add(self.island2, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)



        self.ladders = [self.ladder, self.ladder2]
        self.checkpoints = [self.checkpoint1, self.checkpoint2]
    def update(self, dt):
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        climb_ladder(self.player, self.ladders)
        jump_from_the_top_of_ladder(self.player, self.ladders)
        checkpoint_activation(self.player, self.checkpoints)
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


