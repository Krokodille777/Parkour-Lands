
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, Bridge, PushableBlock, Button, Door, TrapDoor, JumpPad, Lava, ElevatorLeftRight
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from pushableBlock import push_the_block, block_collisions
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor
from elevators import leftright_elevator_movement
from maincamera import follow_player

class Level44:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(90, 700, 50, 50)
        self.ground = Ground(0, 750, 1025, 500)
        self.door = Door(925, 650, 50, 100)
        self.ceiling = Ground(910, 500, 90, 150)
        self.button1 = Button(625, 715, 75, 35)
        self.door.linked_button = self.button1
        self.button2 = Button(325, 715, 75, 35)

        self.wall = Ground(0, 600, 25, 125)
        self.platform = Ground(25, 700, 50, 50)
        self.jumpPad = JumpPad(35, 675, 35, 25, -1000)

        self.wall2 = Ground(290, 270, 50, 85)
        self.block1 = Ground(285, 355, 60, 35)
        self.trapdoor = TrapDoor(345, 360, 110, 25)
        self.trapdoor.linked_button = self.button2  
        self.block2= Ground(440, 355, 60, 35)
        self.wall3 = Ground(445, 270, 50, 85)
        self.box = PushableBlock(350, 155, 85, 85)

        self.floor = Ground(150, 600, 575, 25)
        self.smallWall = Bridge(150, 575, 25, 35)
        self.smallWall2 = Bridge(700, 575, 25, 35)
        self.lava = Lava(175, 580, 550, 25)
        self.elevator = ElevatorLeftRight(400, 500, 100, 35, 300)

        self.finish_level_trigger = FinishLevelTrigger(975, 650, 50, 100)
        

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.lava, self.box, self.door, self.ceiling, self.wall, self.wall2, self.block1, self.trapdoor, self.block2, self.wall3, self.floor, self.smallWall, self.smallWall2, self.elevator, self.platform, self.jumpPad)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.lava, layer = 0) 
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.door, layer = 1)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.button1, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.jumpPad, layer = 0)
        self.all_sprites.add(self.wall2, layer = 1)
        self.all_sprites.add(self.block1, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.block2, layer = 1)
        self.all_sprites.add(self.wall3, layer = 1)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.smallWall, layer = 1)
        self.all_sprites.add(self.smallWall2, layer = 1)
        self.all_sprites.add(self.lava, layer = 0)
        self.all_sprites.add(self.elevator, layer = 0)

        
        

    def update(self, dt):
        
        leftright_elevator_movement(self.elevator, 300, dt)
        self.player.handle_input()
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)

        press_button([self.player], self.colliders, [self.button1, self.button2])
        link_button_to_door([self.button1], [self.door])
        link_button_to_trapdoor([self.button2], [self.trapdoor])
        open_door_trapdoor([self.door], [self.trapdoor])

        
       
        block_collisions(self.box, self.colliders, dt, self.triggers)
        push_the_block(self.player, self.box,  dt)
       
        

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



    