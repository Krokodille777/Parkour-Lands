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
        if player.vel.x > 0:       # Moving right -> hit left side of wall
            player.rect.right = c.rect.left
        elif player.vel.x < 0:     # Moving left -> hit right side of wall
            player.rect.left = c.rect.right
        player.pos.x = player.rect.x
        player.vel.x = 0

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
            player.pos.y = player.rect.y
            player.vel.y = 0
            player.on_ground = True
        elif player.vel.y < 0:     # Jumping -> hit ceiling
            player.rect.top = c.rect.bottom
            player.pos.y = player.rect.y
            player.vel.y = 0