import pygame
import math
from physics import respawn_actor

def get_trap_pos(trap):
    return trap.pos


def pendulum_motion(trap, dt):
    trap.angle += trap.angular_velocity * dt

    if trap.angle > trap.max_angle:
        trap.angle = trap.max_angle
        trap.angular_velocity *= -1
    elif trap.angle < -trap.max_angle:
        trap.angle = -trap.max_angle
        trap.angular_velocity *= -1

    radians = math.radians(trap.angle)
    center_x = trap.pivot.x + math.sin(radians) * trap.arm_length
    center_y = trap.pivot.y + math.cos(radians) * trap.arm_length
    trap.rect.center = (round(center_x), round(center_y))
    trap.pos = pygame.math.Vector2(trap.rect.topleft)


def check_mace_trap_collision(mace_trap, player):
    if pygame.sprite.collide_mask(mace_trap, player):
        respawn_actor(player)
        return True
    return False

def update_mace_trap(mace_trap, dt, player):
    pendulum_motion(mace_trap, dt)
    return check_mace_trap_collision(mace_trap, player)
