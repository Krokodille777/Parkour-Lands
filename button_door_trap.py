'''
A file for creating physics to buttons, doors, and traps. This will be used to create puzzles in the game.

Shortly about them:

Buttons themselves are useless until they are linked to something. Only things they can be linked to are doors and traps. When a button is pressed, it will activate all linked objects. When a button is released, it will deactivate all linked objects.

'''
import pygame
from sprites import Player, PushableBlock

def press_button(player, block, buttons):
    for button in buttons:
        if player.colliderect(button.rect) or block.rect.colliderect(button.rect):
            button.pressed = True
        else:
            button.pressed = False

def link_button_to_door(buttons, doors):
    for button in buttons:
        for door in doors:
            if getattr(door, "linked_button", None) == button:
                door.open = button.pressed

def link_button_to_trapdoor(buttons, traps):
    for button in buttons:
        for trap in traps:
            if getattr(trap, "linked_button", None) == button:
                trap.active = button.pressed

def open_door_trapdoor(doors, traps):
    for door in doors:
        if door.open:
            door.rect.height = 0
            door.mask = pygame.mask.from_surface(door.image)
        else:
            door.rect.height = door.original_height
            door.mask = pygame.mask.from_surface(door.image)
    for trap in traps:
        if trap.active:
            trap.rect.height = trap.original_height
            trap.mask = pygame.mask.from_surface(trap.image)
        else:
            trap.rect.height = 0
            trap.mask = pygame.mask.from_surface(trap.image)


