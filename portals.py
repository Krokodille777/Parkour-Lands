import pygame
START_PORTAL_COLOR = (15, 61, 135)
END_PORTAL_COLOR = (235, 142, 2)
PORTAL_TYPES = {"start_portal", "end_portal"}
PORTAL_COOLDOWN = 1.0


def _is_portal(portal):
    return getattr(portal, "type", None) in PORTAL_TYPES


def set_portal_role(portal, role):
    if role not in PORTAL_TYPES:
        raise ValueError("Unknown portal role")
    portal.type = role
    if role == "start_portal":
        portal.image.fill(START_PORTAL_COLOR)
    else:
        portal.image.fill(END_PORTAL_COLOR)


def link_portals(portal1, portal2):
    if portal1 is portal2:
        raise ValueError("A portal cannot link to itself")
    if not _is_portal(portal1) or not _is_portal(portal2):
        raise ValueError("Both objects must be portals")
    if portal1.type == portal2.type:
        raise ValueError("Portals must start with different roles")
    portal1.linked_portal = portal2
    portal2.linked_portal = portal1


def teleport_player(player, portal):
    linked_portal = getattr(portal, "linked_portal", None)
    if linked_portal is None:
        return False

    locked_portal = getattr(player, "portal_lock", None)
    colliding_with_portal = pygame.sprite.collide_mask(player, portal)
    if locked_portal is portal and not colliding_with_portal:
        player.portal_lock = None
        locked_portal = None

    if not colliding_with_portal:
        return False
    if portal.type != "start_portal":
        return False
    if locked_portal is portal:
        return False
    if portal.cooldown > 0 or linked_portal.cooldown > 0:
        return False

    player.pos.x = linked_portal.rect.centerx - player.rect.width / 2
    player.pos.y = linked_portal.rect.centery - player.rect.height / 2
    player.rect.topleft = (round(player.pos.x), round(player.pos.y))
    player.vel.x = 0
    player.vel.y = 0
    player.on_ground = False
    player.ground = None

    set_portal_role(portal, "end_portal")
    set_portal_role(linked_portal, "start_portal")
    portal.cooldown = PORTAL_COOLDOWN
    linked_portal.cooldown = PORTAL_COOLDOWN
    player.portal_lock = linked_portal
    return True


def teleport_pushable_block(block, portal):
    linked_portal = getattr(portal, "linked_portal", None)
    if linked_portal is None:
        return False

    locked_portal = getattr(block, "portal_lock", None)
    colliding_with_portal = pygame.sprite.collide_mask(block, portal)
    if locked_portal is portal and not colliding_with_portal:
        block.portal_lock = None
        locked_portal = None

    if not colliding_with_portal:
        return False
    if portal.type != "start_portal":
        return False
    if locked_portal is portal:
        return False
    if portal.cooldown > 0 or linked_portal.cooldown > 0:
        return False

    block.pos.x = linked_portal.rect.centerx - block.rect.width / 2
    block.pos.y = linked_portal.rect.centery - block.rect.height / 2
    block.rect.topleft = (round(block.pos.x), round(block.pos.y))
    block.vel.x = 0
    block.vel.y = 0
    block.on_ground = False
    block.ground = None

    set_portal_role(portal, "end_portal")
    set_portal_role(linked_portal, "start_portal")
    portal.cooldown = PORTAL_COOLDOWN
    linked_portal.cooldown = PORTAL_COOLDOWN
    block.portal_lock = linked_portal
    return True

def cooldown_timer(portal, dt):
    if portal.cooldown > 0:
        portal.cooldown = max(0.0, portal.cooldown - dt)

