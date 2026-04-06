# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, Spike, Water, Ice, ElevatorUpDown, FragileGround, FinishLevelTrigger
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, buoyant_force
from fragile_ground import respawn_fragile_ground, trigger_fragile_ground, fragile_ground_check

from elevators import updown_elevator_movement
from maincamera import follow_player

class Level38:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(15, 30, 50, 50)
        self.block = Ground(0, 100, 50, 50)
        self.wall = Ground(0, 150, 25, 800)
        self.floor = Ground(25, 625, 150, 25)
        self.spike_down = Spike(150, 600, 25, 25, 0)
        self.elevator = ElevatorUpDown(75, 350, 75, 25, 250)
        self.ground = Ground(0, 650, 250, 600)
        self.spike_down2 = Spike(175, 625, 25, 25, 0)
        self.spike_down3 = Spike(200, 625, 25, 25, 0)
        self.spike_down4 = Spike(225, 625, 25, 25, 0)

        self.water_pool = Water(250, 750, 200, 85)
        self.floor2 = Ground(250, 835, 200, 500)
        self.fg1 = FragileGround(180, 470, 50, 50)
        self.fg2 = FragileGround(230, 420, 50, 50)
        self.fg3 = FragileGround(280, 370, 50, 50)

        self.ceiling = Ground(325, 0, 195, 100)
        self.wall2 = Ground (350, 35, 150, 650)
        
        self.ice = Ice(450, 750, 200, 35)
        self.ground2 = Ground(450, 785, 200, 500)
        self.wall3 = Ground(650, 450, 50, 300)
        self.spike_left = Spike(615, 700, 50, 35, 90)
        self.platform = Ground(500, 660, 25, 25)
        self.fg4 = FragileGround(625, 585, 25, 25)
        self.fg5 = FragileGround(500, 510, 25, 25)

        self.ceiling2 = Ground(450, 0, 400, 250)
        self.wall4 = Ground(800, 35, 50, 800)
        self.ground3 = Ground(650, 750, 150, 500)
        self.finish_level_trigger = FinishLevelTrigger(750, 650, 50, 100)


        self.box = Ground(1075, 1050, 25, 25)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.spike_down, self.spike_down2, self.spike_down3, self.spike_down4,  self.spike_left)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ice, self.ground, self.floor, self.floor2, self.fg1, self.fg2, self.fg3, self.ground2, self.ceiling, self.wall2, self.block, self.wall, self.elevator, self.wall3, self.platform, self.fg4, self.fg5, self.ceiling2, self.wall4, self.ground3)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 2)
        self.all_sprites.add(self.elevator, layer = 1)
        self.all_sprites.add(self.spike_down2, layer = 2)
        self.all_sprites.add(self.spike_down3, layer = 2)
        self.all_sprites.add(self.spike_down4, layer = 2)
        self.all_sprites.add(self.water_pool, layer = 1)
        self.all_sprites.add(self.floor2, layer = 0)
        self.all_sprites.add(self.fg1, layer = 1)
        self.all_sprites.add(self.fg2, layer = 1)
        self.all_sprites.add(self.fg3, layer = 1)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.ice, layer = 1)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.wall3, layer = 0)
        self.all_sprites.add(self.spike_left, layer = 2)
        self.all_sprites.add(self.platform, layer = 1)
        self.all_sprites.add(self.fg4, layer = 1)
        self.all_sprites.add(self.fg5, layer = 1)
        self.all_sprites.add(self.ceiling2, layer = 0)
        self.all_sprites.add(self.wall4, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.box, layer = 1)
        self.all_sprites.add(self.block, layer = 0)
        self.all_sprites.add(self.wall, layer = 0)
 
        

    def update(self, dt):    
        
        
        trigger_fragile_ground(self.player, self.box, [self.fg1, self.fg2, self.fg3, self.fg4, self.fg5])
        fragile_ground_check(self.player, self.box, [self.fg1, self.fg2, self.fg3, self.fg4, self.fg5], self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites,[self.fg1, self.fg2, self.fg3, self.fg4, self.fg5], dt)    
        
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
       
        updown_elevator_movement(self.elevator, 250, dt)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        buoyant_force(self.player, [self.water_pool])
        

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



    