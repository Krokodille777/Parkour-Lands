import pygame


GRAVITY = 2000


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
