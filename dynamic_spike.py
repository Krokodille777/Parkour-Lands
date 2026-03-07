import pygame
from sprites import DynamicSpike
from pygame.locals import *

'''
Dynamic Spikes are a subclass of Spike that can move up and down rhytmically. This should create a timing challenge for the player, as they will need to time their movements to avoid getting hit by the spikes. The movement of the spikes is controlled by a timer that oscillates between 0 and 1, creating a smooth up-and-down motion. The speed of the oscillation can be adjusted by changing the frequency variable.

'''
def dynamic_spike_movement(spike, dt):
    frequency = 1.0  # Adjust this value to change the speed of the oscillation
    spike_timer = pygame.time.get_ticks() / 1000.0  # Get the current time in seconds
    spike_timer += dt * frequency
    spike.rect.y = spike.original_y + int(10 * pygame.math.sin(spike_timer))  # Adjust the amplitude (10) as needed
