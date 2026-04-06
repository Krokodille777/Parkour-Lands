# Level 1 of Chapter 1 - Plains : Basic Movement
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, Water, Ladder, JumpPad, Spike, FragileGround, DynamicSpike, DynamicSpikePlatform, PressTrap, Ice, Bridge
from physics import apply_gravity, move_and_collide, climb_ladder, jump_from_the_top_of_ladder, crouching_adjustment, squash_adjustment, buoyant_force
from fragile_ground import respawn_fragile_ground, trigger_fragile_ground, fragile_ground_check
from dynamic_spike import dynamic_spike_movement_based_on_timer
from press_trap import apply_press_trap_effect, update_press_trap


from maincamera import follow_player

class Level40:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(750, 30, 50, 50)

        self.ground = Ground(780, 80, 50, 25)
        self.wall = Ground(820, 0, 125, 1000.)
        self.water_pool = Water(625, 110, 195, 490)
        self.wall2 = Ground(575, 60, 50, 355)
        self.spike_down = Spike(575, 0, 50, 60, 0)
        self.floor = Ground(260, 600, 685, 150)
        self.block = Ground(575, 550, 50, 50)

        self.spike_down2 = Spike(550, 575, 25, 25, 0)
        self.spike_down3 = Spike(525, 575, 25, 25, 0)
        self.spike_down4 = Spike(500, 575, 25, 25, 0)
        self.spike_down5 = Spike(475, 575, 25, 25, 0)
        self.spike_down6 = Spike(450, 575, 25, 25, 0)
        self.spike_down7 = Spike(425, 575, 25, 25, 0)
        self.spike_down8 = Spike(400, 575, 25, 25, 0)
        self.spike_down9 = Spike(375, 575, 25, 25, 0)
        self.fg1 = FragileGround(390, 495, 40, 35)
        self.fg2 = FragileGround(500, 495, 40, 35)
        self.ceiling = Ground(375, 355, 200, 50)
        self.wall3 = Ground(350, 280, 25, 140)
        self.block2 = Ground(325, 575, 50, 50)


        self.ladder = Ladder(270, 440, 50, 125)
        self.ground2 = Ground(0, 475, 270, 400)
        self.ice = Ice(10, 440, 260, 35)
        self.wall4 = Ground(0, 0, 50, 475)
        self.press_trap = PressTrap(155, 285, 85, 35, 180)
        self.jumpPad = JumpPad(50, 425, 50, 25, -1350)

        self.block3 = Ground(0, 0, 400, 25)
        self.dsp = DynamicSpikePlatform(50, 0, 50, 65)
        self.dsu1 = DynamicSpike(50, 50, 25, 25, 180)
        self.dsu2 = DynamicSpike(75, 50, 25, 25, 180)

        self.platform = Ground(165, 200, 65, 85)
        self.bridge = Bridge(300, 125, 65, 15)
        self.spike_up = Spike(390, 0, 50, 50, 180)

        self.wall5 = Ground(490, 0, 50, 150)
        self.floor2 = Ground(450, 150, 90, 50)

        self.spike_down10 = Spike(350, 255, 25, 25, 0)

        self.finish_level_trigger = FinishLevelTrigger(500, 245, 50, 100)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.press_trap, self.water_pool, self.dsu1, self.dsu2, self.spike_down, self.spike_down2, self.spike_down3, self.spike_down4, self.ladder,self.spike_down5, self.spike_down6, self.spike_down7, self.spike_down8, self.spike_down9, self.spike_down10, self.spike_up)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.wall, self.wall2, self.floor, self.block, self.fg1, self.fg2, self.ceiling, self.wall3, self.block2,  self.ground2, self.ice, self.wall4, self.jumpPad, self.block3, self.dsp, self.platform,  self.bridge, self.spike_up, self.wall5, self.floor2)

        self.all_sprites.add(self.player, layer = 3)
        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.wall, layer = 0)

        self.all_sprites.add(self.water_pool, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 0)
        self.all_sprites.add(self.floor, layer = 0)
        self.all_sprites.add(self.block, layer = 0)
        self.all_sprites.add(self.spike_down2, layer = 0)
        self.all_sprites.add(self.spike_down3, layer = 0)
        self.all_sprites.add(self.spike_down4, layer = 0)
        self.all_sprites.add(self.spike_down5, layer = 0)
        self.all_sprites.add(self.spike_down6, layer = 0)
        self.all_sprites.add(self.spike_down7, layer = 0)
        self.all_sprites.add(self.spike_down8, layer = 0)
        self.all_sprites.add(self.spike_down9, layer = 0)
        self.all_sprites.add(self.fg1, layer = 0)
        self.all_sprites.add(self.fg2, layer = 0)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.wall3, layer = 0)
        self.all_sprites.add(self.block2, layer = 0)
        self.all_sprites.add(self.ladder, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.ice, layer = 0)
        self.all_sprites.add(self.wall4, layer = 0)
        self.all_sprites.add(self.press_trap, layer = 1)
        self.all_sprites.add(self.jumpPad, layer = 1)
        self.all_sprites.add(self.block3, layer = 0)
        self.all_sprites.add(self.dsp, layer = 2)
        self.all_sprites.add(self.dsu1, layer = 1)
        self.all_sprites.add(self.dsu2, layer = 1)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.bridge, layer = 0)
        self.all_sprites.add(self.spike_up, layer = 0)
        self.all_sprites.add(self.wall5, layer = 0)
        self.all_sprites.add(self.floor2, layer = 0)
        self.all_sprites.add(self.spike_down10, layer = 0)
        self.all_sprites.add(self.finish_level_trigger, layer = 0)


    def update(self, dt):    
        for ds in [self.dsu1, self.dsu2]:
            dynamic_spike_movement_based_on_timer(ds, dt)
        trigger_fragile_ground(self.player, self.block, [self.fg1, self.fg2])
        fragile_ground_check(self.player, self.block, [self.fg1, self.fg2], self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites,[self.fg1, self.fg2], dt)    
        buoyant_force(self.player, [self.water_pool])
        apply_gravity(self.player, dt)
      
        update_press_trap(self.press_trap, dt)

        for trap in [self.press_trap]:
            apply_press_trap_effect(self.player, trap, dt)
        self.player.handle_input()
        move_and_collide(self.player, self.colliders, dt, self.triggers)
        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        climb_ladder(self.player, [self.ladder])
        jump_from_the_top_of_ladder(self.player, [self.ladder])
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



    