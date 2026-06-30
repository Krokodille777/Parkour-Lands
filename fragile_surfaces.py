def _as_list(items):
    if items is None:
        return []
    if hasattr(items, "rect"):
        return [items]
    return [item for item in items if hasattr(item, "rect")]


def _remove_surface(surface, colliders=None):
    surface.broken = True
    surface.kill()
    if colliders is not None and surface in colliders:
        colliders.remove(surface)


def break_surface(surface, player=None, block=None, colliders=None):
    breakers = _as_list(player) + _as_list(block)
    for breaker in breakers:
        if breaker.rect.colliderect(surface.rect):
            _remove_surface(surface, colliders)
            return True
    return False


def break_glass(glass, player=None, block=None, colliders=None):
    return break_surface(glass, player, block, colliders)


def break_fragile_surfaces(surfaces, breakers, colliders=None):
    broke_any = False
    for surface in _as_list(surfaces):
        if getattr(surface, "broken", False):
            continue
        if break_surface(surface, breakers, None, colliders):
            broke_any = True
    return broke_any


