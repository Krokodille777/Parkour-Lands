from sprites import FinishLevelTrigger
import pygame


def level_complete(player, finish_trigger):
    if player.rect.colliderect(finish_trigger.rect):
        return True
    return False


def display_level_complete_message(screen, font):
    message = "Level Complete!"
    text_surface = font.render(message, True, (255, 255, 255))  # White color
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)