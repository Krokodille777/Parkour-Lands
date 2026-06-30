import math
import pygame
from pygame.locals import *
from sprites import Player


def _as_list(items):
    if items is None:
        return []
    if hasattr(items, "rect"):
        return [items]
    return [item for item in items if hasattr(item, "rect")]


def update_vine(vine, dt, actors=None):
    touching_actor = any(actor.rect.colliderect(vine.rect) for actor in _as_list(actors))
    if touching_actor:
        vine.active = True

    previous_x = vine.rect.x
    previous_y = vine.rect.y
    vine.delta_x = 0
    vine.delta_y = 0

    if vine.active:
        vine.phase += dt * vine.frequency * 2 * math.pi
        vine.rect.x = round(vine.original_x + math.sin(vine.phase) * vine.amplitude)
        vine.rect.y = vine.original_y
        vine.delta_x = vine.rect.x - previous_x
        vine.delta_y = vine.rect.y - previous_y


def climb_vine(player, vines):
    keys = pygame.key.get_pressed()
    for vine in _as_list(vines):
        if not player.rect.colliderect(vine.rect):
            continue

        vine.active = True
        player.vel.y = 0
        player.vel.x += getattr(vine, "delta_x", 0) * 12

        if keys[K_UP] or keys[K_w]:
            player.vel.y = -Player.SPEED
        elif keys[K_DOWN] or keys[K_s]:
            player.vel.y = Player.SPEED

        if keys[K_SPACE]:
            player.vel.y = Player.JUMP_VEL
            player.vel.x += 250 if player.rect.centerx >= vine.rect.centerx else -250
            player.on_ground = False
        return True

    return False
