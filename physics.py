import pygame
from pygame.locals import *
from sprites import Player

GRAVITY = 2500
HAZARD_TYPES = {"spike", "dynamic_spike", "lava", "press_trap"}
MOVING_PLATFORM_TYPES = {"elevator_up_down", "elevator_left_right"}
PLATFORM_CONTACT_TOLERANCE = 6


def apply_gravity(player, dt: float):
    player.vel.y += GRAVITY * dt


def activate_gravity_jump_pad(player, pad):
    player.gravity_direction = "up" if player.gravity_direction == "down" else "down"
    player.vel.y = pad.launch_vel if player.gravity_direction == "up" else -pad.launch_vel
    player.vel.x += abs(pad.launch_vel) * 0.5 if player.vel.x >= 0 else -abs(pad.launch_vel) * 0.5
    player.on_ground = False
    player.ground = None


def _is_moving_platform(sprite):
    return getattr(sprite, "type", None) in MOVING_PLATFORM_TYPES


def _should_ignore_horizontal_platform_collision(collider, push_left, push_right, push_up, push_down):
    if getattr(collider, "delta_y", 0) == 0 or getattr(collider, "delta_x", 0) != 0:
        return False

    # Vertical elevators should resolve from top/bottom instead of side-shoving
    # the player when only a small vertical overlap is present near the edge.
    return min(push_up, push_down) <= min(push_left, push_right) + PLATFORM_CONTACT_TOLERANCE


def _carry_with_ground(player):
    ground = getattr(player, "ground", None)
    if not _is_moving_platform(ground):
        return
    gravity_direction = getattr(player, "gravity_direction", "down")
    if gravity_direction == "down" and player.vel.y < 0:
        return
    if gravity_direction == "up" and player.vel.y > 0:
        return

    if getattr(ground, "delta_x", 0) == 0 and getattr(ground, "delta_y", 0) == 0:
        return

    player.pos.x += ground.delta_x
    player.rect.x = round(player.pos.x)
    player.pos.y += ground.delta_y
    player.rect.y = round(player.pos.y)
    
def _carry_with_block(block):
      ground = getattr(block, "ground", None)
      if not _is_moving_platform(ground):
          return

      if getattr(ground, "delta_x", 0) == 0 and getattr(ground, "delta_y", 0) == 0:
          return

      block.pos.x += ground.delta_x
      block.rect.x = round(block.pos.x)
      block.pos.y += ground.delta_y
      block.rect.y = round(block.pos.y)

def move_and_collide(player, colliders, dt: float, triggers):
    _carry_with_ground(player)

    player.on_ground = False
    player.on_ice = False
    player.ground = None

    # --- Horizontal pass ---

    player.pos.x += player.vel.x * dt
    player.rect.x = round(player.pos.x)

    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        push_right = c.rect.right - player.rect.left
        push_left = player.rect.right - c.rect.left
        push_down = c.rect.bottom - player.rect.top
        push_up = player.rect.bottom - c.rect.top
        if _should_ignore_horizontal_platform_collision(c, push_left, push_right, push_up, push_down):
            continue
        if player.vel.x > 0:       # Moving right -> hit wall on the right
            player.rect.right = c.rect.left
        elif player.vel.x < 0:     # Moving left -> hit wall on the left
            player.rect.left = c.rect.right
        else:                       # Not moving horizontally but overlapping (e.g. resize)
            if push_right < push_left:
                player.rect.left = c.rect.right
            else:
                player.rect.right = c.rect.left
        player.pos.x = float(player.rect.x)

        

    # Check spike triggers after horizontal movement
    for t in triggers:
        if getattr(t, "type", None) not in HAZARD_TYPES:
            continue
        if not pygame.sprite.collide_mask(player, t):
            continue
        player.pos = pygame.math.Vector2(player.spawn_point)
        player.rect.topleft = (round(player.pos.x), round(player.pos.y))
        player.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        return


    # --- Vertical pass ---
    prev_rect_y = player.rect.copy()
    player.pos.y += player.vel.y * dt
    player.rect.y = round(player.pos.y)

    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        if prev_rect_y.bottom <= c.rect.top:       # Moving down -> land on top
            player.rect.bottom = c.rect.top
            player.vel.y = 0
            player.on_ground = True
            player.ground = c
            if getattr(c, "type", None) == "ice":
                player.on_ice = True
            if getattr(c, "type", None) == "jumppad":
                player.vel.y = c.launch_vel
                player.on_ground = False
                player.ground = None
            if getattr(c, "type", None) == "gravity_jump_pad":
                activate_gravity_jump_pad(player, c)
            if getattr(c, "type", None) == "lava":
                player.pos = pygame.math.Vector2(player.spawn_point)
                player.rect.topleft = (round(player.pos.x), round(player.pos.y))
                player.vel = pygame.math.Vector2(0, 0)
                player.on_ground = False
                player.ground = None
                return
        elif prev_rect_y.top >= c.rect.bottom:     # Moving up -> hit ceiling
            player.rect.top = c.rect.bottom
            player.vel.y = max(player.vel.y, 0)
        else:                       # Not moving vertically but overlapping (e.g. resize)
            push_down = c.rect.bottom - player.rect.top
            push_up   = player.rect.bottom - c.rect.top
            if push_up <= push_down:
                player.rect.bottom = c.rect.top
                player.vel.y = 0
                player.on_ground = True
                player.ground = c
                if getattr(c, "type", None) == "ice":
                    player.on_ice = True
            else:
                player.rect.top = c.rect.bottom
                player.vel.y = max(player.vel.y, 0)
        player.pos.y = float(player.rect.y)
    for t in triggers:
        if getattr(t, "type", None) not in HAZARD_TYPES:
            continue
        if not pygame.sprite.collide_mask(player, t):
            continue
        player.pos = pygame.math.Vector2(player.spawn_point)
        player.rect.topleft = (round(player.pos.x), round(player.pos.y))
        player.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        return
    


    # Crouching adjustment: prevent standing up if there isn't enough room
