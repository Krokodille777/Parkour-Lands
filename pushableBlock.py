'''
Pushable Block is much more interesting object than any logic object. It has almost all possibilities of player, like using jump pads, pressing butons, using portals, and so on. 
And the best thing is, it is not a static object. It can be pushed by the player and be used to solve some mini puzzles. It can be used to hold down buttons, to reach higher places, to block traps, and so on. It is a very versatile object that can be used in many different ways.
When pushable block touches spikes, dynamic spikes or lava, it willl be destroyed, but don't worry, it will respawn after 3 seconds like a fragile ground object.
'''
from sprites import Player, PushableBlock
import pygame


def push_the_block(player,  block, ):

    if player.rect.colliderect(block.rect):
        if player.vel.x > 0:  # Moving right
            block.vel.x = player.vel.x
        elif player.vel.x < 0:  # Moving left
            block.vel.x = player.vel.x


def triggers_check(player, triggers, block):
    for trigger in triggers:
        if getattr(trigger, "type", None) == "spike" or getattr(trigger, "type", None) == "dynamic_spike" or getattr(trigger, "type", None) == "lava":
            continue
        if not pygame.sprite.collide_mask(player, trigger):
            continue
        block.pos = pygame.math.Vector2(block.spawn_point)
        block.rect.topleft = (round(block.pos.x), round(block.pos.y))
        block.vel = pygame.math.Vector2(0, 0)
        return
    

def block_collisions(block, colliders, dt):
    for c in colliders:
        if c is block:
            continue
        if not block.rect.colliderect(c.rect):
            continue
        if block.vel.x > 0:       # Moving right -> hit wall on the right
            block.rect.right = c.rect.left
        elif block.vel.x < 0:     # Moving left -> hit wall on the left
            block.rect.left = c.rect.right
        else:                       # Not moving horizontally but overlapping (e.g. resize)
            if block.rect.right - c.rect.left < c.rect.right - block.rect.left:
                block.rect.left = c.rect.right
            else:
                block.rect.right = c.rect.left
        block.pos.x = float(block.rect.x)

def on_ice(block, colliders):
    block.on_ice = False
    for c in colliders:
        if c is block:
            continue
        if not block.rect.colliderect(c.rect):
            continue
        if getattr(c, "type", None) == "ice":
            block.on_ice = True


def use_jumppad(block, colliders):
    for c in colliders:
        if c is block:
            continue
        if not block.rect.colliderect(c.rect):
            continue
        if getattr(c, "type", None) == "jumppad":
            block.vel.y = c.launch_vel
            block.on_ground = False
            block.ground = None