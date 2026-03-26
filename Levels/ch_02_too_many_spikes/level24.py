# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Spike, JumpPad, Ice, Ladder, Checkpoint, Lava
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from checkpoint import checkpoint_activation
from maincamera import follow_player

class Level24:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 80, 50, 50)
        self.ground = Ground(0, 750, 300, 500)
        self.lava_pool = Lava(300, 950, 500, 300)
        self.ladder = Ladder(370, 550, 50, 200)
        self.island1 = Ground (250, 550, 100, 50)
        self.wall1 = Ground(250, 450, 40, 100)
        self.checkpoint1 = Checkpoint(300, 500, 50, 50)
        self.tip_cloud = TipCloud(500, 150, 200, 100, "If you are unsure how to \n complete the following parts. \n Try to use Checkpoints to your advantage!")
        self.island2 = Ground(430, 550, 100, 50)
        self.jumpPad = JumpPad(480, 525, 50, 25, -1300)
        self.platform1 = Ground(650, 250, 50, 50)
        self.spike_up = Spike(657, 300, 35, 50, 180)
        self.platform2 = Ground(750, 325, 50, 50)
        self.spike_up2 = Spike(757, 375, 35, 50, 180)
        self.ground2 = Ground(800, 600, 125, 700)
        self.checkpoint2 = Checkpoint(800, 550, 50, 50)
        self.spike_down = Spike(890, 560, 25, 40, 0)
        self.ground3 = Ground(915, 700, 125, 700)
        self.ice = Ice(915, 600, 125, 100 )
        self.ground4 = Ground(1040, 800, 135, 700)
        self.spike_down2 = Spike(1040, 750, 45, 50, 0)
        self.spike_down3 = Spike(1085, 750, 45, 50, 0)
        self.spike_down4 = Spike(1130, 750, 45, 50, 0)
        self.platform3 = Ground(1130, 550, 100, 50)
        self.wall2 = Ground(1175, 600, 50, 200)    
        self.finish_level_trigger = FinishLevelTrigger(1200, 450, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.checkpoint1, self.ladder, self.checkpoint2, self.spike_down, self.spike_down2, self.spike_down3, self.spike_down4, self.spike_up, self.spike_up2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.lava_pool, self.island1, self.wall1, self.island2, self.platform1, self.platform2, self.ground2, self.ground3, self.ice, self.ground4, self.platform3, self.wall2, self.jumpPad)
     

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 3)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.lava_pool, layer = 0)
        self.all_sprites.add(self.ladder, layer = 0)
        self.all_sprites.add(self.island1, layer = 0)
        self.all_sprites.add(self.checkpoint1, layer = 1)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.island2, layer = 0)
        self.all_sprites.add(self.jumpPad, layer = 0)
        self.all_sprites.add(self.platform1, layer = 0)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.platform2, layer = 0)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.checkpoint2, layer = 1)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.ice, layer = 0)
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.platform3, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.spike_down3, layer = 1)
        self.all_sprites.add(self.spike_down4, layer = 1)


        self.ladders = [self.ladder]
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