def crouching_adjustment(player, colliders):
    if not player.crouching:
        return

    # Build a test rect at full height, keeping the contact side fixed.
    if player.gravity_direction == "down":
        test_rect = pygame.Rect(
            player.rect.x,
            player.rect.bottom - player.full_height,
            player.full_width,
            player.full_height
        )
    else:
        test_rect = pygame.Rect(
            player.rect.x,
            player.rect.y,
            player.full_width,
            player.full_height
        )

    for c in colliders:
        if c is player:
            continue
        if test_rect.colliderect(c.rect):
            # Standing up would clip into this collider — stay crouched
            return

    # Enough room — allow standing up
    player.crouching = False

def squash_adjustment(player, colliders):
    if not player.squashed:
        return

    # Build a test rect at full width (anchored at current center)
    test_rect = pygame.Rect(
        player.rect.centerx - player.full_width // 2,  # Center the rect horizontally
        player.rect.y,  # Keep the same y position
        player.full_width,
        player.full_height
    )

    for c in colliders:
        if c is player:
            continue
        if test_rect.colliderect(c.rect):
            # Unsquashing would clip into this collider — stay squashed
            return

    # Enough room — allow unsquashing
    player.squashed = False

def x_pressed(player, box, colliders):
    keys = pygame.key.get_pressed()
    if keys[K_x]:
        player.pos = pygame.math.Vector2(60, 250)
        player.rect.topleft = player.pos
        player.vel = pygame.math.Vector2(0, 0)
        box.pos = pygame.math.Vector2(350, 155)
        box.rect.topleft = box.pos
        box.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        player.ground = None
        box.on_ground = False
        box.ground = None

#Gravity should affect only if you fall off the ladder, not while climbing. So we apply gravity in the main loop as usual, but if the player is on a ladder and pressing up/down, we override the vertical velocity and skip gravity for that frame.
def climb_ladder(player, ladder_group):
    on_ladder = False
    for ladder in ladder_group:
        if player.rect.colliderect(ladder.rect):
            on_ladder = True
            keys = pygame.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                player.vel.y = -Player.SPEED
            elif keys[K_DOWN] or keys[K_s]:
                player.vel.y = Player.SPEED
            else:
                player.vel.y = 0  # Stay still on the ladder if no vertical input
            break

def jump_from_the_top_of_ladder(player, ladder_group):
    for ladder in ladder_group:
        if player.rect.colliderect(ladder.rect):
            keys = pygame.key.get_pressed()
            if (keys[K_SPACE] or keys[K_UP] or keys[K_w]) and player.on_ground:
                player.vel.y = Player.JUMP_VEL if player.gravity_direction == "down" else -Player.JUMP_VEL
                player.on_ground = False




def buoyant_force(player, water_group):
    in_water = False
    for water in water_group:
        if player.rect.colliderect(water.rect):
            in_water = True
            # Simple buoyancy: if player is in water, reduce gravity effect and allow upward movement
            apply_gravity(player, 1/60)  # Apply gravity as usual
            player.vel.y *= 0.5  # Reduce downward velocity to simulate buoyancy
            player.vel.x *= 0.8  # Optional: reduce horizontal speed in water for more resistance
            keys = pygame.key.get_pressed()
            if keys[K_UP] or keys[K_w]:
                player.vel.y -= Player.SPEED * 0.5  # Allow upward movement in water
            break
    return in_water


def apply_speed_zones(player, triggers):
    for t in triggers:
        if getattr(t, "type", None) not in ("accelerator", "decelerator"):
            continue
        if player.rect.colliderect(t.rect):
            if t.type == "accelerator":
                player.vel.x *= 1.8
            elif t.type == "decelerator":
                player.vel.x *= 0.4






