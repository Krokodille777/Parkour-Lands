# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, Bridge, Ice, FinishLevelTrigger, JumpPad, Lava, Ladder, Spike, ElevatorLeftRight, FragileGround, DynamicSpikePlatform, DynamicSpike
from physics import apply_gravity, move_and_collide, climb_ladder, jump_from_the_top_of_ladder, crouching_adjustment, squash_adjustment
from fragile_ground import respawn_fragile_ground, trigger_fragile_ground, fragile_ground_check
from dynamic_spike import dynamic_spike_movement_based_on_timer
from elevators import leftright_elevator_movement
from maincamera import follow_player

class Level36:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 700, 50, 50)
        self.ground = Ground(0, 750, 150, 500)
        self.jump_pad = JumpPad(100, 725, 50, 25, -900)
        self.lava = Lava(150, 775, 200, 500)

        self.fg1 = FragileGround(175, 600, 45, 45)
        self.fg2 = FragileGround(275, 625, 45, 45)

        self.ground2 = Ground(350, 800, 650, 500)
        self.ceiling = Ground(465, 570, 185, 35)
        self.ice = Ice(350, 750, 650, 50)
        self.spike_down = Spike(450, 725, 25, 25, 0)
        self.spike_up = Spike(560, 605, 25, 25, 180)

        self.wall1 = Ground(750, 0, 100, 750)
        self.ladder1 = Ladder(675, 520, 50, 200)

        self.block1 = Ground(600, 520, 50, 50)
        self.lava2 = Lava(515, 530, 85, 40)
        self.block2 = Ground(465, 495, 50, 75)
        self.fg3 = FragileGround(520, 475, 45, 45)
        self.block3 = Ground(425, 475, 90, 50)
        self.ground3 = Ground(0, 500, 425, 25 )
        self.elevator = ElevatorLeftRight(180, 460, 65, 25, 150)

        self.ceiling2 = Ground(100, 225, 275, 175)
        self.dsp1 = DynamicSpikePlatform(150, 350, 75, 50)
        self.dsp2 = DynamicSpikePlatform(250, 350, 75, 50)
        self.dsu1 = DynamicSpike(150, 385, 25, 25, 180)
        self.dsu2 = DynamicSpike(175, 385, 25, 25, 180)
        self.dsu3 = DynamicSpike(200, 385, 25, 25, 180)

        self.dsu4 = DynamicSpike(250, 385, 25, 25, 180)
        self.dsu5 = DynamicSpike(275, 385, 25, 25, 180)
        self.dsu6 = DynamicSpike(300, 385, 25, 25, 180)

        self.wall2 = Ground(0, 0, 25, 525)
        self.ladder2 = Ladder(35, 225, 50, 200,)

        self.dsp3 = DynamicSpikePlatform(200, 225, 75, 50)
        self.dsd1 = DynamicSpike(200, 215, 25, 25, 0)
        self.dsd2 = DynamicSpike(225, 215, 25, 25, 0)
        self.dsd3 = DynamicSpike(250, 215, 25, 25, 0)
        self.bridge = Bridge(375, 225, 85, 25)
        self.platform = Ground(460, 225, 125, 50)


        self.box = Ground(1000, 1000, 50, 50)

        self.tip_cloud = TipCloud(600, 800, 200, 100,"Don't hesitate, when stepped \n on the fragile ground \n" 
                                  "Once you step on it, you have a \n second to get off before it breaks!")
        
        self.tip_cloud2 = TipCloud(600, 300, 200, 100,"The dynamic spikes will \n move up and down based \non a timer, so time your \n movements carefully!")
        self.finish_level_trigger = FinishLevelTrigger(535, 125, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_down, self.spike_up, self.ladder1, self.ladder2, self.dsu1, self.dsu2, self.dsu3, self.dsu4, self.dsu5, self.dsu6, self.dsd1, self.dsd2, self.dsd3)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.lava, self.ground2, self.ceiling, self.ice, self.fg1, self.fg2, self.wall1, self.jump_pad, self.block1, self.lava2, self.block2, self.fg3, self.block3, self.ground3, self.elevator, self.ceiling2, self.dsp1, self.dsp2, self.wall2, self.dsp3, self.bridge, self.platform)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.jump_pad, layer = 0)
        self.all_sprites.add(self.lava, layer = 0)
        self.all_sprites.add(self.fg1, layer = 0)
        self.all_sprites.add(self.fg2, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.ice, layer = 2)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.ladder1, layer = 0)
        self.all_sprites.add(self.block1, layer = 0)
        self.all_sprites.add(self.lava2, layer = 0)
        self.all_sprites.add(self.block2, layer = 0)
        self.all_sprites.add(self.fg3, layer = 0)
        self.all_sprites.add(self.block3, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.elevator, layer = 0)
        self.all_sprites.add(self.ceiling2, layer = 1)
        self.all_sprites.add(self.dsp1, layer = 2)
        self.all_sprites.add(self.dsp2, layer = 2)
        self.all_sprites.add(self.dsu1, layer = 1)
        self.all_sprites.add(self.dsu2, layer = 1)
        self.all_sprites.add(self.dsu3, layer = 1)
        self.all_sprites.add(self.dsu4, layer = 1)
        self.all_sprites.add(self.dsu5, layer = 1)
        self.all_sprites.add(self.dsu6, layer = 1)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.ladder2, layer = 0)
        self.all_sprites.add(self.dsp3, layer = 2)
        self.all_sprites.add(self.dsd1, layer = 1)
        self.all_sprites.add(self.dsd2, layer = 1)
        self.all_sprites.add(self.dsd3, layer = 1)
        self.all_sprites.add(self.bridge, layer = 0)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.box, layer = 0)
        self.all_sprites.add(self.tip_cloud2, layer = 2)
 
        

    def update(self, dt):    
        
        
        trigger_fragile_ground(self.player, self.box, [self.fg1, self.fg2, self.fg3])
        fragile_ground_check(self.player, self.box, [self.fg1, self.fg2, self.fg3], self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites,[self.fg1, self.fg2, self.fg3], dt)    
        
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
       
        leftright_elevator_movement(self.elevator, 150, dt)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        climb_ladder(self.player, [self.ladder1, self.ladder2])
        jump_from_the_top_of_ladder(self.player, [self.ladder1, self.ladder2])


        for ds in [self.dsu1, self.dsu2, self.dsu3, self.dsu4, self.dsu5, self.dsu6, self.dsd1, self.dsd2, self.dsd3]:
            dynamic_spike_movement_based_on_timer(ds, dt)
        self.player.handle_input()
        

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



    