def _as_list(items):
    if items is None:
        return []
    if hasattr(items, "rect"):
        return [items]
    return [item for item in items if hasattr(item, "rect")]


def slow_down_player(player, blood_areas=None, dt=None):
    """
    Slows the player while their rect overlaps blood.

    Use it after player.handle_input(), before move_and_collide():
        slow_down_player(self.player, [self.blood_pool], dt)
    """
    if isinstance(blood_areas, (int, float)):
        blood_areas = None

    touched_blood = False
    slow_factor = 0.5
    for blood in _as_list(blood_areas):
        if player.rect.colliderect(blood.rect):
            touched_blood = True
            slow_factor = getattr(blood, "slow_factor", slow_factor)
            break

    if blood_areas is None:
        touched_blood = True

    if not touched_blood:
        return False

    player.vel.x *= slow_factor
    player.vel.y *= max(0.35, slow_factor)
    return True