#Antigravity Physics

def apply_agt(player, dt: float):
    player.vel.y -= GRAVITY * dt  # Reverse gravity to create an antigravity effect

def agt_move_and_collide(player, colliders, dt: float, triggers):
    _carry_with_ground(player)
    player.on_ground = False
    player.on_ice = False
    player.ground = None

    # --- Horizontal pass ---
    player.pos.x += player.vel.x * dt
    player.rect.x = round(player.pos.x)

    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        push_right = c.rect.right - player.rect.left
        push_left = player.rect.right - c.rect.left
        push_down = c.rect.bottom - player.rect.top
        push_up = player.rect.bottom - c.rect.top
        if _should_ignore_horizontal_platform_collision(c, push_left, push_right, push_up, push_down):
            continue
        if player.vel.x > 0:
            player.rect.right = c.rect.left
        elif player.vel.x < 0:
            player.rect.left = c.rect.right
        else:
            if push_right < push_left:
                player.rect.left = c.rect.right
            else:
                player.rect.right = c.rect.left
        player.pos.x = float(player.rect.x)

    for t in triggers:
        if getattr(t, "type", None) not in HAZARD_TYPES:
            continue
        if not pygame.sprite.collide_mask(player, t):
            continue
        player.pos = pygame.math.Vector2(player.spawn_point)
        player.rect.topleft = (round(player.pos.x), round(player.pos.y))
        player.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        player.gravity_direction = "down"
        return

    # --- Vertical pass (reversed for antigravity) ---
    prev_rect_y = player.rect.copy()
    player.pos.y += player.vel.y * dt
    player.rect.y = round(player.pos.y)

    for c in colliders:
        if c is player:
            continue
        if not player.rect.colliderect(c.rect):
            continue
        if prev_rect_y.top >= c.rect.bottom:     # Moving up -> land on bottom
            player.rect.top = c.rect.bottom
            player.vel.y = 0
            player.on_ground = True
            player.ground = c
            if getattr(c, "type", None) == "ice":
                player.on_ice = True
            if getattr(c, "type", None) == "jumppad":
                player.vel.y = c.launch_vel
                player.on_ground = False
                player.ground = None
            if getattr(c, "type", None) == "gravity_jump_pad":
                activate_gravity_jump_pad(player, c)

            if getattr(c, "type", None) == "lava":
                player.pos = pygame.math.Vector2(player.spawn_point)
                player.rect.topleft = (round(player.pos.x), round(player.pos.y))
                player.vel = pygame.math.Vector2(0, 0)
                player.on_ground = False
                player.ground = None
                player.gravity_direction = "down"
                return
        elif prev_rect_y.bottom <= c.rect.top:       # Moving down -> hit ceiling
            player.rect.bottom = c.rect.top
            player.vel.y = min(player.vel.y, 0)

        else:                       # Not moving vertically but overlapping (e.g. resize)
            push_down = c.rect.bottom - player.rect.top
            push_up   = player.rect.bottom - c.rect.top
            if push_up <= push_down:
                player.rect.bottom = c.rect.top
                player.vel.y = min(player.vel.y, 0)
            else:
                player.rect.top = c.rect.bottom
                player.vel.y = 0

        player.pos.y = float(player.rect.y)
    for t in triggers:
        if getattr(t, "type", None) not in HAZARD_TYPES:
            continue
        if not pygame.sprite.collide_mask(player, t):
            continue
        player.pos = pygame.math.Vector2(player.spawn_point)
        player.rect.topleft = (round(player.pos.x), round(player.pos.y))
        player.vel = pygame.math.Vector2(0, 0)
        player.on_ground = False
        player.gravity_direction = "down"
        return
    
def frozen_adjustment(player, colliders):
    if not player.frozen:
        return

    player.vel = pygame.math.Vector2(0, 0)
    player.pos = pygame.math.Vector2(player.rect.topleft)
    player.on_ground = False
    player.ground = None
    player.on_ice = False


def switch_to_alter_player(player, alter_player):
    if player.frozen or not alter_player.frozen:
        return False  # Hyde is already active or the state is inconsistent.

    player.frozen = True
    alter_player.frozen = False
    frozen_adjustment(player, [])
    alter_player.vel = pygame.math.Vector2(0, 0)
    alter_player.on_ground = False
    alter_player.ground = None
    alter_player.on_ice = False
    return True

def switch_to_normal_player(player, alter_player):
    if alter_player.frozen or not player.frozen:
        return False  # Jekyll is already active or the state is inconsistent.

    alter_player.frozen = True
    player.frozen = False
    frozen_adjustment(alter_player, [])
    player.vel = pygame.math.Vector2(0, 0)
    player.on_ground = False
    player.ground = None
    player.on_ice = False
    return True
