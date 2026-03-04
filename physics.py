import pygame
from pygame.locals import *
from sprites import Player


GRAVITY = 1500


def apply_gravity(player, dt: float):
    player.vel.y += GRAVITY * dt


def move_and_collide(player, colliders, dt: float, triggers):
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

    # Check spike triggers after horizontal movement
    for t in triggers:
        if getattr(t, "type", None) != "spike":
            continue
        if not pygame.sprite.collide_mask(player, t):
            continue
        player.pos = pygame.math.Vector2(player.spawn_point)
        player.rect.topleft = (round(player.pos.x), round(player.pos.y))
        player.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        return


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
                player.pos = pygame.math.Vector2(player.spawn_point)
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
    for t in triggers:
        if getattr(t, "type", None) != "spike":
            continue
        if not pygame.sprite.collide_mask(player, t):
            continue
        player.pos = pygame.math.Vector2(player.spawn_point)
        player.rect.topleft = (round(player.pos.x), round(player.pos.y))
        player.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        return
    


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




def buoyant_force(player, water_group):
    in_water = False
    for water in water_group:
        if player.rect.colliderect(water.rect):
            in_water = True
            # Simple buoyancy: if player is in water, reduce gravity effect and allow upward movement
            apply_gravity(player, 1/60)  # Apply gravity as usual
            player.vel.y *= 0.5  # Reduce downward velocity to simulate buoyancy
            player.vel.x *= 0.8  # Optional: reduce horizontal speed in water for more resistance
            keys = pygame.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                player.vel.y -= Player.SPEED * 0.5  # Allow upward movement in water
            break
    return in_water


def apply_speed_zones(player, triggers):
    for t in triggers:
        if getattr(t, "type", None) not in ("accelerator", "decelerator"):
            continue
        if player.rect.colliderect(t.rect):
            if t.type == "accelerator":
                player.vel.x *= 1.8
            elif t.type == "decelerator":
                player.vel.x *= 0.4




