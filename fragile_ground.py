from sprites import FragileGround
import pygame

def is_standing_on(player, platform):
    return (
        abs(player.rect.bottom - platform.rect.top) <= 2
        and player.rect.right > platform.rect.left
        and player.rect.left < platform.rect.right
    )
def is_block_standing_on(block, platform):
    return (
        abs(block.rect.bottom - platform.rect.top) <= 2
        and block.rect.right > platform.rect.left
        and block.rect.left < platform.rect.right
    )


def trigger_fragile_ground(actor, box, fragile_grounds):
    for fg in fragile_grounds:
        if fg.broken or fg.breaking:
            continue
        if is_standing_on(actor, fg) or is_block_standing_on(box, fg):
            fg.breaking = True
            fg.break_timer = 0


def fragile_ground_check(player, box, fragile_grounds, colliders, dt):
    trigger_fragile_ground(player, box, fragile_grounds)

    for fg in fragile_grounds:
        if fg.broken or not fg.breaking:
            continue
        fg.break_timer += dt
        if fg.break_timer >= fg.break_delay:
            fg.broken = True
            fg.breaking = False
            fg.kill()  # Remove from all sprite groups to stop rendering and collisions
            if fg in colliders:
                colliders.remove(fg)  


def respawn_fragile_ground(colliders, all_sprites, fragile_grounds, dt):
    for fg in fragile_grounds:
        if fg.broken:
            fg.respawn_timer += dt
            if fg.respawn_timer >= 3.0:  # Respawn after 3 seconds
                all_sprites.add(fg, layer = 0)  # Add back to the sprite group to render it
                if fg not in colliders:
                    colliders.append(fg)  # Add back to colliders so player can collide with it again
                fg.break_timer = 0
                fg.respawn_timer = 0
                fg.breaking = False
                fg.broken = False
