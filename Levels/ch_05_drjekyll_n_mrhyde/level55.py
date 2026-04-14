
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, AlterStand, AlterPlayer, Bridge, Lava, Button, TrapDoor, Door, Spike, JumpPad, GravityJumpPad, Checkpoint, Ladder, PressTrap, StartPortal, EndPortal
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, frozen_adjustment, climb_ladder, jump_from_the_top_of_ladder, apply_agt, agt_move_and_collide, switch_to_alter_player, switch_to_normal_player
from pushableBlock import push_the_block, block_collisions
from button_door_trap import press_button,  link_button_to_trapdoor, open_door_trapdoor
from checkpoint import checkpoint_activation
from press_trap import apply_press_trap_effect, update_press_trap
from portals import teleport_player, teleport_pushable_block, cooldown_timer, link_portals

from maincamera import follow_player, follow_alter_player

class Level55:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(20, 700, 50, 50)
        self.ground = Ground(0, 750, 80, 500)
        self.lava = Lava(80, 760, 280, 490)
        self.trapdoor = TrapDoor(80, 750, 280, 15)
        self.concrete_wall = Ground(360, 750, 10, 500)
        self.floor = Ground(370, 800, 65, 450)
        self.jumpPad = JumpPad(375, 775, 50, 25, -1500)
        self.trapdoor2 = TrapDoor(370, 750, 65, 15)
        self.wall = Ground(435, 750, 25, 500)
        self.ground2 = Ground(455, 755, 545, 495)
        self.checkpoint = Checkpoint(600, 705, 50, 50)
        self.ground3 = Ground(775, 655, 225, 100)

        self.platform = Bridge(0, 550, 150, 25)
        self.alter_stand = AlterStand(5, 525, 50, 25)
        self.hyde = AlterPlayer(5, 475, 50, 50)
        self.gravity_jumpPad = GravityJumpPad(100, 525, 50, 25, -3000)

        self.platform2 = Bridge(175, 450, 60, 25)
        self.box1= PushableBlock(165, 365, 85, 85)
        self.button = Button(175, 340, 60, 35)
        self.gravity_jumpPad2 = GravityJumpPad(235, 340, 50, 25, 3000)

        self.lone_block = Bridge(265, 550, 25, 25)

        self.platform3 = Ground(475, 525, 65, 35)
        self.small_wall =Ground(525, 475, 25, 100)
        self.button2= Button(475, 500, 50, 25)

        self.platform4 = Ground(700, 425, 100, 25)
        self.button3 = Button(745, 400, 50, 25)
        self.ladder = Ladder(800, 425, 50, 200)

        self.floor2 = Ground(325, 390, 375, 25)
        self.small_wall2 = Ground(775, 0, 25, 355)
        self.small_ceiling = Ground(385, 0, 390, 255)
        self.trapdoor3 = TrapDoor(685, 325, 90, 25)
        self.blue_portal = StartPortal(715, 250, 50, 75)
        self.press_trap1 = PressTrap(585, 255, 100, 50, 180)
        self.press_trap2 = PressTrap(485, 255, 100, 50, 180)
        self.press_trap3 = PressTrap(385, 255, 100, 50, 180)
        self.orange_portal = EndPortal(330, 295, 50, 75)
        self.ladder2 = Ladder(300, 265, 25, 100)

        self.ground4 = Ground(150, 255, 150, 85)
        self.ground5 = Ground(0, 240, 150, 85)
        self.spike_down = Spike(125, 215, 25, 25, 0)
        self.finish_level_trigger = FinishLevelTrigger(10, 140, 50, 100)

        self.door = Door(1500, 265, 100, 185)

        self.trapdoor.linked_button = self.button
        self.trapdoor3.linked_button = self.button2
        self.trapdoor2.linked_button = self.button3
        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.button, self.button2, self.button3, self.blue_portal, self.orange_portal, self.spike_down, self.press_trap1, self.press_trap2, self.press_trap3, self.ladder, self.ladder2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.ground4, self.jumpPad, self.floor, self.floor2, self.gravity_jumpPad, self.gravity_jumpPad2, self.ground5, self.alter_stand, self.player, self.hyde,  self.platform2,  self.box1, self.wall, self.ground3, self.platform, self.lone_block, self.platform3, self.small_wall, self.platform4, self.small_wall2, self.small_ceiling, self.trapdoor, self.trapdoor2, self.trapdoor3, self.lava)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.alter_stand, layer = 1)
        self.all_sprites.add(self.hyde, layer = 2)
        self.all_sprites.add(self.platform2, layer = 1)
        self.all_sprites.add(self.box1, layer = 1)
        self.all_sprites.add(self.wall, layer = 1)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.platform, layer = 1)
        self.all_sprites.add(self.lone_block, layer = 1)
        self.all_sprites.add(self.platform3, layer = 1)
        self.all_sprites.add(self.small_wall, layer = 1)
        self.all_sprites.add(self.platform4, layer = 1)
        self.all_sprites.add(self.small_wall2, layer = 1)
        self.all_sprites.add(self.small_ceiling, layer = 1)
        self.all_sprites.add(self.blue_portal, layer = 1)
        self.all_sprites.add(self.orange_portal, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 1)
        self.all_sprites.add(self.trapdoor2, layer = 1)
        self.all_sprites.add(self.lava, layer = 1)
        self.all_sprites.add(self.jumpPad, layer = 1)
        self.all_sprites.add(self.gravity_jumpPad, layer = 1)
        self.all_sprites.add(self.button, layer = 1)
        self.all_sprites.add(self.button2, layer = 1)
        self.all_sprites.add(self.button3, layer = 1)
        self.all_sprites.add(self.gravity_jumpPad2, layer = 1)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.press_trap1, layer = 1)
        self.all_sprites.add(self.press_trap2, layer = 1)
        self.all_sprites.add(self.press_trap3, layer = 1)
        self.all_sprites.add(self.checkpoint, layer = 1)
        self.all_sprites.add(self.ladder, layer = 1)
        self.all_sprites.add(self.ladder2, layer = 1)
        self.all_sprites.add(self.trapdoor3, layer = 1)
        self.all_sprites.add(self.floor, layer = 1)
        self.all_sprites.add(self.floor2, layer = 1)
        self.all_sprites.add(self.concrete_wall, layer = 1)
        self.all_sprites.add(self.ground4, layer = 1)
        self.all_sprites.add(self.ground5, layer = 1)



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
        climb_ladder(active_player, [self.ladder, self.ladder2])
        jump_from_the_top_of_ladder(active_player, [self.ladder, self.ladder2])

        teleport_player(active_player, self.blue_portal)
        teleport_player(active_player, self.orange_portal)
        teleport_pushable_block(self.box1, self.blue_portal)
        teleport_pushable_block(self.box1, self.orange_portal)
        cooldown_timer(self.blue_portal, dt)
        cooldown_timer(self.orange_portal, dt)

        update_press_trap(self.press_trap1, dt)
        update_press_trap(self.press_trap2, dt)
        update_press_trap(self.press_trap3, dt)
        apply_press_trap_effect(active_player, self.press_trap1, dt)
        apply_press_trap_effect(active_player, self.press_trap2, dt)
        apply_press_trap_effect(active_player, self.press_trap3, dt)
        press_button([self.player, self.hyde], [self.box1], [self.button, self.button2, self.button3])
        link_button_to_trapdoor([self.button], [self.trapdoor])
        link_button_to_trapdoor([self.button2], [self.trapdoor3])
        link_button_to_trapdoor([self.button3], [self.trapdoor2])
        open_door_trapdoor([self.door], [self.trapdoor, self.trapdoor2, self.trapdoor3])
        push_the_block(active_player, self.box1, dt)
        
        block_collisions(self.box1, self.colliders, dt, self.triggers)

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



    
