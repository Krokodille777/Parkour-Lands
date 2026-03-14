import math
import pygame


def get_trap_area(trap):
    if trap.direction == "down":
        return pygame.Rect(
            trap.original_x,
            trap.original_y,
            trap.original_width,
            trap.original_height + trap.range,
        )
    if trap.direction == "up":
        return pygame.Rect(
            trap.original_x,
            trap.original_y - trap.range,
            trap.original_width,
            trap.original_height + trap.range,
        )
    if trap.direction == "right":
        return pygame.Rect(
            trap.original_x,
            trap.original_y,
            trap.original_width + trap.range,
            trap.original_height,
        )
    if trap.direction == "left":
        return pygame.Rect(
            trap.original_x - trap.range,
            trap.original_y,
            trap.original_width + trap.range,
            trap.original_height,
        )
    return trap.rect.copy()


def _apply_extension(trap, extension):
    extension_px = max(0, min(int(round(extension)), trap.range))

    if trap.direction == "down":
        size = (trap.original_width, trap.original_height + extension_px)
        topleft = (trap.original_x, trap.original_y)
    elif trap.direction == "up":
        size = (trap.original_width, trap.original_height + extension_px)
        topleft = (trap.original_x, trap.original_y - extension_px)
    elif trap.direction == "right":
        size = (trap.original_width + extension_px, trap.original_height)
        topleft = (trap.original_x, trap.original_y)
    else:
        size = (trap.original_width + extension_px, trap.original_height)
        topleft = (trap.original_x - extension_px, trap.original_y)

    if trap.extension == extension_px and trap.rect.topleft == topleft and trap.image.get_size() == size:
        return

    trap.image = pygame.Surface(size, pygame.SRCALPHA)
    trap.image.fill(trap.color)
    trap.rect = trap.image.get_rect(topleft=topleft)
    trap.mask = pygame.mask.from_surface(trap.image)
    trap.extension = extension_px


def _wave_extension(trap, phase):
    trap.phase = phase
    return trap.range * (1 - math.cos(phase)) * 0.5


def _set_state(trap, state):
    trap.state = state
    trap.state_timer = 0.0

    if state == "waiting_retracted":
        trap.phase = 0.0
        _apply_extension(trap, 0)
    elif state == "waiting_extended":
        trap.phase = math.pi
        _apply_extension(trap, trap.range)


def update_press_trap(trap, dt):
    if trap.state == "waiting_retracted":
        trap.state_timer += dt
        if trap.state_timer >= trap.retracted_wait_time:
            _set_state(trap, "extending")
        else:
            _apply_extension(trap, 0)
        return

    if trap.state == "extending":
        trap.state_timer += dt
        progress = min(1.0, trap.state_timer / trap.move_duration)
        extension = _wave_extension(trap, progress * math.pi)
        _apply_extension(trap, extension)
        if progress >= 1.0:
            _set_state(trap, "waiting_extended")
        return

    if trap.state == "waiting_extended":
        trap.state_timer += dt
        if trap.state_timer >= trap.extended_wait_time:
            _set_state(trap, "retracting")
        else:
            _apply_extension(trap, trap.range)
        return

    if trap.state == "retracting":
        trap.state_timer += dt
        progress = min(1.0, trap.state_timer / trap.move_duration)
        extension = _wave_extension(trap, math.pi + progress * math.pi)
        _apply_extension(trap, extension)
        if progress >= 1.0:
            _set_state(trap, "waiting_retracted")


def apply_press_trap_effect(player, trap, dt):
    update_press_trap(trap, dt)
    return bool(player and pygame.sprite.collide_mask(player, trap))
