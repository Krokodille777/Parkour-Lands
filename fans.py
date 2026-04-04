'''
Вентилятор создаёт прямоугольную зону потока перед собой и ускоряет игрока,
если тот находится внутри этой зоны.
'''

import pygame


def get_fan_area(fan):
    direction_x, direction_y = fan.direction
    if direction_y < 0:  # Up
        return pygame.Rect(fan.rect.left, fan.rect.top - fan.range, fan.rect.width, fan.range + fan.rect.height)
    if direction_y > 0:  # Down
        return pygame.Rect(fan.rect.left, fan.rect.top, fan.rect.width, fan.range + fan.rect.height)
    if direction_x < 0:  # Left
        return pygame.Rect(fan.rect.left - fan.range, fan.rect.top, fan.range + fan.rect.width, fan.rect.height)
    if direction_x > 0:  # Right
        return pygame.Rect(fan.rect.left, fan.rect.top, fan.range + fan.rect.width, fan.rect.height)
    return fan.rect.copy()


def _apply_airflow(body, fan, dt, water_multiplier=1.0, horizontal_only=False):
    if not body.rect.colliderect(get_fan_area(fan)):
        return

    direction_x, direction_y = fan.direction
    force = fan.force * dt * water_multiplier
    body.vel.x += direction_x * force
    if not horizontal_only:
        body.vel.y += direction_y * force


def apply_fan_effect(player, fan, dt, water_multiplier=1.0):
    _apply_airflow(player, fan, dt, water_multiplier=water_multiplier)

def apply_fan_effect_in_water(player, fan, dt):
    _apply_airflow(player, fan, dt, water_multiplier=0.5)

def apply_fan_effect_left_right(player, fan, dt):
    _apply_airflow(player, fan, dt, horizontal_only=True)

def apply_fan_effect_to_block(block, fan, dt):
    _apply_airflow(block, fan, dt)
