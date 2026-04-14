
import pygame
from pygame.locals import *
from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Spike, Lava, GravityJumpPad
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from physics import apply_agt, agt_move_and_collide
from maincamera import follow_player

class Level53:
    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.bg_color = (119, 164, 237)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player = Player(60, 700, 50, 50)
        self.ground = Ground(0, 750, 350, 500)
        self.lava = Lava(350, 760, 650, 490)
        self.agtJumppad = GravityJumpPad(315, 725, 35, 25, -1800)


        self.platform2 = Ground(300, 500, 250, 50)
        self.spike_up = Spike(400, 550, 25, 25, 180)
        self.spike_up2 = Spike(425, 550, 25, 25, 180)

        self.tip_cloud = TipCloud(330, 450, 100, 100, "Flip the gravity with ease \n by using this special kind of \n **jump pad**!")

    
        self.ground2 = Ground(550, 150, 150, 50)
        self.agtJumppad2 = GravityJumpPad(665, 200, 35, 25, 1800)

        self.platform = Ground(655, 450, 120, 50)

       
        self.finish_level_trigger = FinishLevelTrigger(725, 350, 50, 100)


        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_level_trigger, self.lava, self.spike_up, self.spike_up2)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.ground2, self.player,  self.platform2, self.agtJumppad, self.agtJumppad2, self.platform)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.ground2, layer = 0)
        self.all_sprites.add(self.player, layer = 2)
        self.all_sprites.add(self.finish_level_trigger, layer = 1)
        self.all_sprites.add(self.lava, layer = 0)
        self.all_sprites.add(self.platform2, layer = 1)
        self.all_sprites.add(self.spike_up, layer = 1)
        self.all_sprites.add(self.spike_up2, layer = 1)
        self.all_sprites.add(self.agtJumppad, layer = 1)
        self.all_sprites.add(self.agtJumppad2, layer = 1)
        self.all_sprites.add(self.platform, layer = 1)
        self.all_sprites.add(self.tip_cloud, layer = 3)



    def update(self, dt):
        self.player.handle_input(dt)

        if self.player.gravity_direction == "up":
            apply_agt(self.player, dt)
            agt_move_and_collide(self.player, self.colliders, dt, self.triggers)
        else:
            apply_gravity(self.player, dt)
            move_and_collide(self.player, self.colliders, dt, self.triggers)

        crouching_adjustment(self.player, self.colliders)
        squash_adjustment(self.player, self.colliders)
        




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



    
