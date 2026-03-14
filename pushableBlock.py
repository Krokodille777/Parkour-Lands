'''
Pushable blocks are puzzle objects that can be moved by the player and can
interact with the same world elements as the player.
'''
import pygame

from physics import apply_gravity, move_and_collide

HAZARD_TYPES = {"spike", "dynamic_spike", "lava"}


def push_the_block(player, block):
    pushing = False
    if player.rect.colliderect(block.rect):
        if player.vel.x > 0 and player.rect.centerx <= block.rect.centerx:
            block.vel.x = max(block.vel.x, player.vel.x)
            pushing = True
        elif player.vel.x < 0 and player.rect.centerx >= block.rect.centerx:
            block.vel.x = min(block.vel.x, player.vel.x)
            pushing = True

    if not pushing:
        block.handle_input()


def triggers_check(*args):
    if len(args) == 3:
        _, triggers, block = args
    elif len(args) == 2:
        block, triggers = args
    else:
        raise TypeError("triggers_check expects (block, triggers) or (player, triggers, block)")

    for trigger in triggers:
        if getattr(trigger, "type", None) not in HAZARD_TYPES:
            continue

        if hasattr(trigger, "mask"):
            collided = pygame.sprite.collide_mask(block, trigger)
        else:
            collided = block.rect.colliderect(trigger.rect)

        if not collided:
            continue

        block.pos = pygame.math.Vector2(block.spawn_point)
        block.rect.topleft = (round(block.pos.x), round(block.pos.y))
        block.vel = pygame.math.Vector2(0, 0)
        block.on_ground = False
        block.ground = None
        block.delta_x = 0
        block.delta_y = 0
        return True

    return False


def block_collisions(block, colliders, dt, triggers=None):
    prev_x, prev_y = block.rect.x, block.rect.y
    apply_gravity(block, dt)
    move_and_collide(block, colliders, dt, triggers or [])
    block.delta_x = block.rect.x - prev_x
    block.delta_y = block.rect.y - prev_y


def on_ice(block, colliders):
    return block.on_ice


def use_jumppad(block, colliders):
    return getattr(block.ground, "type", None) == "jumppad"
