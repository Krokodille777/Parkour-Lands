import pygame
from pygame.locals import *
from sprites import Player, Void, NetherSky, CaveStone, Lava, Checkpoint, Fire, EmberCrystal, SoulGround, Ground, DarkFloor, NetherWall, Dripstone, FinishLevelTrigger, TipCloud, Bridge, FragileSurface, Glass, PushableBlock, Button, JumpPad, Door, PressTrap, Blood, Ladder, TrapDoor, FragileGround, Blood
from effects import apply_shake_effect, apply_fog_effect
from physics import apply_gravity, move_and_collide, climb_ladder, crouching_adjustment, squash_adjustment, jump_from_the_top_of_ladder
from fragile_surfaces import break_surface, break_glass
from button_door_trap import press_button, link_button_to_door, link_button_to_trapdoor, open_door_trapdoor
from pushableBlock import push_the_block, block_collisions
from fragile_ground import trigger_fragile_ground, fragile_ground_check, respawn_fragile_ground
from blood import slow_down_player
from press_trap import apply_press_trap_effect, update_press_trap
from maincamera import follow_player
from checkpoint import checkpoint_activation


class Level61:
    def __init__(self):
        self.WORLD_WIDTH = 9000
        self.WORLD_HEIGHT = 7000
        self.all_sprites = pygame.sprite.LayeredUpdates()

        #Cave Part
        self.void = Void(0, 0, 800, 750)
        self.cave_wall = CaveStone()


