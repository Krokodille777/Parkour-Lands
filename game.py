import pygame
from pygame.locals import *


from Levels.ch_01_plains.level1 import Level1
from Levels.ch_01_plains.level2 import Level2
from Levels.ch_01_plains.level3 import Level3
from Levels.ch_01_plains.level4 import Level4


pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

LEVELS = [Level1, Level2, Level3, Level4]
current_level_index = 0
current_level = LEVELS[current_level_index]()

running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds


    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
    current_level.update(dt)
    current_level.draw(screen)

    if current_level.is_finished():
        current_level_index+=1
        if current_level_index >= len(LEVELS):
            print("Congratulations! You've completed all levels!")
            running = False
        else:
            current_level = LEVELS[current_level_index]()

            
    pygame.display.flip()

pygame.quit()
