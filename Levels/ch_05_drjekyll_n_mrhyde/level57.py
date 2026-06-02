import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, PushableBlock, ControllableFan, AlterStand, AlterPlayer, Spike, Button, Checkpoint, JumpPad,  StartPortal, EndPortal
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, frozen_adjustment, switch_to_alter_player, switch_to_normal_player
from pushableBlock import push_the_block, block_collisions
from portals import teleport_player, teleport_pushable_block, cooldown_timer, link_portals
from controllableFan import control_fan_from_button
from button_door_trap import press_button
from maincamera import follow_player, follow_alter_player
from checkpoint import checkpoint_activation

class Level57:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()

       #Alter Spawn Room

        self.groundFloor = Ground(0, 900, self.WORLD_WIDTH, 250)
        self.ground_wall = Ground(0, 750, 50, 150)
        self.ground_wall2 = Ground(950, 750, 100, 150)
        self.alter_stand = AlterStand(425, 900, 50, 50)
        self.hyde = AlterPlayer(425, 850, 50, 50)
        self.blue_portal1 = StartPortal(300, 750, 50, 75)
        self.tip1 = TipCloud(250, 750, 50, 50, "1")
        self.blue_portal2 = StartPortal(400, 750, 50, 75)
        self.tip2 = TipCloud(350, 750, 50, 50, "2")
        self.blue_portal3 = StartPortal(500, 750, 50, 75)
        self.tip3 = TipCloud(450, 750, 50, 50, "3")
        self.blue_portal4 = StartPortal(600, 750, 50, 75)
        self.tip4 = TipCloud(550, 750, 50, 50, "4")

        #4 Control Rooms

        #Room 1

        self.orange_portal1 = EndPortal(10, 275, 25, 75)
        self.tip11 = TipCloud(75, 275, 50, 50, "1")
        self.button1 = Button(80, 375, 50, 50)
        self.box1 = PushableBlock(80, 300, 50, 50)
    

        #Room 2
        self.orange_portal2 = EndPortal(10, 475, 25, 75)
        self.tip21 = TipCloud(75, 475, 50, 50, "2")
        self.button2 = Button(80, 575, 50, 50)
        self.box2 = PushableBlock(80, 500, 50, 50)

        #Room 3
        self.button3 = Button(855, 100, 50, 50)
        self.box3 = PushableBlock(855, 50, 50, 50)
        self.orange_portal3 = EndPortal(1000, 15, 25, 75)
        self.tip31 = TipCloud(850, 50, 50, 50, "3")

        #Room 4
        self.button4 = Button(855, 285, 50, 50)
        self.box4 = PushableBlock(855, 200, 50, 50)
        self.orange_portal4 = EndPortal(1000, 200, 25, 75)
        self.tip41 = TipCloud(850, 275, 50, 50, "4")


        # Main Area
        self.ground = Ground(0, 625, 200, 125)
        self.wall = Ground(175 ,275, 25, 350)
        self.between_rooms1 = Ground(0, 425, 175, 50)
        self.ceiling = Ground(0, 250, 200, 25)
        self.wall2 = Ground(-40, 0, 50, 750)
        self.main_ceiling = Ground(0, 0, 700, 150)
        self.extra_ceiling = Ground(700, 0, 100, 50)
        self.wall3 = Ground(800, 0, 25, 535)
        self.between_rooms2 = Ground(825, 150, 225, 50)
        self.ground2 = Ground(825, 335, 250, 200)
        self.wall4= Ground(900, 535, 175, 100)
        self.wall5 = Ground(1025, 0, 500, 1000)
        self.ground3 = Ground(300, 635, 750, 115)
        self.tiny_ground = Ground(200, 725, 100, 25)

        #In the Middle

        self.jump_pad = JumpPad(220, 700, 50, 25, -1000)
        self.player = Player (295, 485, 50, 50)
        self.cfan_up = ControllableFan(650, 635, 125, 50, (0, -1), 30000, 600)
        self.tip411 = TipCloud(625, 550, 50, 50, "4")
        self.checkpoint = Checkpoint(825, 585, 50, 50)
        self.centersquare = Ground(400, 285, 200, 200)
        self.cfan_left = ControllableFan(775, 175, 50, 125, (-1, 0), 30000, 600)
        self.tip311 = TipCloud(750, 150, 50, 50, "3")
        self.spike_up = Spike(700, 50, 25, 25, 180)
        self.spike_ip2 = Spike(725, 50, 25, 25, 180)
        self.spike_ip3 = Spike(750, 50, 25, 25, 180)
        self.spike_ip4 = Spike(775, 50, 25, 25, 180)
        self.cfan_down = ControllableFan(225, 115, 125, 50, (0, 1), 30000, 1000)
        self.tip111 = TipCloud(200, 100, 50, 50, "1")

       
        self.finish_level_trigger = FinishLevelTrigger(100, 150, 50, 100)
        self.cfan_right = ControllableFan(175, 500, 50, 125, (1, 0), 30000, 600)
        self.tip211 = TipCloud(150, 450, 50, 50, "2")


        self.blue_portal1.linked_portal = self.orange_portal1
        self.orange_portal1.linked_portal = self.blue_portal1
        self.blue_portal2.linked_portal = self.orange_portal2
        self.orange_portal2.linked_portal = self.blue_portal2
        self.blue_portal3.linked_portal = self.orange_portal3
        self.orange_portal3.linked_portal = self.blue_portal3
        self.blue_portal4.linked_portal = self.orange_portal4
        self.orange_portal4.linked_portal = self.blue_portal4

        self.cfan_down.linked_button = self.button1
        self.cfan_right.linked_button = self.button2
        self.cfan_left.linked_button = self.button3
        self.cfan_up.linked_button = self.button4
       
        self.triggers = pygame.sprite.Group()
        self.triggers.add( self.button1, self.button2, self.button3, self.button4, self.finish_level_trigger, self.checkpoint, self.blue_portal1, self.blue_portal2, self.blue_portal3, self.blue_portal4, self.orange_portal1, self.orange_portal2, self.orange_portal3, self.orange_portal4, self.spike_up, self.spike_ip2, self.spike_ip3, self.spike_ip4)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.wall, self.ceiling, self.wall5, self.wall2, self.main_ceiling, self.extra_ceiling, self.wall3, self.between_rooms1, self.ground2, self.wall4, self.ground3, self.tiny_ground, self.groundFloor, self.ground_wall, self.ground_wall2, self.alter_stand, self.centersquare, self.jump_pad, self.box1, self.box2, self.box3, self.box4, self.cfan_up, self.cfan_left, self.cfan_down, self.cfan_right, self.between_rooms2)

        self.all_sprites.add(self.ground, layer = 1)
        self.all_sprites.add(self.wall, layer = 1)
        self.all_sprites.add(self.ceiling, layer = 1)
        self.all_sprites.add(self.wall2, layer = 1)
        self.all_sprites.add(self.main_ceiling, layer = 1)
        self.all_sprites.add(self.extra_ceiling, layer = 1)
        self.all_sprites.add(self.wall3, layer = 1)
        self.all_sprites.add(self.between_rooms1, layer = 1)
        self.all_sprites.add(self.ground2, layer = 1)
        self.all_sprites.add(self.wall4, layer = 1)
        self.all_sprites.add(self.ground3, layer = 1)
        self.all_sprites.add(self.tiny_ground, layer = 1)
        self.all_sprites.add(self.jump_pad, layer = 2)
        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.cfan_up, layer = 2)
        self.all_sprites.add(self.checkpoint, layer = 2)
        self.all_sprites.add(self.centersquare, layer = 1)
        self.all_sprites.add(self.cfan_left, layer = 2)
        self.all_sprites.add(self.spike_up, layer = 2)
        self.all_sprites.add(self.spike_ip2, layer = 2)
        self.all_sprites.add(self.spike_ip3, layer = 2)
        self.all_sprites.add(self.spike_ip4, layer = 2)
        self.all_sprites.add(self.cfan_down, layer = 2)
        self.all_sprites.add(self.blue_portal1, layer = 2)
        self.all_sprites.add(self.tip1, layer = 3)
        self.all_sprites.add(self.blue_portal2, layer = 2)
        self.all_sprites.add(self.tip2, layer = 3)
        self.all_sprites.add(self.blue_portal3, layer = 2)
        self.all_sprites.add(self.tip3, layer = 3)
        self.all_sprites.add(self.blue_portal4, layer = 2)
        self.all_sprites.add(self.tip4, layer = 3)
        self.all_sprites.add(self.orange_portal1, layer = 2)
        self.all_sprites.add(self.tip11, layer = 3)
        self.all_sprites.add(self.button1, layer = 2)
        self.all_sprites.add(self.box1, layer = 2)
        self.all_sprites.add(self.orange_portal2, layer = 2)
        self.all_sprites.add(self.tip21, layer = 3)
        self.all_sprites.add(self.button2, layer = 2)
        self.all_sprites.add(self.box2, layer = 2)
        self.all_sprites.add(self.button3, layer = 2)
        self.all_sprites.add(self.box3, layer = 2)
        self.all_sprites.add(self.orange_portal3, layer = 2)
        self.all_sprites.add(self.tip31, layer = 3)
        self.all_sprites.add(self.button4, layer = 2)
        self.all_sprites.add(self.box4, layer = 2)
        self.all_sprites.add(self.orange_portal4, layer = 2)
        self.all_sprites.add(self.tip41, layer = 3)
        self.all_sprites.add(self.groundFloor, layer = 1)
        self.all_sprites.add(self.ground_wall, layer = 1)
        self.all_sprites.add(self.ground_wall2, layer = 1)
        self.all_sprites.add(self.alter_stand, layer = 1)
        self.all_sprites.add(self.hyde, layer = 3)
        self.all_sprites.add(self.finish_level_trigger, layer = 2)
        self.all_sprites.add(self.cfan_right, layer = 2)
        self.all_sprites.add(self.tip211, layer = 3)
        self.all_sprites.add(self.tip111, layer = 3)
        self.all_sprites.add(self.tip311, layer = 3)
        self.all_sprites.add(self.tip411, layer = 3)
        self.all_sprites.add(self.wall5, layer = 1)
        self.all_sprites.add(self.between_rooms2, layer = 1)



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
        self.box2.handle_input(dt)
        self.box3.handle_input(dt)
        self.box4.handle_input(dt)
  
        push_the_block(active_player, self.box1, dt)
        push_the_block(active_player, self.box2, dt)
        push_the_block(active_player, self.box3, dt)
        push_the_block(active_player, self.box4, dt)
        press_button([self.hyde], [self.box1, self.box2, self.box3, self.box4], [self.button1, self.button2, self.button3, self.button4])
       
        control_fan_from_button(
            [self.button1, self.button2, self.button3, self.button4],
            [self.cfan_down, self.cfan_right, self.cfan_left, self.cfan_up],
            self.player,
            [self.box1, self.box2, self.box3, self.box4],
            dt,
            water_areas=[],
        )
       
        apply_gravity(active_player, dt)
        move_and_collide(active_player, self.colliders, dt, self.triggers)
        
        frozen_adjustment(self.player, self.colliders)
        frozen_adjustment(self.hyde, self.colliders)

        
        link_portals(self.blue_portal1, self.orange_portal1)
        link_portals(self.blue_portal2, self.orange_portal2)
        link_portals(self.blue_portal3, self.orange_portal3)
        link_portals(self.blue_portal4, self.orange_portal4)



        crouching_adjustment(active_player, self.colliders)
        squash_adjustment(active_player, self.colliders)

        teleport_player(active_player, self.blue_portal1)
        teleport_player(active_player, self.orange_portal1)
        teleport_pushable_block(self.box1, self.blue_portal1)
        teleport_pushable_block(self.box1, self.orange_portal1)
        cooldown_timer(self.blue_portal1, dt)
        cooldown_timer(self.orange_portal1, dt)
        teleport_player(active_player, self.blue_portal2)
        teleport_player(active_player, self.orange_portal2)
        teleport_pushable_block(self.box2, self.blue_portal2)
        teleport_pushable_block(self.box2, self.orange_portal2)
        cooldown_timer(self.blue_portal2, dt)
        cooldown_timer(self.orange_portal2, dt)
        teleport_player(active_player, self.blue_portal3)
        teleport_player(active_player, self.orange_portal3)
        teleport_pushable_block(self.box3, self.blue_portal3)
        teleport_pushable_block(self.box3, self.orange_portal3)
        cooldown_timer(self.blue_portal3, dt)
        cooldown_timer(self.orange_portal3, dt)
        teleport_player(active_player, self.blue_portal4)
        teleport_player(active_player, self.orange_portal4)
        teleport_pushable_block(self.box4, self.blue_portal4)
        teleport_pushable_block(self.box4, self.orange_portal4)
        cooldown_timer(self.blue_portal4, dt)
        cooldown_timer(self.orange_portal4, dt)


        block_collisions(self.box1, self.colliders, dt, self.triggers)
        block_collisions(self.box2, self.colliders, dt, self.triggers)
        block_collisions(self.box3, self.colliders, dt, self.triggers)
        block_collisions(self.box4, self.colliders, dt, self.triggers)

        
        checkpoint_activation(active_player, [self.checkpoint])

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



    
