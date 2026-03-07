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


def apply_fan_effect(player, fan, dt):
    if not player.rect.colliderect(get_fan_area(fan)):
        return

    direction_x, direction_y = fan.direction
    player.vel.x += direction_x * fan.force * dt
    player.vel.y += direction_y * fan.force * dt

    
