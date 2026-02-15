

def follow_player(player, screen_width, world_width, screen_height, world_height):
    # Center the player on the screen, but clamp to world bounds
    offset_x = screen_width // 2 - round(player.pos.x) - player.rect.width // 2
    offset_x = max(min(offset_x, 0), screen_width - world_width)
    offset_x = int(offset_x)  # Ensure it's an integer for blitting

    offset_y = screen_height // 2 - round(player.pos.y) - player.rect.height // 2
    offset_y = max(min(offset_y, 0), screen_height - world_height)
    
    return offset_x, offset_y   