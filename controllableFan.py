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


def apply_fan_effect_to_block(block, fan, dt, water_multiplier=1.0):
    _apply_airflow(block, fan, dt, water_multiplier=water_multiplier)


def _iter_bodies(bodies):
    if bodies is None:
        return []
    if hasattr(bodies, "rect"):
        return [bodies]
    return [body for body in bodies if hasattr(body, "rect")]


def _is_in_water(body, water_areas):
    if body is None:
        return False
    return any(body.rect.colliderect(getattr(water, "rect", water)) for water in _iter_bodies(water_areas))


def control_fan_from_button(buttons, fans, player=None, blocks=None, dt=0.0, water_areas=None):
    blocks = _iter_bodies(blocks)
    for fan in fans:
        linked_button = getattr(fan, "linked_button", None)
        linked_from_button = any(fan in getattr(button, "linked_objects", []) and button.pressed for button in buttons)
        if not ((linked_button and linked_button.pressed) or linked_from_button or getattr(fan, "active", False)):
            continue

        if player is not None:
            player_multiplier = 0.5 if _is_in_water(player, water_areas) else 1.0
            if fan.direction[1] == 0:
                _apply_airflow(player, fan, dt, water_multiplier=player_multiplier, horizontal_only=True)
            else:
                _apply_airflow(player, fan, dt, water_multiplier=player_multiplier)

        for block in blocks:
            block_multiplier = 0.5 if _is_in_water(block, water_areas) else 1.0
            _apply_airflow(block, fan, dt, water_multiplier=block_multiplier)
