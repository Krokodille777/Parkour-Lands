'''
A file for creating physics to buttons, doors, and traps. This will be used to create puzzles in the game.

Shortly about them:

Buttons themselves are useless until they are linked to something. Only things they can be linked to are doors and traps. When a button is pressed, it will activate all linked objects. When a button is released, it will deactivate all linked objects.

'''


def _iter_blocks(blocks):
    if blocks is None:
        return []
    if hasattr(blocks, "rect"):
        return [blocks]
    return [block for block in blocks if hasattr(block, "rect")]


def _iter_actors(actors):
    if actors is None:
        return []
    if hasattr(actors, "rect"):
        return [actors]
    return [actor for actor in actors if hasattr(actor, "rect")]


def press_button(players, blocks, buttons):
    for button in buttons:
        player_pressing = any(actor.rect.colliderect(button.rect) for actor in _iter_actors(players))
        block_pressing = any(block.rect.colliderect(button.rect) for block in _iter_blocks(blocks))
        button.set_pressed(player_pressing or block_pressing)


def link_button_to_door(buttons, doors):
    for door in doors:
        linked_button = getattr(door, "linked_button", None)
        linked_from_button = any(door in getattr(button, "linked_objects", []) and button.pressed for button in buttons)
        door.open = bool((linked_button and linked_button.pressed) or linked_from_button)


def link_button_to_trapdoor(buttons, traps):
    for trap in traps:
        linked_button = getattr(trap, "linked_button", None)
        linked_from_button = any(trap in getattr(button, "linked_objects", []) and button.pressed for button in buttons)
        trap.open = bool((linked_button and linked_button.pressed) or linked_from_button)
def link_button_to_fan(buttons, fans):
    for fan in fans:
        linked_button = getattr(fan, "linked_button", None)
        linked_from_button = any(fan in getattr(button, "linked_objects", []) and button.pressed for button in buttons)
        fan.active = bool((linked_button and linked_button.pressed) or linked_from_button)

def open_door_trapdoor(doors, traps):
    for door in doors:
        door.set_open(door.open)
    for trap in traps:
        trap.set_open(trap.open)


def activate_fan_from_button(buttons, fans):
    for fan in fans:
        linked_button = getattr(fan, "linked_button", None)
        linked_from_button = any(fan in getattr(button, "linked_objects", []) and button.pressed for button in buttons)
        fan.active = bool((linked_button and linked_button.pressed) or linked_from_button)