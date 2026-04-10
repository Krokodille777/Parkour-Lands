
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, PushableBlock, JumpPad, DynamicSpikePlatform, DynamicSpike, Bridge, FragileGround, Lava, Button, TrapDoor, Door, StartPortal, EndPortal
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from pushableBlock import push_the_block, block_collisions
from button_door_trap import press_button, link_button_to_trapdoor, open_door_trapdoor
from fragile_ground import fragile_ground_check, respawn_fragile_ground, trigger_fragile_ground
from dynamic_spike import dynamic_spike_movement_based_on_timer
from portals import teleport_player, cooldown_timer, link_portals
from maincamera import follow_player

class Level47:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(0, 625, 50, 50)
        self.ground = Ground(0, 800, 350, 500)
        self.platform  = Bridge(0, 750, 30, 25)
        self.platform2 = Bridge(0, 675, 40, 25)
        self.ledge = Ground(150, 750, 75, 25)
        self.blue_portal = StartPortal(170, 650, 50, 100)
        self.ground2 = Ground(0, 0, 275, 625)
        self.wall = Ground(225, 625, 50, 150)

        self.ground3 = Ground(350, 750, 650, 500 )
        self.wall2 = Ground(600, 0, 400, 750)
        self.jump_pad = JumpPad(550, 725, 50, 25, -1000)

        self.platform3 = Bridge(275, 600, 30 ,25)
        self.fg = FragileGround(325, 575, 40, 40)
        self.platform4 = Bridge(415, 565, 95, 25)
        self.button = Button(445, 540, 65, 25)
        self.box = PushableBlock(445, 485, 65, 65)

        self.dynamic_platform = DynamicSpikePlatform(550, 275, 50, 35)
        self.dsu = DynamicSpike(550, 295, 25, 25, 180)
        self.dsu2 = DynamicSpike(575, 295, 25, 25, 180)


        self.floor = Ground(275, 350, 200, 50)
        self.lava = Lava(275, 325, 200, 25)

        self.trapdoor = TrapDoor(275, 300, 200, 25)

        self.trapdoor.linked_button = self.button
        

        self.orange_portal = EndPortal(335, 100, 50, 100)
        self.blue_portal.linked_portal = self.orange_portal
        self.orange_portal.linked_portal = self.blue_portal
        self.ground4 = Ground(475, 275, 150, 25)
        self.finish_level_trigger = FinishLevelTrigger(525, 175, 50, 100)

        self.door = Door(1775, 300, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.button, self.dsu, self.dsu2, self.orange_portal, self.blue_portal)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.box, self.platform, self.platform2, self.ledge, self.wall, self.ground3, self.wall2, self.jump_pad, self.platform3, self.fg, self.platform4, self.dynamic_platform, self.dsu, self.dsu2, self.floor, self.lava, self.trapdoor, self.ground4, self.door)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.box, layer = 2)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.lava, layer = 0)
        self.all_sprites.add(self.trapdoor, layer = 0)
        self.all_sprites.add(self.platform, layer = 1)
        self.all_sprites.add(self.platform2, layer = 1)
        self.all_sprites.add(self.ledge, layer = 1)
        self.all_sprites.add(self.blue_portal, layer = 1)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.ground3, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.jump_pad, layer = 1)
        self.all_sprites.add(self.platform3, layer = 1)
        self.all_sprites.add(self.fg, layer = 1)
        self.all_sprites.add(self.platform4, layer = 1)
        self.all_sprites.add(self.button, layer = 1)
        self.all_sprites.add(self.floor, layer = 2)
        self.all_sprites.add(self.button, layer = 1)
        self.all_sprites.add(self.dynamic_platform, layer = 2)
        self.all_sprites.add(self.dsu, layer = 1)
        self.all_sprites.add(self.dsu2, layer = 1)
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.orange_portal, layer = 1)
        self.all_sprites.add(self.trapdoor, layer = 0)
        self.all_sprites.add(self.door, layer = 0)

    def update(self, dt):
        self.player.handle_input()
        self.box.handle_input(dt)
        dynamic_spike_movement_based_on_timer(self.dsu,  dt)
        dynamic_spike_movement_based_on_timer(self.dsu2, dt)
        trigger_fragile_ground(self.player, self.box, [self.fg])
        fragile_ground_check(self.player, self.box, [self.fg] ,self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites, [self.fg], dt)
        link_portals(self.blue_portal, self.orange_portal)
        
        
        
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)

        teleport_player(self.player, self.blue_portal)
        teleport_player(self.player, self.orange_portal)
        cooldown_timer(self.blue_portal, dt)
        cooldown_timer(self.orange_portal, dt)

        press_button([self.player], self.colliders, [self.button])
        link_button_to_trapdoor([self.button], [self.trapdoor])
        open_door_trapdoor([self.door], [self.trapdoor])

        push_the_block(self.player, self.box,  dt)
        block_collisions(self.box, self.colliders, dt, self.triggers)

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



    