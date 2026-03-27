import pygame
from pygame.locals import *


from Levels.ch_01_plains.level1 import Level1
from Levels.ch_01_plains.level2 import Level2
from Levels.ch_01_plains.level3 import Level3
from Levels.ch_01_plains.level4 import Level4
from Levels.ch_01_plains.level5 import Level5
from Levels.ch_01_plains.level6 import Level6
from Levels.ch_01_plains.level7 import Level7
from Levels.ch_02_too_many_spikes.level21 import Level21
from Levels.ch_02_too_many_spikes.level22 import Level22
from Levels.ch_02_too_many_spikes.level23 import Level23
from Levels.ch_02_too_many_spikes.level24 import Level24
from Levels.ch_02_too_many_spikes.level25 import Level25
from Levels.ch_02_too_many_spikes.level26 import Level26
from Levels.ch_02_too_many_spikes.level27 import Level27
from Levels.ch_02_too_many_spikes.level28 import Level28
from Levels.ch_02_too_many_spikes.level29 import Level29
from Levels.ch_02_too_many_spikes.level30 import Level30

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

LEVELS = [Level1, Level2, Level3, Level4, Level5, Level6, Level7, Level21, Level22, Level23, Level24, Level25, Level26, Level27, Level28, Level29, Level30]
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
