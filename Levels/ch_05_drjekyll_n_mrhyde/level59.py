import pygame
from pygame.locals import *
from sprites import Player, AlterPlayer, AlterStand, Bridge,  PressTrap, Icicle, Button, ElevatorLeftRight, ElevatorUpDown, StartPortal, EndPortal, GravityJumpPad, Ladder, ControllableFan, FinishLevelTrigger, Lava, Door, Ice, TrapDoor, PushableBlock
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, frozen_adjustment, switch_to_alter_player, switch_to_normal_player, climb_ladder, jump_from_the_top_of_ladder
from physics import agt_move_and_collide, apply_agt
from pushableBlock import push_the_block, block_collisions
from portals import teleport_player, cooldown_timer, link_portals
from controllableFan import control_fan_from_button
from button_door_trap import press_button, link_button_to_door, link_button_to_fan, open_door_trapdoor, activate_fan_from_button
from maincamera import follow_player, follow_alter_player
from elevators import updown_elevator_movement, leftright_elevator_movement
from press_trap import update_press_trap, apply_press_trap_effect

class Level59:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (163, 182, 194)
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.ice_floor = Ice(0, 950, 250, 600)
        self.player = Player(30, 890, 50, 50)
        self.elevator = ElevatorLeftRight(135, 900, 75, 25, 115)
        self.lava = Lava(250, 955, 125, 550)
        self.ice_floor4 = Ice(375, 960, 625, 600)
        self.door = Door(300, 850, 25, 100)
        self.blue_portal = StartPortal(350, 850, 35, 50)
        self.ice_wall = Ice(410, 850, 65, 115)
        self.orange_portal = EndPortal(515, 850, 35, 50)
        self.small_ground = Bridge(475, 950, 30, 100)

        self.elevator2 = ElevatorLeftRight(590, 900, 75, 25, 75)
        self.icicle_down = Icicle(505, 925, 35,35, 0)
        self.icicle_down2 = Icicle(540, 925, 35,35, 0)
        self.icicle_down3 = Icicle(575, 925, 35,35, 0)
        self.icicle_down4 = Icicle(610, 925, 35,35, 0)
        self.icicle_down5 = Icicle(645, 925, 35,35, 0)
        self.icicle_down6 = Icicle(680, 925, 35,35, 0)
        self.small_ground2 = Bridge(715, 950, 60, 100)
        self.ice_wall2 = Ice(775, 0, 75, 1000)
        self.ice_wall3 = Ice(600, 545, 25, 305)
        self.icicle_right = Icicle(625, 600, 35, 35, -90)
        self.elevator3 = ElevatorUpDown(665, 690, 70, 25, 200)
        self.icicle_left = Icicle( 740, 600, 35, 35, 90)
        self.door2 = Door(600, 445, 25,100 )
        self.press_trap = PressTrap(600, 365, 80, 75, 90)
        self.finish_level_trigger = FinishLevelTrigger(700, 295, 50, 100)


        self.elevator4 = ElevatorLeftRight(300, 475, 75, 25, 250)

        self.ice_ceiling = Ice(235, 335, 365, 35)
        self.small_wall = Bridge(260, 370, 25, 50)
        self.cfan_left = ControllableFan(230, 370, 25, 75, (-1, 0), 10000, 1000)

        #Alter Room

        self.ice_floor2 = Ice(0, 815, 600, 35)
        self.ceiling = Bridge(0, 635, 220, 50 )
        self.button2 = Button(155, 685, 30, 25)
        self.button1 = Button(15, 785, 30, 25)
        self.alter_stand = AlterStand(65, 815, 50, 30)
        self.hyde = AlterPlayer(65, 765, 50, 50)
        self.wall = Bridge(315, 685, 100, 130)
        self.agt_jumpad = GravityJumpPad(235, 785, 50, 30, -800)
        self.ceiling2 = Bridge(285, 635, 185, 50)
        self.ice_floor3 = Ice(145, 545, 455, 25)
        self.agt_jumpad2 = GravityJumpPad(545, 560, 50, 30, 800)
        self.ladder = Ladder(470, 635, 25, 125)
        self.button3 = Button(525, 785, 50, 25)
        self.box = PushableBlock(525, 735, 50, 50)
        self.small_wall2 = Bridge(145, 545, 25, 90)
        self.lava2 = Lava(10, 565, 135, 75)
        self.ice_wall4 = Ice(-40, 0, 50, 635)
        self.platform = Bridge(5, 455, 40, 20)
        self.platform2 = Ice(100, 395, 35, 20)

        self.ice_ceiling2 = Ice(185, 0, 825, 250)
        self.icicle_up = Icicle(450, 250, 35, 35, 180)
        self.icicle_up2= Icicle(485, 250, 35, 35, 180)


        self.trapdoor = TrapDoor(600, 1500, 25, 50)

        self.door.linked_button = self.button1
        self.door2.linked_button = self.button2
        self.cfan_left.linked_button = self.button1
    

       
        self.triggers = pygame.sprite.Group()
        self.triggers.add( self.finish_level_trigger, self.press_trap, self.button1, self.button2, self.button3, self.ladder, self.lava, self.lava2, self.blue_portal, self.orange_portal, self.icicle_down, self.icicle_down2, self.icicle_down3, self.icicle_down4, self.icicle_down5, self.icicle_down6, self.icicle_right, self.icicle_left, self.icicle_up, self.icicle_up2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ice_floor, self.elevator, self.door, self.ice_floor4, self.ice_wall, self.ice_floor2, self.small_ground, self.elevator2, self.small_ground2, self.ice_wall2, self.ice_wall3, self.elevator3, self.door2, self.ice_ceiling, self.small_wall, self.ceiling, self.alter_stand, self.wall, self.ceiling2, self.ice_floor3,  self.small_wall2, self.ice_wall4, self.platform, self.platform2, self.ice_ceiling2, self.agt_jumpad, self.agt_jumpad2, self.press_trap, self.box, self.elevator4, self.trapdoor, self.cfan_left)

        self.all_sprites.add(self.ice_floor, layer = 0)
        self.all_sprites.add(self.elevator, layer = 1)
        self.all_sprites.add(self.lava, layer = 1)
        self.all_sprites.add(self.door, layer = 1)
        self.all_sprites.add(self.blue_portal, layer = 1)
        self.all_sprites.add(self.ice_wall, layer = 1)
        self.all_sprites.add(self.orange_portal, layer = 1)
        self.all_sprites.add(self.small_ground, layer = 0)
        self.all_sprites.add(self.elevator2, layer = 1)
        self.all_sprites.add(self.icicle_down, layer = 1)
        self.all_sprites.add(self.icicle_down2, layer = 1)
        self.all_sprites.add(self.icicle_down3, layer = 1)
        self.all_sprites.add(self.icicle_down4, layer = 1)
        self.all_sprites.add(self.icicle_down5, layer = 1)
        self.all_sprites.add(self.icicle_down6, layer = 1)
        self.all_sprites.add(self.small_ground2, layer = 0)
        self.all_sprites.add(self.ice_wall2, layer = 1)
        self.all_sprites.add(self.ice_wall3, layer = 1)
        self.all_sprites.add(self.icicle_right, layer = 1)
        self.all_sprites.add(self.elevator3, layer = 1)
        self.all_sprites.add(self.icicle_left, layer = 1)
        self.all_sprites.add(self.door, layer = 1)
        self.all_sprites.add(self.press_trap, layer = 1)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.ice_ceiling, layer = 1)
        self.all_sprites.add(self.small_wall, layer = 1)
        self.all_sprites.add(self.cfan_left, layer = 1)
        self.all_sprites.add(self.ice_floor2, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.button1, layer = 1)
        self.all_sprites.add(self.alter_stand, layer = 1)
        self.all_sprites.add(self.hyde, layer = 1)
        self.all_sprites.add(self.wall, layer = 1)
        self.all_sprites.add(self.agt_jumpad, layer = 1)
        self.all_sprites.add(self.ceiling2, layer = 1)
        self.all_sprites.add(self.ice_floor3, layer = 0)
        self.all_sprites.add(self.agt_jumpad2, layer = 1)
        self.all_sprites.add(self.ladder, layer = 1)
        self.all_sprites.add(self.button3, layer = 1)
        self.all_sprites.add(self.box, layer = 1)
        self.all_sprites.add(self.small_wall2, layer = 1)
        self.all_sprites.add(self.lava2, layer = 1)
        self.all_sprites.add(self.ice_wall4, layer = 1)
        self.all_sprites.add(self.platform, layer = 1)
        self.all_sprites.add(self.platform2, layer = 1)
        self.all_sprites.add(self.ice_ceiling2, layer = 1)
        self.all_sprites.add(self.icicle_up, layer = 1)
        self.all_sprites.add(self.icicle_up2, layer = 1)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.elevator4, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.door2, layer = 1)
        self.all_sprites.add(self.ice_floor4, layer = 1)



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
        self.box.handle_input(dt)
        leftright_elevator_movement(self.elevator, 115, dt)
        leftright_elevator_movement(self.elevator2, 75, dt)
        updown_elevator_movement(self.elevator3, 200, dt)
        leftright_elevator_movement(self.elevator4, 250, dt)

        if active_player.gravity_direction == "up":
            apply_agt(active_player, dt)
            agt_move_and_collide(active_player, self.colliders, dt, self.triggers)

        else:
            apply_gravity(active_player, dt)
            move_and_collide(active_player, self.colliders, dt, self.triggers)

        frozen_adjustment(self.player, self.colliders)
        frozen_adjustment(self.hyde, self.colliders)
        link_portals(self.blue_portal, self.orange_portal)
       

        crouching_adjustment(active_player, self.colliders)
        squash_adjustment(active_player, self.colliders)
        climb_ladder(active_player, [self.ladder])
        jump_from_the_top_of_ladder(active_player, [self.ladder])

        teleport_player(active_player, self.blue_portal)
        teleport_player(active_player, self.orange_portal)
        cooldown_timer(self.blue_portal, dt)
        cooldown_timer(self.orange_portal, dt)

        update_press_trap(self.press_trap, dt)

        apply_press_trap_effect(active_player, self.press_trap, dt)
  
        press_button([self.player, self.hyde], [self.box], [self.button1, self.button2, self.button3])
        link_button_to_door([self.button1, self.button2], [self.door, self.door2])
        link_button_to_fan([self.button3], [self.cfan_left])
        open_door_trapdoor([self.door, self.door2], [self.trapdoor])
        push_the_block(active_player, self.box, dt)
        
        block_collisions(self.box, self.colliders, dt, self.triggers)
        control_fan_from_button(
            [self.button3],
            [self.cfan_left],
            player=active_player,
            dt=dt,
            water_areas = None)
        

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
        screen.fill((163, 182, 194))
        for sprite in self.all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

    def is_finished(self):
        return self._active_player().rect.colliderect(self.finish_level_trigger.rect)



    
