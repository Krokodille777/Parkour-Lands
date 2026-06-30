import pygame


def get_sulfur_area(sulfur):
    direction_x, direction_y = sulfur.direction
    if direction_y < 0:
        return pygame.Rect(sulfur.rect.left, sulfur.rect.top - sulfur.range, sulfur.rect.width, sulfur.range + sulfur.rect.height)
    if direction_y > 0:
        return pygame.Rect(sulfur.rect.left, sulfur.rect.top, sulfur.rect.width, sulfur.range + sulfur.rect.height)
    if direction_x < 0:
        return pygame.Rect(sulfur.rect.left - sulfur.range, sulfur.rect.top, sulfur.range + sulfur.rect.width, sulfur.rect.height)
    if direction_x > 0:
        return pygame.Rect(sulfur.rect.left, sulfur.rect.top, sulfur.range + sulfur.rect.width, sulfur.rect.height)
    return sulfur.rect.copy()


def _apply_airflow(body, sulfur, dt, water_multiplier=1.0, horizontal_only=False):
    if not body.rect.colliderect(get_sulfur_area(sulfur)):
        return

    direction_x, direction_y = sulfur.direction
    force = sulfur.force * dt * water_multiplier
    body.vel.x += direction_x * force
    if not horizontal_only:
        body.vel.y += direction_y * force
    return True


def apply_sulfur_effect(player, sulfur, dt, water_multiplier=1.0):
    return _apply_airflow(player, sulfur, dt, water_multiplier=water_multiplier)

def apply_sulfur_effect_in_water(player, sulfur, dt):
    return _apply_airflow(player, sulfur, dt, water_multiplier=0.5)

def apply_sulfur_effect_to_block(block, sulfur, dt):
    return _apply_airflow(block, sulfur, dt)
