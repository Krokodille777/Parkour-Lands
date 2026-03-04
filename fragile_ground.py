from sprites import FragileGround
import pygame
def is_standing_on(player, platform):
    return (
        abs(player.rect.bottom - platform.rect.top) <= 2
        and player.rect.right > platform.rect.left
        and player.rect.left < platform.rect.right
    )
def fragile_ground_check(player, fragile_grounds, colliders, dt):
    for fg in fragile_grounds:
        if fg.broken:
            continue
        if not is_standing_on(player, fg):
            fg.break_timer = 0 # Reset timer if player is not standing on it
            continue
        #If player is standing on fragile ground, the platform starts breaking. If the player stays on it for 0.5 second, it breaks and the player falls through.
        fg.break_timer += dt
        if fg.break_timer >= 0.5:  # Break after 0.5 second
            fg.broken = True
            fg.kill()  # удаляем спрайт из всех групп, чтобы он перестал рендериться и коллайдиться
            colliders.remove(fg)  # удаляем из коллайдеров, чтобы игрок мог провалиться
def respawn_fragile_ground(colliders, all_sprites, fragile_grounds, dt):
    for fg in fragile_grounds:
        if fg.broken:
            fg.respawn_timer += dt
            if fg.respawn_timer >= 3.0:  # Respawn after 3 seconds
                all_sprites.add(fg, layer = 0)  # Add back to the sprite group to render it
                colliders.append(fg)  # Add back to colliders so player can collide with it again
                fg.break_timer = 0
                fg.respawn_timer = 0
                fg.broken = False
