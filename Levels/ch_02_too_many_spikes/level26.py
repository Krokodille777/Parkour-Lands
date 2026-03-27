# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, Spike, TipCloud, FinishLevelTrigger, JumpPad, Lava, ElevatorLeftRight, ElevatorUpDown
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from elevators import leftright_elevator_movement, updown_elevator_movement
from maincamera import follow_player

class Level26:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(100, 0, 50, 50)
        self.wall1 = Ground(20, 0, 50, 80)
        self.ground = Ground(20, 80, 150, 50)
        self.elevator_up_down = ElevatorUpDown(275, 120, 80, 25, 75)
        self.wall2 = Ground(360, 0, 50, 300)
        self.ground2 = Ground(175, 250, 225, 50)
        self.wall3 = Ground(0, 200, 50, 500)
        self.ground3 = Ground(50, 520, 150, 300)
        self.spike_down = Spike(50, 470, 35, 50, 0)
        self.wall4 = Ground(200, 470, 50, 350)
        self.elevator_left_right = ElevatorLeftRight(300, 440, 80, 25, 75)
        self.lava_pool = Lava(250, 520, 250, 350)
        self.wall5 = Ground(500, 470, 75, 350)
        self.jumpPad = JumpPad(525, 445, 50, 25, -1300)
        self.spike_down2 = Spike(575, 500, 35, 50, 0)
        self.ground5 = Ground(575, 550, 50, 300)
        self.ground4 = Ground(610, 140, 125, 700)
        self.wall6 = Ground(735, 0, 50, 350)
        self.finish_level_trigger = FinishLevelTrigger(685, 40, 50, 100)
        self.tip_cloud = TipCloud(750, 150, 220, 200, "This game provides \n two types of elevators. \n One moves up and down. \n The other moves left and right. \n Try to use them to your advantage!")

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_down, self.spike_down2, self.elevator_left_right, self.elevator_up_down, self.jumpPad, self.lava_pool)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.wall1, self.ground, self.elevator_up_down, self.wall2, self.ground2, self.wall3, self.ground3, self.wall4, self.lava_pool, self.wall5, self.ground4, self.wall6, self.elevator_left_right, self.jumpPad)
     

        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.wall1, layer = 0)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.elevator_up_down, layer = 3)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.wall3, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.wall4, layer = 0)
        self.all_sprites.add(self.elevator_left_right, layer = 3)
        self.all_sprites.add(self.lava_pool, layer = 0)
        self.all_sprites.add(self.wall5, layer = 0)
        self.all_sprites.add(self.jumpPad, layer = 0)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.wall6, layer = 0)
        self.all_sprites.add(self.ground5, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 3) 


  
    def update(self, dt):
        updown_elevator_movement(self.elevator_up_down, 75, dt)
        leftright_elevator_movement(self.elevator_left_right, 75, dt)
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


