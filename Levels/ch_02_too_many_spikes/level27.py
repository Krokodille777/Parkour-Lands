import pygame
from pygame.locals import *
from sprites import Player, Ground, Spike, FinishLevelTrigger, JumpPad, Bridge, ElevatorLeftRight, Checkpoint
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder
from elevators import leftright_elevator_movement
from checkpoint import checkpoint_activation
from maincamera import follow_player

class Level27:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 0, 50, 50)
        self.ground = Ground(0, 100, 450, 50)
        self.bridge = Bridge(450, 100, 150, 25)
        self.wall1 = Ground(750, 0, 50, 300)
        self.spike_up = Spike(415, 150, 35, 50, 180)
        self.spike_up2 = Spike(380, 150, 35, 50, 180)
        self.elevator_left_right = ElevatorLeftRight(425, 240, 80, 25, 225)
        self.ground2 = Ground(195, 270, 575, 50)
        self.wall2 = Ground(0, 150, 75, 300)
        self.ground3 = Ground(75, 400, 75, 50)
        self.checkpoint = Checkpoint(100, 350, 50, 50)
        self.block1 = Ground(125, 450, 50, 275)
        self.ground4 = Ground(150, 675, 550, 500)
        self.jumpPad = JumpPad(300, 650, 50, 25, -1700)
        self.jumpPad2 = JumpPad(550, 650, 50, 25, -1700)

        self.spike_up3 = Spike(292.5, 320, 35, 50, 180)
        self.spike_up4 = Spike(327.5, 320, 35, 50, 180)

 

        self.spike_up5 = Spike(532.5, 320, 35, 50, 180)
        self.spike_up6 = Spike(567.5, 320, 35, 50, 180)
 
        self.block2 = Ground(700, 650, 50, 75)
        self.block3 = Ground(750, 625, 50, 125)
        self.block4 = Ground(800, 600, 100, 200)
    
        self.final_jumpPad = JumpPad(850, 575, 50, 25, -1700)
        self.ground5 = Ground(900, 100, 100, 1000)
        self.finish_level_trigger = FinishLevelTrigger(950, 0, 50, 100)
     
        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_up, self.spike_up2, self.spike_up3, self.spike_up4, self.spike_up5, self.spike_up6)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.ground3, self.ground4, self.ground5, self.block1, self.block2, self.block3, self.block4, self.wall1, self.wall2, self.bridge, self.elevator_left_right, self.jumpPad, self.jumpPad2, self.final_jumpPad)
    
        self.all_sprites.add(self.player, layer=2)
        self.all_sprites.add(self.ground, layer=0)
        self.all_sprites.add(self.bridge, layer=0)
        self.all_sprites.add(self.wall1, layer=0)
        self.all_sprites.add(self.spike_up, layer=1)
        self.all_sprites.add(self.spike_up2, layer=1)
        self.all_sprites.add(self.elevator_left_right, layer=3)
        self.all_sprites.add(self.ground2, layer=0)
        self.all_sprites.add(self.wall2, layer=0)
        self.all_sprites.add(self.ground3, layer=0)
        self.all_sprites.add(self.checkpoint, layer=1)
        self.all_sprites.add(self.block1, layer=0)
        self.all_sprites.add(self.ground4, layer=0)
        self.all_sprites.add(self.jumpPad, layer=0)
        self.all_sprites.add(self.jumpPad2, layer=0)
        self.all_sprites.add(self.spike_up3, layer=1)
        self.all_sprites.add(self.spike_up4, layer=1)
        self.all_sprites.add(self.spike_up5, layer=1)
        self.all_sprites.add(self.spike_up6, layer=1)
        self.all_sprites.add(self.block2, layer=0)
        self.all_sprites.add(self.block3, layer=0)
        self.all_sprites.add(self.block4, layer=0)
        self.all_sprites.add(self.final_jumpPad, layer=0)
        self.all_sprites.add(self.ground5, layer=0)
        self.all_sprites.add(self.finish_level_trigger, layer=1)
        self.checkpoints = [self.checkpoint]
    def update(self, dt):
       leftright_elevator_movement(self.elevator_left_right, 225, dt)
       self.player.handle_input()
       apply_gravity(self.player, dt)
       move_and_collide(self.player, self.colliders, dt, self.triggers)
       crouching_adjustment(self.player, self.colliders)
       squash_adjustment(self.player, self.colliders)
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
