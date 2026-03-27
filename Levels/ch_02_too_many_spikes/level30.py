# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, Spike, FinishLevelTrigger, Ladder, Bridge, ElevatorLeftRight, Checkpoint, Lava,  ElevatorUpDown, Ice, JumpPad
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from elevators import updown_elevator_movement, leftright_elevator_movement
from checkpoint import checkpoint_activation
from maincamera import follow_player

class Level30:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(30, 725, 50, 50)
       
        self.ground = Ground(0, 800, 500, 500)
        self.spike_down = Spike(125,  750, 35, 50, 0)

        self.spike_down2 = Spike(350, 750, 35, 50, 0)
        self.spike_down3 = Spike(375, 750, 35, 50, 0)

        self.lava1 = Lava(500, 900, 500, 130)

        self.block1 = Ground(550, 725, 85, 60)
        self.spike_up = Spike(575, 785, 35, 35, 180)
        self.ladder = Ladder(640, 725, 50, 125)
        self.block2 = Ground(695, 675, 50, 125)
        self.spike_right = Spike(745, 675, 40, 40, 270)
        self.island1 = Ground(622, 850, 150, 25)

        self.platform1 = Ground(782, 800, 55, 35)
        self.platform2 = Ground(857, 750, 93, 35)
        self.jumpPad = JumpPad(902, 725, 50, 25, -1700)
        self.wall1 = Ground(950, 0, 100, 1500)


        self.ground2 = Ground(470, 610, 75, 65)
        self.floor = Ground(545, 642, 150, 33)
        self.ice = Ice(545, 610, 150, 32)
        self.ground3 = Ground(690, 610, 145, 65)
        self.wall2 = Ground(800, 500, 35, 160)
        self.bridge = Bridge(835 ,500 ,65, 25)
        self.checkpoint = Checkpoint(813, 450, 50, 50)

        self.block3 = Ground(525, 325, 225, 250)
        self.spike_left = Spike(480, 350, 35, 50, 90)
        self.spike_left2 = Spike(480, 385, 35, 50, 90)
        
        self.spike_down5 = Spike(675, 275, 35, 50, 0)
        self.spike_down6 = Spike(640, 275, 35, 50, 0)
        self.spike_down7 = Spike(605, 275, 35, 50, 0)
        self.spike_down8 = Spike(570, 275, 35, 50, 0)

        self.platform3 = Ground(405, 545, 65, 65)
        self.ground4 = Ground(340, 480, 65, 65)
        self.bridge2 = Bridge(275, 480, 70, 25)
        self.wall3 = Ground(225, 480, 50, 80)
        self.ice2 = Ice(50, 505, 175, 60)
        self.wall4 = Ground(0, 0, 50, 565)

        self.elevator_up_down = ElevatorUpDown(50, 285, 75, 45, 170)

        self.floor2 = Ground(225, 265, 325, 35)
        self.ceiling = Ground(50, 0, 500, 25)
        self.spike_up2 = Spike(165, 25, 35, 55, 180)
        self.spike_up3 = Spike(205, 25, 35, 55, 180)
        self.small_wall = Bridge(225, 230, 25, 35)
        self.lava2 = Lava(250, 235, 300, 30)
        self.small_wall2 = Bridge(525, 230, 25, 35)
        self.platform_top = Ground(320, 100, 65, 25)
        self.elevator_left_right = ElevatorLeftRight(320, 125, 80, 25, 250)
        self.platform_bottom = Ground(320, 150, 65, 25)
        self.spike_up4 = Spike(470, 25, 35, 55, 180)


        self.block4 = Ground(735, 230, 80, 50)
        self.bridge3 = Bridge(815, 230, 135, 25)

        self.finish_level_trigger = FinishLevelTrigger(900, 130, 50, 100)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_down, self.spike_down2,  self.spike_down3, self.spike_up, self.spike_right,self.ladder, self.checkpoint, self.spike_left, self.spike_left2, self.spike_down5, self.spike_down6, self.spike_down7, self.spike_down8, self.spike_up2, self.spike_up3, self.spike_up4)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.block1, self.block2, self.island1, self.platform1, self.platform2, self.jumpPad, self.wall1, self.lava1, self.ground2, self.floor, self.ice, self.ground3,  self.wall2, self.bridge, self.block3, self.platform3, self.ground4, self.bridge2, self.wall3, self.ice2, self.wall4, self.elevator_up_down, self.floor2, self.ceiling, self.small_wall, self.lava2, self.small_wall2, self.platform_top, self.elevator_left_right, self.platform_bottom, self.block4, self.bridge3)
     

        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.spike_down3, layer = 1)
        self.all_sprites.add(self.lava1, layer = 0)
        self.all_sprites.add(self.block1, layer = 0)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.ladder, layer = 0)
        self.all_sprites.add(self.block2, layer = 0)
        self.all_sprites.add(self.spike_right, layer = 1)
        self.all_sprites.add(self.island1, layer = 0)
        self.all_sprites.add(self.platform1, layer = 0)
        self.all_sprites.add(self.platform2, layer = 0)
        self.all_sprites.add(self.jumpPad, layer = 0)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.ice, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.bridge, layer = 0)
        self.all_sprites.add(self.checkpoint, layer = 1)
        self.all_sprites.add(self.block3, layer = 0)
        self.all_sprites.add(self.spike_left, layer = 1)
        self.all_sprites.add(self.spike_left2, layer = 1)
        self.all_sprites.add(self.spike_down5, layer = 1)
        self.all_sprites.add(self.spike_down6, layer = 1)
        self.all_sprites.add(self.spike_down7, layer = 1)
        self.all_sprites.add(self.platform3, layer = 0)
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.bridge2, layer = 0)
        self.all_sprites.add(self.wall3, layer = 0)
        self.all_sprites.add(self.ice2, layer = 0)
        self.all_sprites.add(self.wall4, layer = 0)
        self.all_sprites.add(self.elevator_up_down, layer = 3)
        self.all_sprites.add(self.floor2, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.spike_up3, layer = 1)
        self.all_sprites.add(self.spike_up4, layer = 1)
        self.all_sprites.add(self.small_wall, layer = 0)
        self.all_sprites.add(self.lava2, layer = 0)
        self.all_sprites.add(self.small_wall2, layer = 0)
        self.all_sprites.add(self.platform_top, layer = 0)
        self.all_sprites.add(self.elevator_left_right, layer = 3)
        self.all_sprites.add(self.platform_bottom, layer = 0)
        self.all_sprites.add(self.block4, layer = 0)
        self.all_sprites.add(self.bridge3, layer = 0)
        self.all_sprites.add(self.spike_down8, layer = 1)




    def update(self, dt):
        updown_elevator_movement(self.elevator_up_down, 170, dt)
        leftright_elevator_movement(self.elevator_left_right, 250, dt)
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        climb_ladder(self.player, [self.ladder])
        checkpoint_activation(self.player, [self.checkpoint])
        jump_from_the_top_of_ladder(self.player, [self.ladder])
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


