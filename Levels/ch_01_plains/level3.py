# Level 3 structure is based on the third picture from rrr.png. A long horizontal level with a few platforms and a lava pool in the middle. The player has to jump across the platforms to reach the end of the level. The tip cloud will give a hint about how to jump across the lava pool.
import pygame

from sprites import Player, Ground, TipCloud, FinishLevelTrigger, Lava
from physics import apply_gravity, move_and_collide, crouching_adjustment, squash_adjustment
from maincamera import follow_player


class Level3:

    def __init__(self):
        self.WORLD_WIDTH = 2000
        self.WORLD_HEIGHT = 1500
        self.all_sprites = pygame.sprite.LayeredUpdates()
        
        self.player = Player(60, 250, 50, 50)
        self.ground = Ground(0, 750, 325, 500)
        self.stair1 = Ground(100, 700, 225, 50)
        self.stair2 = Ground(150, 650, 175, 50)
        self.stair3 = Ground(200, 600, 125, 50)
        self.lava_pool = Lava(325, 800, 2000, 500)
        self. platform1 = Ground(345, 625, 100, 50)
        self.platform2 = Ground(655, 625, 100, 50)

        self.tip_cloud = TipCloud(355, 300, 200, 50, "Watch out for the lava!")

        self.finish_flag = FinishLevelTrigger(752, 525, 50, 100)

        self.triggers = pygame.sprite.Group()
        self.triggers.add(self.finish_flag)
        self.colliders = pygame.sprite.Group()
        self.colliders.add(self.ground, self.stair1, self.stair2, self.stair3, self.lava_pool, self.platform1, self.platform2)

        self.all_sprites.add(self.ground, layer = 0)
        self.all_sprites.add(self.stair1, layer = 0)
        self.all_sprites.add(self.stair2, layer = 0)
        self.all_sprites.add(self.stair3, layer = 0)
        self.all_sprites.add(self.lava_pool, layer = 0)
        self.all_sprites.add(self.platform1, layer = 0)
        self.all_sprites.add(self.platform2, layer = 0)
        self.all_sprites.add(self.tip_cloud, layer = 1)
        self.all_sprites.add(self.finish_flag, layer = 1)
        self.all_sprites.add(self.player, layer = 2)

    def update(self, dt):
            apply_gravity(self.player, dt)
            move_and_collide(self.player, self.colliders, dt, self.triggers)
            crouching_adjustment(self.player, self.colliders)
            squash_adjustment(self.player, self.colliders)
            self.player.handle_input()
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
        return self.player.rect.colliderect(self.finish_flag.rect)