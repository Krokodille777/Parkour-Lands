import pygame


def checkpoint_activation(player, checkpoint_group):
    for checkpoint in checkpoint_group:
        if player.rect.colliderect(checkpoint.rect):
            player.spawn_point = pygame.math.Vector2(checkpoint.rect.x, checkpoint.rect.y)
