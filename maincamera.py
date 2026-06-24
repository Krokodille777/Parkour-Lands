def _clamp_offset(offset, min_offset, max_offset):
    if min_offset > max_offset:
        return (min_offset + max_offset) // 2
    return max(min(offset, max_offset), min_offset)


def _follow_target(
    target,
    screen_width,
    world_width,
    screen_height,
    world_height,
    world_left=0,
    world_top=0,
):
    # Positive max offsets let the camera show map parts placed before x=0 or y=0.
    max_offset_x = -world_left
    min_offset_x = screen_width - (world_left + world_width)
    offset_x = screen_width // 2 - round(target.pos.x) - target.rect.width // 2
    offset_x = int(_clamp_offset(offset_x, min_offset_x, max_offset_x))

    max_offset_y = -world_top
    min_offset_y = screen_height - (world_top + world_height)
    offset_y = screen_height // 2 - round(target.pos.y) - target.rect.height // 2
    offset_y = int(_clamp_offset(offset_y, min_offset_y, max_offset_y))

    return offset_x, offset_y


def follow_targetlevel510(
    target,
    screen_start_x,
    world_start_x,
    screen_end_x,
    world_end_x,
    screen_width,
    world_width,
    screen_height,
    world_height,
):
    world_left = world_start_x
    world_width = world_end_x - world_start_x
    return _follow_target(
        target,
        screen_width,
        world_width,
        screen_height,
        world_height,
        world_left,
    )


def follow_player(
    player,
    screen_width,
    world_width,
    screen_height,
    world_height,
    world_left=0,
    world_top=0,
):
    return _follow_target(
        player,
        screen_width,
        world_width,
        screen_height,
        world_height,
        world_left,
        world_top,
    )


def follow_player_level510(
    player,
    screen_start_x,
    world_start_x,
    screen_end_x,
    world_end_x,
    screen_width,
    world_width,
    screen_height,
    world_height,
):
    return follow_targetlevel510(
        player,
        screen_start_x,
        world_start_x,
        screen_end_x,
        world_end_x,
        screen_width,
        world_width,
        screen_height,
        world_height,
    )


def follow_alter_player(
    alter_player,
    screen_width,
    world_width,
    screen_height,
    world_height,
    world_left=0,
    world_top=0,
):
    return _follow_target(
        alter_player,
        screen_width,
        world_width,
        screen_height,
        world_height,
        world_left,
        world_top,
    )
