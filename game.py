import pygame
from pygame.locals import *

from sprites import Ground, Player

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

# Create sprite instances
ground = Ground(20, 700, 800, 100)
player = Player(45, 625, 50, 50)
# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(ground)
all_sprites.add(player)


running = True
while running:
    clock.tick(60)  # Limit to 60 FPS

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        

    # Update sprites
    all_sprites.update()

    #Sky color
    screen.fill((119, 164, 237))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()