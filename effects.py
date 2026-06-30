import pygame
import random


def shake_effect(intensity):
    """Returns a one-frame camera offset for screen shake."""
    if intensity <= 0:
        return 0, 0
    return random.randint(-intensity, intensity), random.randint(-intensity, intensity)


def fog_effect(screen, color, alpha):
    fog_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    fog_surface.fill(color + (alpha,))
    screen.blit(fog_surface, (0, 0))

def bloom_effect(screen, intensity):
    bloom_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    bloom_surface.fill((255, 255, 255, intensity))
    screen.blit(bloom_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)


def apply_shake_effect(screen, intensity, duration=None):
    return shake_effect(intensity)

def apply_fog_effect(screen, color, alpha):
    fog_effect(screen, color, alpha)
    
def apply_bloom_effect(screen, intensity):
    bloom_effect(screen, intensity)
