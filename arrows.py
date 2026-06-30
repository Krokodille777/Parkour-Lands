import math
import pygame
from physics import respawn_actor
from sprites import Arrow


def _as_list(items):
    if items is None:
        return []
    if hasattr(items, "rect"):
        return [items]
    return [item for item in items if hasattr(item, "rect")]


def _direction_from_angle(angle):
    radians = math.radians(angle)
    return pygame.math.Vector2(math.cos(radians), math.sin(radians))


def shoot_arrow(launcher, arrows, all_sprites=None, layer=2):
    arrow = Arrow(
        launcher.rect.centerx,
        launcher.rect.centery,
        30,
        12,
        launcher.angle,
        launcher.launch_speed,
    )
    direction = _direction_from_angle(launcher.angle)
    arrow.vel = direction * launcher.launch_speed
    arrow.pos.x -= arrow.rect.width / 2
    arrow.pos.y -= arrow.rect.height / 2
    arrow.rect.topleft = (round(arrow.pos.x), round(arrow.pos.y))

    arrows.add(arrow)
    if all_sprites is not None:
        try:
            all_sprites.add(arrow, layer=layer)
        except TypeError:
            all_sprites.add(arrow)
    return arrow


def update_arrow_launcher(launcher, arrows, all_sprites, dt, layer=2):
    if not getattr(launcher, "active", True):
        return None

    launcher.shoot_timer += dt
    if launcher.shoot_timer < launcher.shoot_interval:
        return None

    launcher.shoot_timer = 0.0
    return shoot_arrow(launcher, arrows, all_sprites, layer)


def update_arrows(arrows, dt, colliders=None, player=None, world_rect=None):
    for arrow in list(arrows):
        arrow.age += dt
        arrow.pos.x += arrow.vel.x * dt
        arrow.pos.y += arrow.vel.y * dt
        arrow.rect.topleft = (round(arrow.pos.x), round(arrow.pos.y))

        if arrow.age >= arrow.lifetime:
            arrow.kill()
            continue

        if world_rect is not None and not arrow.rect.colliderect(world_rect):
            arrow.kill()
            continue

        if player is not None and pygame.sprite.collide_mask(arrow, player):
            respawn_actor(player)
            arrow.kill()
            continue

        for collider in _as_list(colliders):
            if collider is arrow or not arrow.rect.colliderect(collider.rect):
                continue

            if getattr(collider, "type", None) in ("fragile_surface", "glass"):
                collider.kill()
            arrow.kill()
            break
