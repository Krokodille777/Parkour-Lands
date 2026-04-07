'''
Pushable blocks are puzzle objects that can be moved by the player and can
interact with the same world elements as the player.
'''
import pygame

from physics import apply_gravity, move_and_collide, _carry_with_block
HAZARD_TYPES = {"spike", "dynamic_spike", "lava", "press_trap"}
MOVING_PLATFORM_TYPES = {"elevator_up_down", "elevator_left_right"}
PUSH_TOLERANCE = 4
HEAD_SUPPORT_TOLERANCE = 3
MIN_HEAD_OVERLAP = 10


def _vertical_overlap(rect_a, rect_b):
    return rect_a.bottom > rect_b.top + 4 and rect_a.top < rect_b.bottom - 4


def _horizontal_overlap(rect_a, rect_b):
    return max(0, min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left))


def _is_resting_on_head(player, block):
    if getattr(player, "gravity_direction", "down") != "down":
        return False

    touching_head = abs(block.rect.bottom - player.rect.top) <= HEAD_SUPPORT_TOLERANCE
    overlap = _horizontal_overlap(player.rect, block.rect)
    return touching_head and overlap >= MIN_HEAD_OVERLAP


def push_the_block(player, block, dt):
    pushing = False
    player_next_rect = player.rect.move(round(player.vel.x * dt), 0)

    if block.on_ground and block.ground is player and _is_resting_on_head(player, block):
        block.vel.x = player.vel.x
        return

    if _vertical_overlap(player.rect, block.rect):
        moving_into_left_side = (
            player.vel.x > 0
            and player.rect.right <= block.rect.left + PUSH_TOLERANCE
            and player_next_rect.right >= block.rect.left
        )
        moving_into_right_side = (
            player.vel.x < 0
            and player.rect.left >= block.rect.right - PUSH_TOLERANCE
            and player_next_rect.left <= block.rect.right
        )

        if moving_into_left_side or (player.rect.colliderect(block.rect) and player.vel.x > 0 and player.rect.centerx <= block.rect.centerx):
            block.vel.x = max(block.vel.x, player.vel.x)
            pushing = True
        elif moving_into_right_side or (player.rect.colliderect(block.rect) and player.vel.x < 0 and player.rect.centerx >= block.rect.centerx):
            block.vel.x = min(block.vel.x, player.vel.x)
            pushing = True

    if not pushing:
        block.handle_input(dt)


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

def on_moving_platform(block, colliders):
    return getattr(block.ground, "type", None) in MOVING_PLATFORM_TYPES

def use_jumppad(block, colliders):
    return getattr(block.ground, "type", None) == "jumppad"

def respawn_block(block, colliders, triggers, dt):
    if block.vel.x == 0 and block.vel.y == 0:
        return

    if triggers_check(block, triggers):
        return

    block_collisions(block, colliders, dt, triggers)
