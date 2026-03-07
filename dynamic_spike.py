import pygame
from sprites import DynamicSpike
from pygame.locals import *
import math
'''
Dynamic Spikes are a subclass of Spike that can move up and down rhytmically. This should create a timing challenge for the player, as they will need to time their movements to avoid getting hit by the spikes. The movement of the spikes is controlled by a timer that oscillates between 0 and 1, creating a smooth up-and-down motion. The speed of the oscillation can be adjusted by changing the frequency variable.

'''

FREQUENCY = 0.08  # Oscillations per second
AMPLITUDE = 12   # How far the spike moves up and down from its original position
TIMER = 0.0   


#The function will work, depending on spike angle

def dynamic_spike_movement_based_on_timer(spike, dt):
    global TIMER
    TIMER += dt * FREQUENCY * 2 *math.pi  # Increment timer based on frequency
    offset = math.sin(TIMER) * AMPLITUDE  # Calculate vertical offset using sine wave
    if spike.angle == 0:  # Pointing up
        spike.rect.y = spike.original_y + offset
    elif spike.angle == 180:  # Pointing down
        spike.rect.y = spike.original_y - offset
    elif spike.angle == 90:  # Pointing right
        spike.rect.x = spike.original_x + offset
    elif spike.angle == 270:  # Pointing left
        spike.rect.x = spike.original_x - offset
        