import pygame
from physics import respawn_actor

def apply_gravity_to_spike_trap(spike_trap, dt):
    if not spike_trap.active:
        return

    spike_trap.vel.y = min(
        spike_trap.max_fall_speed,
        spike_trap.vel.y + spike_trap.gravity * dt,
    )
    spike_trap.pos.y += spike_trap.vel.y * dt
    spike_trap.rect.y = round(spike_trap.pos.y)

def check_spike_trap_collision(spike_trap, player):
    if spike_trap.active and pygame.sprite.collide_mask(spike_trap, player):
        respawn_actor(player)
        return True
    return False

def reset_spike_trap(spike_trap):
    spike_trap.pos = pygame.math.Vector2(spike_trap.spawn_point)
    spike_trap.rect.topleft = (round(spike_trap.pos.x), round(spike_trap.pos.y))
    spike_trap.vel = pygame.math.Vector2(0, 0)
    spike_trap.active = False

def update_spike_trap(spike_trap, dt, player):
    apply_gravity_to_spike_trap(spike_trap, dt)
    return check_spike_trap_collision(spike_trap, player)

