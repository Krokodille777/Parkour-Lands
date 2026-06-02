import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, ControllableFan, AlterStand, AlterPlayer, Bridge, DynamicSpike, DynamicSpikePlatform, Button, TrapDoor, Door, Water,  StartPortal, EndPortal
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment, frozen_adjustment, buoyant_force, switch_to_alter_player, switch_to_normal_player
from pushableBlock import push_the_block, block_collisions
from button_door_trap import press_button,  link_button_to_trapdoor, open_door_trapdoor
from portals import teleport_player, teleport_pushable_block, cooldown_timer, link_portals
from dynamic_spike import dynamic_spike_movement_based_on_timer
from controllableFan import control_fan_from_button
from maincamera import follow_player, follow_alter_player

class Level56:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()

        #Big Heart
        self.water = Water(0, 0, self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.ground = Ground(0, 850, self.WORLD_WIDTH, 650)
        self.ground1left = Ground(0, 800, 355, 50)
        self.ground1right = Ground(620, 800, 600, 50)
        self.ground2left = Ground(0, 750, 335, 50)
        self.ground2right = Ground(640, 750, 600, 50)
        self.ground3left = Ground(0, 675, 300, 75)
        self.ground3right = Ground(675, 675, 600, 75)
        self.ground4left = Ground(0, 650, 250, 25)
        self.ground4right = Ground(725, 650, 600, 25)
        self.ground5left = Ground(0, 585, 200, 65)
        self.ground5right = Ground(775, 585, 600, 65)
        self.ground6left = Ground(0, 510, 175, 75)
        self.ground6right = Ground(800, 510, 600, 75)
        self.ground7left = Ground(0, 455, 150, 65)
        self.ground7right = Ground(825, 455, 600, 65)
        self.ground8left = Ground(0, 400, 175, 55)
        self.ground8right = Ground(800, 380, 600, 75)
        self.ground9left = Ground(0, 335, 225, 65)
        self.ground9right = Ground(750, 335, 600, 65)
        self.ground10 = Ground(0, 0, self.WORLD_WIDTH, 335)
        self.ground11 = Ground(375, 335, 225, 50)
        self.ground12 = Ground(450, 365, 70, 50)

        #Small Heart in the middle
        self.small_ground = Ground(450, 635, 75, 25)
        self.small_ground1left = Ground(425, 625, 25, 25)
        self.small_ground1right = Ground(525, 625, 25, 25)
        self.small_ground2left = Ground(400, 600, 50, 25)
        self.small_ground2right = Ground(525, 600, 50, 25)
        self.small_ground3left = Ground(375, 575, 75, 25)
        self.small_ground3right = Ground(525, 575, 75, 25)
        self.small_ground4left = Ground(350, 525, 100, 50)
        self.small_ground4right = Ground(525, 525, 100, 50)
        self.small_ground5left = Ground(375, 500, 75, 25)
        self.small_ground5right = Ground(525, 500, 75, 25)
        self.small_ground6left = Ground(425, 475, 25, 25)
        self.small_ground6right = Ground(525, 475, 25, 25)

        #Inside the big heart

        self.wall = Bridge(475, 660, 25, 190)
        self.player = Player(405, 800, 50, 50)
        self.alter_stand = AlterStand(525, 850, 50, 25)
        self.hyde = AlterPlayer(525, 800, 50, 50)
        self.platform1left = Bridge(395, 755, 80, 25)
        self.blue_portal = StartPortal(430, 705, 25, 50)
        self.platform1right = Bridge(500, 755, 80, 25)
        self.dsp1 = DynamicSpikePlatform(300, 735, 35, 25)
        self.dsu1 = DynamicSpike(300, 732, 16, 16, 0)
        self.dsu2 = DynamicSpike(308, 732, 16, 16, 0)
        self.dsp2 = DynamicSpikePlatform(640, 735, 35, 25)
        self.dsu4 = DynamicSpike(648, 732, 16, 16, 0)
        self.dsu5 = DynamicSpike(656, 732, 16, 16, 0)

        self.dsp3 = DynamicSpikePlatform(240, 650, 35, 25)
        self.dsr1 = DynamicSpike(260, 650, 25, 25, -90)
        self.dsp4 = DynamicSpikePlatform(725, 650, 35, 25)
        self.dsl1 = DynamicSpike(715, 650, 25, 25, 90)
        self.dsp5 = DynamicSpikePlatform(330, 525, 35, 50)
        self.dsl2 = DynamicSpike(320, 525, 25, 25, 90)
        self.dsl3 = DynamicSpike(320, 550, 25, 25, 90)
        self.dsp6 = DynamicSpikePlatform(590, 525, 35, 50)
        self.dsr2 = DynamicSpike(605, 525, 25, 25, -90)
        self.dsr3 = DynamicSpike(605, 550, 25, 25, -90)
        self.dsp7 = DynamicSpikePlatform(140, 485, 35, 25)
        self.dsr4 = DynamicSpike(160, 485, 25, 25, -90)
        self.dsp8 = DynamicSpikePlatform(825, 485, 35, 25)
        self.dsl4 = DynamicSpike(815, 485, 25, 25, 90)
        self.platform3left = Bridge(150, 455, 75, 25)
        self.cfan_right = ControllableFan(175, 400, 25, 50, (1, 0), 30000, 500)
        self.box = PushableBlock(205, 405, 50, 50)
        self.button1 = Button(180, 560, 50, 25)
        self.small_wall = Bridge(425, 385, 25, 115)
        self.button2 = Button(500, 730, 50, 25)
        self.button3 = Button(400, 400, 25, 50)
        self.platform3right = Bridge(625, 455, 50, 25)
        self.orange_portal = EndPortal(630, 405, 25, 50)
        self.door = Door(1475, 550, 50, 100)

        #Inside the small heart
        self.trapdoor = TrapDoor(450, 450, 75, 25)
        self.trapdoor2 = TrapDoor(450, 520, 75, 25)
        self.finish_level_trigger = FinishLevelTrigger(450, 610, 75, 25)

        self.cfan_right.linked_button = self.button1
        self.trapdoor.linked_button = self.button2
        self.trapdoor2.linked_button = self.button3
        self.blue_portal.linked_portal = self.orange_portal
        self.orange_portal.linked_portal = self.blue_portal

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.blue_portal, self.orange_portal,self.dsl1, self.dsl2, self.dsl3, self.dsl4, self.dsr1, self.dsr2, self.dsr3, self.dsr4, self.dsu1, self.dsu2,self.dsu4, self.dsu5, self.button1, self.button2, self.button3, self.finish_level_trigger, self.water)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground1left, self.trapdoor2, self.ground1right, self.ground2left, self.ground2right, self.ground3left, self.ground3right, self.ground4left, self.ground4right, self.ground5left, self.ground5right, self.ground6left, self.ground6right, self.ground7left, self.ground7right, self.ground8left, self.ground8right, self.ground9left, self.ground9right, self.ground10, self.ground11, self.ground12, self.wall, self.alter_stand, self.platform1left, self.platform1right, self.platform3left, self.platform3right, self.small_wall, self.trapdoor, self.small_ground, self.small_ground1left, self.small_ground1right, self.small_ground2left, self.small_ground2right, self.small_ground3left, self.small_ground3right, self.small_ground4left, self.small_ground4right, self.small_ground5left, self.small_ground5right, self.small_ground6left, self.small_ground6right, self.box, self.dsp1, self.dsp2, self.dsp3, self.dsp4,(self.dsp5),(self.dsp6),(self.dsp7),(self.dsp8),(self.cfan_right),(self.hyde),(self.player))

        self.all_sprites.add(self.water, layer = 0)
        self.all_sprites.add(self.ground, layer = 1)
        self.all_sprites.add(self.ground1left, layer = 1)
        self.all_sprites.add(self.ground1right, layer = 1)
        self.all_sprites.add(self.ground2left, layer = 1)
        self.all_sprites.add(self.ground2right, layer = 1)
        self.all_sprites.add(self.ground3left, layer = 1)
        self.all_sprites.add(self.ground3right, layer = 1)
        self.all_sprites.add(self.ground4left, layer = 1)
        self.all_sprites.add(self.ground4right, layer = 1)
        self.all_sprites.add(self.ground5left, layer = 1)
        self.all_sprites.add(self.ground5right, layer = 1)
        self.all_sprites.add(self.ground6left, layer = 1)
        self.all_sprites.add(self.ground6right, layer = 1)
        self.all_sprites.add(self.ground7left, layer = 1)
        self.all_sprites.add(self.ground7right, layer = 1)
        self.all_sprites.add(self.ground8left, layer = 1)
        self.all_sprites.add(self.ground8right, layer = 1)
        self.all_sprites.add(self.ground9left, layer = 1)
        self.all_sprites.add(self.ground9right, layer = 1)
        self.all_sprites.add(self.ground10, layer = 1)
        self.all_sprites.add(self.ground11, layer = 1)
        self.all_sprites.add(self.ground12, layer = 1)
        self.all_sprites.add(self.wall, layer = 2)
        self.all_sprites.add(self.alter_stand, layer = 2)
        self.all_sprites.add(self.platform1left, layer = 2)
        self.all_sprites.add(self.platform1right, layer = 2)
        self.all_sprites.add(self.dsp1, layer = 3)
        self.all_sprites.add(self.dsu1, layer = 2)
        self.all_sprites.add(self.dsu2, layer = 2)

        self.all_sprites.add(self.dsp2, layer = 3)
        self.all_sprites.add(self.dsu4, layer = 2)
        self.all_sprites.add(self.dsu5, layer = 2)

        self.all_sprites.add(self.dsp3, layer = 3)
        self.all_sprites.add(self.dsr1, layer = 2)
        self.all_sprites.add(self.dsp4, layer = 3)
        self.all_sprites.add(self.dsl1, layer = 2)
        self.all_sprites.add(self.dsp5, layer = 3)
        self.all_sprites.add(self.dsl2, layer = 2)
        self.all_sprites.add(self.dsl3, layer = 2)
        self.all_sprites.add(self.dsl4, layer = 2)
        self.all_sprites.add(self.dsp6, layer = 3)
        self.all_sprites.add(self.dsr2, layer = 2)
        self.all_sprites.add(self.dsr3, layer = 2)
        self.all_sprites.add(self.dsp7, layer = 3)
        self.all_sprites.add(self.dsr4, layer = 2)
        self.all_sprites.add(self.dsp8, layer = 3)
        self.all_sprites.add(self.dsl4, layer = 2)
        self.all_sprites.add(self.platform3left, layer = 2)
        self.all_sprites.add(self.cfan_right, layer = 2)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.button1, layer = 2)
        self.all_sprites.add(self.small_wall, layer = 2)
        self.all_sprites.add(self.button2, layer = 2)
        self.all_sprites.add(self.platform3right, layer = 2)
        self.all_sprites.add(self.orange_portal, layer = 2)
        self.all_sprites.add(self.trapdoor, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 2)
        self.all_sprites.add(self.player, layer = 4)
        self.all_sprites.add(self.hyde, layer = 4)
        self.all_sprites.add(self.small_ground, layer = 1)
        self.all_sprites.add(self.small_ground1left, layer = 1)
        self.all_sprites.add(self.small_ground1right, layer = 1)
        self.all_sprites.add(self.small_ground2left, layer = 1)
        self.all_sprites.add(self.small_ground2right, layer = 1)
        self.all_sprites.add(self.small_ground3left, layer = 1)
        self.all_sprites.add(self.small_ground3right, layer = 1)
        self.all_sprites.add(self.small_ground4left, layer = 1)
        self.all_sprites.add(self.small_ground4right, layer = 1)
        self.all_sprites.add(self.small_ground5left, layer = 1)
        self.all_sprites.add(self.small_ground5right, layer = 1)
        self.all_sprites.add(self.small_ground6left, layer = 1)
        self.all_sprites.add(self.small_ground6right, layer = 1)
        self.all_sprites.add(self.door, layer = 2)
        self.all_sprites.add(self.blue_portal, layer = 2)
        self.all_sprites.add(self.button3, layer = 2)
        self.all_sprites.add(self.trapdoor2, layer = 2)
        



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
        for ds in [self.dsu1, self.dsu2, self.dsu4, self.dsu5, self.dsl1, self.dsl2, self.dsl3, self.dsl4, self.dsr1, self.dsr2, self.dsr3, self.dsr4]:
            dynamic_spike_movement_based_on_timer(ds, dt)

        press_button([self.player, self.hyde], [self.box], [self.button1, self.button2, self.button3])
        link_button_to_trapdoor([self.button2], [self.trapdoor])
        link_button_to_trapdoor([self.button3], [self.trapdoor2])
        open_door_trapdoor([self.door], [self.trapdoor, self.trapdoor2])
        push_the_block(active_player, self.box, dt)
        control_fan_from_button(
            [self.button1],
            [self.cfan_right],
            active_player,
            [self.box],
            dt,
            water_areas=[self.water],
        )

        apply_gravity(active_player, dt)
        move_and_collide(active_player, self.colliders, dt, self.triggers)
        
        frozen_adjustment(self.player, self.colliders)
        frozen_adjustment(self.hyde, self.colliders)

        
        link_portals(self.blue_portal, self.orange_portal)



        crouching_adjustment(active_player, self.colliders)
        buoyant_force(active_player, [self.water])
        squash_adjustment(active_player, self.colliders)

        teleport_player(active_player, self.blue_portal)
        teleport_player(active_player, self.orange_portal)
        teleport_pushable_block(self.box, self.blue_portal)
        teleport_pushable_block(self.box, self.orange_portal)
        cooldown_timer(self.blue_portal, dt)
        cooldown_timer(self.orange_portal, dt)

        block_collisions(self.box, self.colliders, dt, self.triggers)


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



    
