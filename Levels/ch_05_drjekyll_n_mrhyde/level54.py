import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, AlterStand, AlterPlayer, Button, Door, TrapDoor, FragileGround, ElevatorLeftRight, Spike, Ladder, Ice, Bridge
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, climb_ladder, jump_from_the_top_of_ladder, frozen_adjustment, switch_to_alter_player, switch_to_normal_player
from pushableBlock import push_the_block, block_collisions
from elevators import leftright_elevator_movement
from fragile_ground import trigger_fragile_ground, fragile_ground_check, respawn_fragile_ground
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor
from maincamera import follow_player, follow_alter_player

class Level54:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 700, 50, 50)
        self.ground = Ground(0, 750, 1000, 500)
        self.ladder = Ladder(260, 590, 50, 100)
        self.main_button = Button(700, 700, 75, 50)
        self.door = Door(900, 650, 50, 100)
        self.door.linked_button = self.main_button
        self.block = Ground(850, 600, 150, 50)

        self.cabin_floor = Bridge(175, 600, 70, 25)
        self.cabin_wall = Bridge(175, 490, 25, 110)
        self.cabin_ceiling = Bridge(200, 490, 170, 25)
        self.cabin_wall2 = Bridge(370, 490, 25, 110)
        self.cabin_floor2 = Bridge(325, 600, 70, 25)
        self.button1 = Button(200, 520, 35, 75)
        self.button2 = Button(335, 520, 35, 75)


        self.alter_stand = AlterStand(140, 340, 50, 35)
        self.hyde = AlterPlayer(140, 290, 50, 50)
        self.wall = Ground(90, 0, 50, 400)
        self.platform2 = Ground(135, 375, 75, 25)
        self.trapdoor = TrapDoor(210, 375, 75, 25)
        self.wall2 = Ground(285, 0, 25, 375)
        self.wall3 = Ground(185, 400, 25, 95)
        self.ice = Ice(185, 465, 225, 25)
        self.floor2 = Ground(405, 465, 125, 25)
        self.spike_down = Spike(405, 440,25, 25, 0)
        self.spike_down2 = Spike(430, 440, 25, 25, 0)
        self.spike_down3 = Spike(455, 440, 25, 25, 0)
        self.spike_down4 = Spike(480, 440, 25, 25, 0)
        self.spike_down5 = Spike(505, 440, 25, 25, 0)
        self.platform3 = Ground(310, 365, 25, 25)

        self.elevator = ElevatorLeftRight(395, 300, 65, 25, 50)

        self.fg1 = FragileGround(530, 325, 50, 35)
        self.fg2 = FragileGround(580, 360, 50, 35)
        self.floor3 = Ground(530, 465, 150, 25)
        self.ground2 = Ground(630, 430, 50, 35)
        self.box1 = PushableBlock(630, 365, 65, 65)
        self.trapdoor2 = TrapDoor(680, 430, 100, 25)
        self.wall4 = Ground(780, 0, 150, 600)

        self.platform4 = Ground(620, 0, 35, 250)
        self.spike_up = Spike(625, 250, 25, 25, 180)

       
        self.finish_level_trigger = FinishLevelTrigger(950, 650, 50, 100)

        self.trapdoor.linked_button = self.button1
        self.trapdoor2.linked_button = self.button2


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.button1, self.button2, self.main_button, self.spike_up, self.spike_down, self.spike_down2, self.spike_down3, self.spike_down4, self.spike_down5)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.block, self.door, self.fg1, self.fg2, self.elevator, self.platform4, self.alter_stand, self.player, self.hyde,  self.platform2,  self.box1, self.wall, self.platform3, self.floor2, self.floor3, self.ice, self.cabin_floor, self.cabin_wall, self.cabin_ceiling, self.cabin_wall2, self.cabin_floor2, self.trapdoor, self.trapdoor2, self.wall2, self.wall3, self.wall4)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.alter_stand, layer = 1)
        self.all_sprites.add(self.hyde, layer = 2)
        self.all_sprites.add(self.platform2, layer = 1)
        self.all_sprites.add(self.box1, layer = 1)
        self.all_sprites.add(self.wall, layer = 1)
        self.all_sprites.add(self.ladder, layer = 1)
        self.all_sprites.add(self.cabin_floor, layer = 1)
        self.all_sprites.add(self.cabin_wall, layer = 1)
        self.all_sprites.add(self.cabin_ceiling, layer = 1)
        self.all_sprites.add(self.cabin_wall2, layer = 1)
        self.all_sprites.add(self.cabin_floor2, layer = 1)
        self.all_sprites.add(self.button1, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.wall2, layer = 1)
        self.all_sprites.add(self.wall3, layer = 1)
        self.all_sprites.add(self.ice, layer = 1)
        self.all_sprites.add(self.floor2, layer = 1)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.spike_down3, layer = 1)
        self.all_sprites.add(self.spike_down4, layer = 1)
        self.all_sprites.add(self.spike_down5, layer = 1)
        self.all_sprites.add(self.platform3, layer = 1)
        self.all_sprites.add(self.elevator, layer = 1)
        self.all_sprites.add(self.fg1, layer = 1)
        self.all_sprites.add(self.fg2, layer = 1)
        self.all_sprites.add(self.floor3, layer = 1)
        self.all_sprites.add(self.ground2, layer = 1)
        self.all_sprites.add(self.trapdoor2 , layer = 1)
        self.all_sprites.add(self.wall4, layer = 1)
        self.all_sprites.add(self.platform3, layer = 1)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.block, layer = 1)
        self.all_sprites.add(self.main_button, layer = 0)
        self.all_sprites.add(self.platform4, layer = 1)
        self.all_sprites.add(self.door, layer = 1)



    def _active_player(self):
        return self.hyde if not self.hyde.frozen else self.player

    def _handle_switch_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_1]:
            switch_to_normal_player(self.player, self.hyde)
        elif keys[K_2]:
            switch_to_alter_player(self.player, self.hyde)

    def update(self, dt):
        self._handle_switch_input()
        
        active_player = self._active_player()

        active_player.handle_input(dt)
        self.box1.handle_input(dt)
        leftright_elevator_movement(self.elevator,50, dt)
        trigger_fragile_ground(active_player, self.box1, [self.fg1, self.fg2])
        fragile_ground_check(active_player, self.box1, [self.fg1, self.fg2], self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites, [self.fg1, self.fg2], dt)
        frozen_adjustment(self.player, self.colliders)
        frozen_adjustment(self.hyde, self.colliders)

        apply_gravity(active_player, dt)
        move_and_collide(active_player, self.colliders, dt, self.triggers)
        crouching_adjustment(active_player, self.colliders)
        squash_adjustment(active_player, self.colliders)
        climb_ladder(active_player, [self.ladder])
        jump_from_the_top_of_ladder(active_player, [self.ladder])


        press_button([self.player, self.hyde], [self.box1], [self.button1, self.button2, self.main_button])
        link_button_to_door([self.main_button], [self.door])
        link_button_to_trapdoor([self.button1, self.button2], [self.trapdoor, self.trapdoor2])
        open_door_trapdoor([self.door], [self.trapdoor, self.trapdoor2])


        push_the_block(active_player, self.box1, dt)
        block_collisions(self.box1, self.colliders, dt, self.triggers)

    def draw(self, screen):
        active_player = self._active_player()
        if active_player is self.hyde:
            offset_x, offset_y = follow_alter_player(
            self.hyde,
            screen.get_width(),
            self.WORLD_WIDTH,
            screen.get_height(),
            self.WORLD_HEIGHT,
        )
        else:
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
        return self._active_player().rect.colliderect(self.finish_level_trigger.rect)



    
