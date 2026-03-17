
def _follow_target(target, screen_width, world_width, screen_height, world_height):
    offset_x = screen_width // 2 - round(target.pos.x) - target.rect.width // 2
    offset_x = max(min(offset_x, 0), screen_width - world_width)
    offset_x = int(offset_x)

    offset_y = screen_height // 2 - round(target.pos.y) - target.rect.height // 2
    offset_y = max(min(offset_y, 0), screen_height - world_height)
    offset_y = int(offset_y)

    return offset_x, offset_y


def follow_player(player, screen_width, world_width, screen_height, world_height):
    # Center the player on the screen, but clamp to world bounds
    return _follow_target(player, screen_width, world_width, screen_height, world_height)


def follow_alter_player(alter_player, screen_width, world_width, screen_height, world_height):
    # Hyde uses the same camera logic as Jekyll.
    return _follow_target(alter_player, screen_width, world_width, screen_height, world_height)
