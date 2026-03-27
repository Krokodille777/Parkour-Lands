# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, Spike, FinishLevelTrigger, Ladder, Bridge, ElevatorUpDown, Ice
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from elevators import updown_elevator_movement

from maincamera import follow_player

class Level29:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 0, 50, 50)
       
        self.ground = Ground(0, 750, 1000, 500)
        self.block1 = Ground(175, 625, 175, 85)
        self.ladder1 = Ladder(355, 625, 50, 125)
        self.wall1 = Ground(170, 0, 50, 625)
        self.wall2 = Ground(410, 560, 50, 130)
        self.block2 = Ground(360, 455, 100, 105)
        self.block3 = Ground(295, 430, 65, 130)
        self.platform1 = Bridge(220, 600, 25, 25)
        self.platform2 = Bridge (270, 520, 25, 25)
        self.platform3 = Bridge(220, 420, 25, 25)
        self.spike_right = Spike(220, 290, 50, 35, 270) 
        self.ceiling2 = Ground(220, 0, 325 ,290 )
        self.spike_up = Spike(295, 290, 35, 50, 180)
        self.ice = Ice(360, 430, 100, 50)
        self.elevator_up_down = ElevatorUpDown(465, 480, 75, 25, 100)
        self.wall3 = Ground(545, 0, 50, 500)
        self.ceiling = Ground(595, 0, 200, 400)
        self.spike_up2 = Spike(595, 400, 50, 50, 180)
        self.spike_up3 = Spike(645, 400, 50, 50, 180)
        self.spike_up4 = Spike(695, 400, 50, 50, 180)
        self.spike_up5 = Spike(745, 400, 50, 50, 180)
        self.wall4 = Ground(795, 0, 50, 575)
        self.block4 = Ground(760, 575, 100, 50)
        self.ladder2 = Ladder(710, 575, 50, 175)
        self.block5 = Ground(550, 575, 160, 50)

        self.spike_down = Spike(460, 600, 45, 25, 0)
        self.spike_down2 = Spike(510, 600, 45, 25, 0)
        self.floor = Ground(460, 625, 150, 125)
        self.finish_level_trigger = FinishLevelTrigger(900, 650, 50, 100)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.ladder1, self.ladder2, self.spike_right, self.spike_up, self.spike_up2, self.spike_up3, self.spike_up4, self.spike_up5, self.spike_down, self.spike_down2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.block1, self.wall1, self.wall2, self.block2, self.block3, self.platform1, self.platform2, self.platform3, self.ice, self.elevator_up_down, self.wall3, self.ceiling, self.ceiling2, self.wall4, self.block4, self.block5, self.floor)
     

        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.block1, layer = 0)
        self.all_sprites.add(self.ladder1, layer = 0)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.block2, layer = 0)
        self.all_sprites.add(self.block3, layer = 0)
        self.all_sprites.add(self.platform1, layer = 0)
        self.all_sprites.add(self.platform2, layer = 0)
        self.all_sprites.add(self.platform3, layer = 0)
        self.all_sprites.add(self.spike_right, layer = 1)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.ice, layer = 0)
        self.all_sprites.add(self.elevator_up_down, layer = 3)
        self.all_sprites.add(self.wall3, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.ceiling2, layer = 0)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.spike_up3, layer = 1)
        self.all_sprites.add(self.spike_up4, layer = 1)
        self.all_sprites.add(self.spike_up5, layer = 1)
        self.all_sprites.add(self.wall4, layer = 0)
        self.all_sprites.add(self.block4, layer = 0)
        self.all_sprites.add(self.ladder2, layer = 0)
        self.all_sprites.add(self.block5, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.block5, layer = 0)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)




    def update(self, dt):
        updown_elevator_movement(self.elevator_up_down, 100, dt)
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
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


