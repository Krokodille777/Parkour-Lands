
import pygame
from pygame.locals import *
from sprites import Player, Ground, FinishLevelTrigger, JumpPad,  DynamicSpike, DynamicSpikePlatform, Spike, Lava, GravityJumpPad, Ice, Fan, Checkpoint, FragileGround, PressTrap, Bridge
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from physics import apply_agt, agt_move_and_collide
from fragile_ground import trigger_fragile_ground, fragile_ground_check, respawn_fragile_ground
from press_trap import apply_press_trap_effect, update_press_trap
from checkpoint import checkpoint_activation
from dynamic_spike import dynamic_spike_movement_based_on_timer
from fans import apply_fan_effect
from maincamera import follow_player

class Level58:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 850, 50, 50)
        self.ground = Ground(0, 1000, 250, 500)
        self.jumpPad = JumpPad(200, 975, 50, 25, -1000)
        self.lava = Lava(250, 1025, 950, 500)
        self.block1 = Ground(370, 950, 50, 200)
        self.spike_down = Spike(370, 900, 50, 50, 0)
        

        self.platform2 = Bridge(420, 950, 75, 15)
        self.jumpPad2 = JumpPad(495, 1000, 100, 25, -2500)
        self.platform3 = Bridge(595, 950, 50, 15)

        self.platform4 = Ground(500, 730,  105, 25)
        self.spike_up = Spike(520, 755, 35,35, 180)
        self.spike_up2 = Spike(555, 755, 35,35, 180)

        self.platform = Ground(250, 825, 120, 50)
        self.dsp = DynamicSpikePlatform(265, 825, 35, 35)
        self.dsd = DynamicSpike(265, 815, 32, 32, 0)

        self.wall = Ground(0, 0, 100, 700)
        self.wallpart = Ground(100, 620, 300, 80)
        self.press_trap3 = PressTrap(250, 587.5, 100, 63, 0)
        self.floor_decor2 = Bridge(100, 620, 150, 40)
        self.wall_decor2 = Bridge(65, 0, 35, 660)
        self.spike_right = Spike(100, 340, 35, 35, -90)
        self.spike_right2 = Spike(100, 375, 35, 35, -90)
        self.spike_right3 = Spike(100, 410, 35, 35, -90)
        self.fan_up = Fan(125, 595, 85, 35, (0, -1), 7000, 400)


        self.fg2 = FragileGround(685, 915, 35, 35)
        self.agtJumppad = GravityJumpPad(775, 895, 50, 25, -5000)

        self.small_wall = Bridge(650, 600, 35, 195)
        self.press_trap1 = PressTrap(685, 600, 85, 60, 90)
        self.press_trap2 = PressTrap(685, 710, 85, 60, 90)
        self.small_wall2 = Bridge(845, 600, 35, 450)

        self.ground2 = Ground(250, 350, 850, 105)
        self.checkpoint = Checkpoint(730, 470, 50, 50)
        self.ice = Ice(580, 435, 270, 35)
        self.small_block = Ground(530, 455, 50, 60)
        self.small_block2 = Ground(490, 455, 50, 60)
        self.lava2 = Lava(410, 455, 80, 35)
        self.small_block3 = Ground(350, 455, 60, 60)

        self.ceiling_decor = Bridge(225, 455, 125, 35)
        self.wall_decor = Bridge(225, 355, 35, 115)
        self.floor_decor = Bridge(225, 365, 850, 35)
        self.spike_down2 = Spike(325, 315, 35, 35, 0)
        self.jumpPad23= JumpPad(400, 325, 35, 25, -700)

        self.platform5 = Ground(460, 255, 80, 60)
        self.spike_right4 = Spike(515, 160, 25, 25, -90)
        self.platform6 = Ground(480, 155, 50, 50)
        self.spike_right5 = Spike(540, 260, 35, 35, -90)


        self.ceiling = Ground(0, 0, 250, 60)
        self.agtJumppad2 = GravityJumpPad(215, 50, 35, 30, 250)
        self.spike_up4 = Spike(250, 0, 50, 50, 180)
        self.spike_up5 = Spike(300, 0, 50, 50, 180)
        self.spike_up6 = Spike(350, 0, 50, 50, 180)
        self.spike_up7 = Spike(400, 0, 50, 50, 180)
        self.spike_up8 = Spike(450, 0, 50, 50, 180)


        self.small_wall3 = Bridge(600, 300, 25, 50)
        self.lava3 = Lava(625, 315, 80, 35)
        self.small_wall4 = Bridge(705, 300, 25, 50)
       
        self.finish_level_trigger = FinishLevelTrigger(750, 250, 50, 100)
        self.wall2 = Ground(850, 0, 500, self.WORLD_HEIGHT)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.lava, self.spike_up, self.spike_up2, self.spike_down2, self.spike_down, self.dsd, self.lava2, self.spike_right2, self.checkpoint, self.spike_right3, self.spike_up4, self.spike_up5, self.spike_up6, self.spike_up7, self.spike_up8, self.press_trap1, self.press_trap2, self.press_trap3, self.spike_right4, self.spike_right5)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.wall2, self.ground2, self.player, self.platform2, self.agtJumppad, self.agtJumppad2, self.fan_up, self.press_trap1, self.press_trap2, self.press_trap3,self.platform, self.block1, self.dsp, self.wall, self.wallpart, self.floor_decor2, self.wall_decor2, self.small_wall, self.small_wall2, self.ceiling, self.platform3, self.platform4, self.platform5, self.platform6, self.fg2, self.ice, self.small_block, self.small_block2, self.small_block3, self.ceiling_decor, self.jumpPad, self.jumpPad2, self.jumpPad23, self.small_wall3, self.small_wall4)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.player, layer = 1)
        self.all_sprites.add(self.platform, layer = 0)
        self.all_sprites.add(self.dsp, layer = 1)
        self.all_sprites.add(self.dsd, layer = 0)
        self.all_sprites.add(self.block1, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.platform2, layer = 0)
        self.all_sprites.add(self.jumpPad, layer = 0)
        self.all_sprites.add(self.platform3, layer = 0)
        self.all_sprites.add(self.platform4, layer = 0)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.wall, layer = 0)
        self.all_sprites.add(self.wallpart, layer = 0)
        self.all_sprites.add(self.press_trap3, layer = 1)
        self.all_sprites.add(self.floor_decor2, layer = 0)
        self.all_sprites.add(self.wall_decor2, layer = 0)
        self.all_sprites.add(self.spike_right, layer = 1)
        self.all_sprites.add(self.spike_right2, layer = 1)
        self.all_sprites.add(self.spike_right3, layer = 1)
        self.all_sprites.add(self.fan_up, layer = 0)
        self.all_sprites.add(self.fg2, layer = 0)
        self.all_sprites.add(self.agtJumppad, layer = 0)
        self.all_sprites.add(self.agtJumppad2, layer = 0)
        self.all_sprites.add(self.small_wall, layer = 1)
        self.all_sprites.add(self.press_trap1, layer = 1)
        self.all_sprites.add(self.press_trap2, layer = 1)
        self.all_sprites.add(self.small_wall2, layer = 1)
        self.all_sprites.add(self.checkpoint, layer = 0)
        self.all_sprites.add(self.ice, layer = 0)
        self.all_sprites.add(self.small_block, layer = 0)
        self.all_sprites.add(self.small_block2, layer = 0)
        self.all_sprites.add(self.lava2, layer = 0)
        self.all_sprites.add(self.small_block3, layer = 0)
        self.all_sprites.add(self.ceiling_decor, layer = 0)
        self.all_sprites.add(self.wall_decor, layer = 0)
        self.all_sprites.add(self.spike_down, layer = 1)
        self.all_sprites.add(self.spike_down2, layer = 1)
        self.all_sprites.add(self.jumpPad2, layer = 0)
        self.all_sprites.add(self.platform5, layer = 0)
        self.all_sprites.add(self.spike_right4, layer = 1)
        self.all_sprites.add(self.platform6, layer = 0)
        self.all_sprites.add(self.spike_right5, layer = 1)
        self.all_sprites.add(self.ceiling, layer = 0)
        self.all_sprites.add(self.agtJumppad2, layer = 0)
        self.all_sprites.add(self.spike_up4, layer = 1)
        self.all_sprites.add(self.spike_up5, layer = 1)
        self.all_sprites.add(self.spike_up6, layer = 1)
        self.all_sprites.add(self.spike_up7, layer = 1)
        self.all_sprites.add(self.spike_up8, layer = 1)
        self.all_sprites.add(self.lava, layer = 0)
        self.all_sprites.add(self.finish_level_trigger, layer = 0)
        self.all_sprites.add(self.wall2, layer = 0)
        self.all_sprites.add(self.small_wall3, layer = 1)
        self.all_sprites.add(self.lava3, layer = 0)
        self.all_sprites.add(self.small_wall4, layer = 1)
        self.all_sprites.add(self.jumpPad23, layer = 0)

        



    def update(self, dt):
        self.player.handle_input(dt)

        dynamic_spike_movement_based_on_timer(self.dsd, dt)
        

        if self.player.gravity_direction == "up":
            apply_agt(self.player, dt)
            agt_move_and_collide(self.player, self.colliders, dt, self.triggers)
        else:
            apply_gravity(self.player, dt)
            move_and_collide(self.player, self.colliders, dt, self.triggers)

        apply_fan_effect(self.player, self.fan_up, dt, water_multiplier=0.5)
        apply_press_trap_effect (self.player, self.press_trap1, dt)
        apply_press_trap_effect (self.player, self.press_trap2, dt)
        apply_press_trap_effect (self.player, self.press_trap3, dt)
        trigger_fragile_ground(self.player, self.block1, [self.fg2])
        fragile_ground_check(self.player, self.block1, [self.fg2],self.colliders, dt)
        respawn_fragile_ground(self.colliders, self.all_sprites, [self.fg2], dt)

        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)


        checkpoint_activation(self.player, [self.checkpoint])
        update_press_trap(self.press_trap1, dt)
        update_press_trap(self.press_trap2, dt)
        update_press_trap(self.press_trap3, dt)




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



    
