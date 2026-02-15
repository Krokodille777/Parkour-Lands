import pygame
from pygame.locals import *
from sprites import Player


GRAVITY = 1200


def apply_gravity(player, dt: float):
    player.vel.y += GRAVITY * dt


def move_and_collide(player, colliders, dt: float):
    player.on_ground = False

    # --- Horizontal pass ---
    player.pos.x += player.vel.x * dt
    player.rect.x = round(player.pos.x)

    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        if player.vel.x > 0:       # Moving right -> hit wall on the right
            player.rect.right = c.rect.left
        elif player.vel.x < 0:     # Moving left -> hit wall on the left
            player.rect.left = c.rect.right
        else:                       # Not moving horizontally but overlapping (e.g. resize)
            push_right = c.rect.right - player.rect.left
            push_left  = player.rect.right - c.rect.left
            if push_right < push_left:
                player.rect.left = c.rect.right
            else:
                player.rect.right = c.rect.left
        player.pos.x = float(player.rect.x)

    # --- Vertical pass ---
    player.pos.y += player.vel.y * dt
    player.rect.y = round(player.pos.y)

    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        if player.vel.y > 0:       # Falling -> land on top
            player.rect.bottom = c.rect.top
            player.vel.y = 0
            player.on_ground = True
            if getattr(c, "type", None) == "jumppad":
                player.vel.y = c.launch_vel
                player.on_ground = False
            if getattr(c, "type", None) == "lava":
                player.pos = pygame.math.Vector2(60, 625)
                player.rect.topleft = (round(player.pos.x), round(player.pos.y))
                player.vel = pygame.math.Vector2(0, 0)
                player.on_ground = False
                return
            if getattr(c, "type", None) == "spike":
                player.pos = pygame.math.Vector2(60, 625)
                player.rect.topleft = (round(player.pos.x), round(player.pos.y))
                player.vel = pygame.math.Vector2(0, 0)
                player.on_ground = False
                return
        elif player.vel.y < 0:     # Jumping -> hit ceiling
            player.rect.top = c.rect.bottom
            player.vel.y = 0
        else:                       # Not moving vertically but overlapping (e.g. resize)
            push_down = c.rect.bottom - player.rect.top
            push_up   = player.rect.bottom - c.rect.top
            if push_up <= push_down:
                player.rect.bottom = c.rect.top
                player.on_ground = True
            else:
                player.rect.top = c.rect.bottom
        player.pos.y = float(player.rect.y)

    # Crouching adjustment: if player is crouching and there's a ceiling right above, keep them crouched
def crouching_adjustment(player, colliders):
    if not player.crouching:
        return

    # Check for ceiling right above the player's head
    player.rect.y = round(player.pos.y)  # Ensure rect is in sync with pos
    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        if player.vel.y <= 0 and player.rect.top < c.rect.bottom and player.rect.bottom > c.rect.top:
            # There's a ceiling right above, keep crouching
            return

    # No ceiling detected, can stand up
    player.crouching = False


def follow_player(player, screen_width, world_width, screen_height, world_height):
    # Center the player on the screen, but clamp to world bounds
    offset_x = screen_width // 2 - round(player.pos.x) - player.rect.width // 2
    offset_x = max(min(offset_x, 0), screen_width - world_width)
    offset_x = int(offset_x)  # Ensure it's an integer for blitting

    offset_y = screen_height // 2 - round(player.pos.y) - player.rect.height // 2
    offset_y = max(min(offset_y, 0), screen_height - world_height)
    
    return offset_x, offset_y   

#Gravity should affect only if you fall off the ladder, not while climbing. So we apply gravity in the main loop as usual, but if the player is on a ladder and pressing up/down, we override the vertical velocity and skip gravity for that frame.
def climb_ladder(player, ladder_group):
    on_ladder = False
    for ladder in ladder_group:
        if player.rect.colliderect(ladder.rect):
            on_ladder = True
            keys = pygame.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                player.vel.y = -Player.SPEED
            elif keys[K_DOWN] or keys[K_s]:
                player.vel.y = Player.SPEED
            else:
                player.vel.y = 0  # Stay still on the ladder if no vertical input
            break
    # If not on a ladder or no vertical input, apply gravity as usual
    if not on_ladder:
        apply_gravity(player, 1/60)  # Assuming 60 FPS for consistent gravity application

def jump_from_the_top_of_ladder(player, ladder_group):
    for ladder in ladder_group:
        if player.rect.colliderect(ladder.rect):
            keys = pygame.key.get_pressed()
            if (keys[K_SPACE] or keys[K_UP] or keys[K_w]) and player.on_ground:
                player.vel.y = Player.JUMP_VEL
                player.on_ground = False