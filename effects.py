#Background effects for the game: Shaking, Fog, Bloom, etc
import pygame
from pygame.locals import *
import random
def shake_effect(intensity, duration):
    clock = pygame.time.Clock()
    elapsed_time = 0
    while elapsed_time < duration:
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)
        # Apply the offset to the screen or camera position
        # For example, if you have a camera object:
        # camera.set_offset(offset_x, offset_y)
        pygame.display.flip()
        elapsed_time += clock.tick(60) / 1000.0  # Convert milliseconds to seconds

def fog_effect(screen, color, alpha):
    fog_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    fog_surface.fill(color + (alpha,))
    screen.blit(fog_surface, (0, 0))

def bloom_effect(screen, intensity):
    # Create a bloom surface
    bloom_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    bloom_surface.fill((255, 255, 255, intensity))  # White bloom with specified intensity
    # Apply a blur effect to the bloom surface (this is a placeholder, actual blur implementation may vary)
    # For example, you can use a Gaussian blur function here
    # blurred_bloom = gaussian_blur(bloom_surface)
    # For simplicity, we'll just use the bloom surface directly
    screen.blit(bloom_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)


def apply_shake_effect(screen, intensity, duration):
    shake_effect(intensity, duration)

def apply_fog_effect(screen, color, alpha):
    fog_effect(screen, color, alpha)
    
def apply_bloom_effect(screen, intensity):
    bloom_effect(screen, intensity)