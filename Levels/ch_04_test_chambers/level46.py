
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Spike, StartPortal, EndPortal, Checkpoint
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from portals import teleport_player, link_portals, cooldown_timer
from checkpoint import checkpoint_activation
from maincamera import follow_player

class Level46:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(0, 700, 50, 50)
        self.blue_portal = StartPortal(100, 650, 50, 100)
        self.orange_portal = EndPortal(100, 350, 50, 100)
        self.checkpoint = Checkpoint(200, 400, 50, 50)
        self.spike_down = Spike(300, 425, 25, 25, 0)
        self.spike_up = Spike(500, 345, 25, 25, 180)
        
        self.blue_portal.linked_portal = self.orange_portal
        self.orange_portal.linked_portal = self.blue_portal
        self.blue_portal2 = StartPortal(575, 350, 50, 100)
        self.orange_portal2 = EndPortal(575, 650, 50, 100)
        self.orange_portal2.linked_portal = self.blue_portal2
        self.blue_portal2.linked_portal = self.orange_portal2

        self.ground = Ground(0, 750, 1000, 500)
        self.ground2 = Ground(155, 645, 420, 105)
        self.ground3 = Ground(0, 450, 1000, 195)
        self.ground4 = Ground(0, 345, 95, 105)
        self.ground5 = Ground(580, 345, 500, 105)
        self.ground6 = Ground(0, 0, 1000, 345)
        self.tip_cloud = TipCloud(65, 0, 175, 120, "Teleport yourself or the box \n easily with portals!")
        self.finish_level_trigger = FinishLevelTrigger(900, 650, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.blue_portal, self.orange_portal, self.blue_portal2, self.orange_portal2, self.spike_down, self.spike_up)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.ground3, self.ground4, self.ground5, self.ground6)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.blue_portal, layer = 1)
        self.all_sprites.add(self.orange_portal, layer = 1)
        self.all_sprites.add(self.blue_portal2, layer = 1)
        self.all_sprites.add(self.orange_portal2, layer = 1)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.ground3, layer = 0)   
        self.all_sprites.add(self.ground4, layer = 0)
        self.all_sprites.add(self.ground5, layer = 0)
        self.all_sprites.add(self.ground6, layer = 0)
        self.all_sprites.add(self.checkpoint, layer = 1)
        
        

    def update(self, dt):
        self.player.handle_input()
        link_portals(self.blue_portal, self.orange_portal)
        link_portals(self.blue_portal2, self.orange_portal2)
        
        
        
        apply_gravity(self.player, dt)
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)

        teleport_player(self.player, self.blue_portal)
        teleport_player(self.player, self.orange_portal)
        teleport_player(self.player, self.blue_portal2)
        teleport_player(self.player, self.orange_portal2)
        cooldown_timer(self.blue_portal, dt)
        cooldown_timer(self.orange_portal, dt)
        cooldown_timer(self.blue_portal2, dt)
        cooldown_timer(self.orange_portal2, dt)

        checkpoint_activation(self.player, [self.checkpoint])
        
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



    