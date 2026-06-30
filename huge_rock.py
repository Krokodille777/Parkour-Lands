import pygame
from physics import respawn_actor


def _as_list(items):
    if items is None:
        return []
    if hasattr(items, "rect"):
        return [items]
    return [item for item in items if hasattr(item, "rect")]


def _move_axis(rock, colliders, amount, axis):
    if amount == 0:
        return

    if axis == "x":
        rock.pos.x += amount
        rock.rect.x = round(rock.pos.x)
    else:
        rock.pos.y += amount
        rock.rect.y = round(rock.pos.y)

    for collider in _as_list(colliders):
        if collider is rock or not rock.rect.colliderect(collider.rect):
            continue

        if getattr(collider, "type", None) in ("fragile_surface", "glass"):
            collider.kill()
            continue

        if axis == "x":
            if amount > 0:
                rock.rect.right = collider.rect.left
            else:
                rock.rect.left = collider.rect.right
            rock.pos.x = float(rock.rect.x)
            rock.vel.x = 0
        else:
            if amount > 0:
                rock.rect.bottom = collider.rect.top
            else:
                rock.rect.top = collider.rect.bottom
            rock.pos.y = float(rock.rect.y)
            rock.vel.y = 0


def update_huge_rock(rock, dt, colliders=None, player=None, blocks=None, fragile_surfaces=None):
    if not rock.active:
        return False

    previous_x = rock.rect.x
    previous_y = rock.rect.y

    target_speed = rock.roll_direction * rock.max_speed
    if rock.vel.x < target_speed:
        rock.vel.x = min(target_speed, rock.vel.x + rock.acceleration * dt)
    elif rock.vel.x > target_speed:
        rock.vel.x = max(target_speed, rock.vel.x - rock.acceleration * dt)

    rock.vel.y = min(rock.max_fall_speed, rock.vel.y + rock.gravity * dt)

    extra_colliders = _as_list(colliders) + _as_list(fragile_surfaces)
    _move_axis(rock, extra_colliders, rock.vel.x * dt, "x")
    _move_axis(rock, extra_colliders, rock.vel.y * dt, "y")

    rock.delta_x = rock.rect.x - previous_x
    rock.delta_y = rock.rect.y - previous_y

    if player is not None and pygame.sprite.collide_mask(rock, player):
        respawn_actor(player)
        return True

    for block in _as_list(blocks):
        if rock.rect.colliderect(block.rect):
            block.pos.x += rock.delta_x
            block.rect.x = round(block.pos.x)

    return False
