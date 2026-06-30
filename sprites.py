import pygame

from pygame.locals import *


#Static sprites classes + Player class


#Class for ground and platforms

class Ground (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((56, 156, 79))  # Black color for ground
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'ground' # Type identifier for ground objects

#Class for player

class Player (pygame.sprite.Sprite):
    SPEED = 400
    JUMP_VEL = -750
    ICE_ACCEL = 600       # How fast the player accelerates on ice (px/s²)
    ICE_FRICTION = 300    # How fast the player decelerates on ice when no input (px/s²)

    def __init__(self, x, y, width, height):
        super().__init__()
        self.color = (0, 0, 255)
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.spawn_point = pygame.math.Vector2(x, y)
        self.crouching = False
        self.squashed = False # squashing is similar to crouching, but unlike crouching, it shortens the player's width.
        self.full_width = width
        self.full_height = height
        self.mask = pygame.mask.from_surface(self.image)
        self.type = "player"
        self.on_updown_elevator = False
        self.on_leftright_elevator = False
        self.ground = None
        self.on_ice = False
        self.ice = None
        self.frozen = False
        self.portal_lock = None
        self.gravity_direction = "down"

    def _apply_body_size(self, width, height, anchor_y):
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        if self.gravity_direction == "down":
            self.rect = self.image.get_rect(bottomleft = (round(self.pos.x), anchor_y))
        else:
            self.rect = self.image.get_rect(topleft = (round(self.pos.x), anchor_y))
        self.pos.y = float(self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)

    def handle_input(self, dt=1/60):
        if self.frozen:
            self.vel = pygame.math.Vector2(0, 0)
            return

        keys = pygame.key.get_pressed()

        # Determine desired direction
        direction = 0
        if keys[K_LEFT] or keys[K_a]:
            direction -= 1
        if keys[K_RIGHT] or keys[K_d]:
            direction += 1

        # Horizontal movement
        if self.on_ice:
            # On ice: gradually accelerate / decelerate (sliding feel)
            if direction != 0:
                self.vel.x += direction * self.ICE_ACCEL * dt
                # Clamp to max speed
                if self.vel.x > self.SPEED:
                    self.vel.x = self.SPEED
                elif self.vel.x < -self.SPEED:
                    self.vel.x = -self.SPEED
            else:
                # No input: apply friction to slow down
                if self.vel.x > 0:
                    self.vel.x = max(0, self.vel.x - self.ICE_FRICTION * dt)
                elif self.vel.x < 0:
                    self.vel.x = min(0, self.vel.x + self.ICE_FRICTION * dt)
        else:
            # Normal ground: instant response
            self.vel.x = direction * self.SPEED

        # Jumping
        if (keys[K_SPACE] or keys[K_UP] or keys[K_w]) and self.on_ground:
            if self.gravity_direction == "up":
                self.vel.y = -self.JUMP_VEL
            else:
                self.vel.y = self.JUMP_VEL

        if keys[K_c]:
            self.crouching = True
        if keys[K_v]:
            self.squashed = True

        anchor_y = self.rect.bottom if self.gravity_direction == "down" else self.rect.top
        target_width = self.full_width // 2 if self.squashed else self.full_width
        target_height = self.full_height // 2 if self.crouching else self.full_height
        self._apply_body_size(target_width, target_height, anchor_y)



class JumpPad (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, launch_vel):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))  # Yellow
        self.rect = self.image.get_rect(topleft = (x, y))
        self.type = 'jumppad' # Type identifier for jump pad objects
        self.launch_vel = launch_vel

    


class Lava (pygame.sprite.Sprite):
     def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 165, 0))  # Orange color for lava
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'lava' # Type identifier for lava object


class Water (pygame.sprite.Sprite):
     def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((7, 97, 242))  # Deep Sky Blue color for water
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'water' # Type identifier for water object
     

class Spike(pygame.sprite.Sprite):
     def __init__(self, x, y, width, height, angle): #angle parameter will make spikes' class universal, as they will have similar physics, no matter the direction they point
        super().__init__()
        self.angle = angle % 360
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 0, 0), [(0, height), (width // 2, 0), (width, height)])  # Draw a triangle for the spike
        self.image = pygame.transform.rotate(self.image, self.angle)  # Rotate the spike to the specified angle
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'spike' # Type identifier for spike object

class DynamicSpikePlatform(pygame.sprite.Sprite): #A platform where dynamic spikes are placed. It has the same physics as normal ground, but different color and type identifier, so we can add different physics if needed in the future.
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 0, 0))  # Dark red color for dynamic spike platform
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'dynamic_spike_platform' # Type identifier for dynamic spike platform objects

class DynamicSpike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle):
        super().__init__()
        self.angle = angle % 360
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 0, 0), [(0, height), (width // 2, 0), (width, height)])  # Draw a triangle for the spike
        self.image = pygame.transform.rotate(self.image, self.angle)  # Rotate the spike to the specified angle
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.original_y = y  # Store the original y position for oscillation
        self.amplitude = 12  # Oscillation amplitude in pixels
        self.original_x = x  # Store the original x position for oscillation (if needed for horizontal movement)
        self.frequency = 0.75  # Oscillation frequency in Hz
        self.phase = 0.0
        self.type = 'dynamic_spike' # Type identifier for dynamic spike object

class Icicle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle):
        super().__init__()
        self.angle = angle % 360
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (173, 216, 226), [(0, height), (width // 2, 0), (width, height)])  # Draw a triangle for the icicle
        self.image = pygame.transform.rotate(self.image, self.angle)  # Rotate the icicle to the specified angle
        self.image.fill((173, 216, 226), special_flags=pygame.BLEND_RGBA_MULT)  # Semi transparent light blue color for icicle
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'icicle' # Type identifier for icicle object

#Bridge class is similar to ground, but with different color and type identifier, so we can add different physics if needed in the future
class Bridge (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((139, 69, 19))  # Brown color for bridge
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'bridge' # Type identifier for bridge objects

#Ladder is completely different from other objects as it is not a collider, but a trigger for different physics (climbing), so it has its own class and type identifier. It's semi-transparent to indicate that it's not a solid object.
class Ladder (pygame.sprite.Sprite): 
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((160, 82, 45))  # Sienna color for ladder
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'ladder' # Type identifier for ladder objects


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((221, 2, 224))  # Magenta color for checkpoint
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'checkpoint'


#Dynamic sprites classes


#Fragile ground is a type of ground that breaks when the player steps on.
class FragileGround(Ground):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((169, 169, 169))  # Dark gray color for fragile ground
        self.break_timer = 0  
        self.break_delay = 0.5
        self.respawn_timer = 0
        self.breaking = False
        self.broken = False  
        self.type = 'fragile_ground' # Type identifier for fragile ground objects


class ElevatorUpDown(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, range):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 255))  # Cyan color for elevator
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.pos = pygame.math.Vector2(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'elevator_up_down' # Type identifier for elevator objects
        self.range = range
        self.direction = 1
        self.start_y = y
        self.delta_x = 0
        self.delta_y = 0

class ElevatorLeftRight(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, range):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 255))  # Cyan color for elevator
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.pos = pygame.math.Vector2(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'elevator_left_right' # Type identifier for elevator objects
        self.range = range
        self.direction = 1
        self.start_x = x
        self.delta_x = 0
        self.delta_y = 0


class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((173, 216, 230))  # Light blue color for ice
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'ice' # Type identifier for ice objects



#Portals

class StartPortal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((15, 61, 135))  # Light Blue color for start portal (like in Portal game)
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'start_portal' # Type identifier for start portal objects
        self.linked_portal = None
        self.cooldown = 0.0

class EndPortal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((235, 142, 2))  # Copper color for end portal (like in Portal game)
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'end_portal' # Type identifier for end portal objects
        self.linked_portal = None
        self.cooldown = 0.0


class Fan (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction, force, range):
        super().__init__()
        self.direction = direction  # Direction should be a normalized vector (e.g., (0, -1) for up)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self._draw_body()
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'fan' # Type identifier for fan objects
        self.force = force
        self.range = range

    def _draw_body(self):
        width, height = self.image.get_size()
        body_rect = self.image.get_rect()
        border_radius = max(4, min(width, height) // 4)
        frame_color = (202, 210, 219)
        outline_color = (92, 102, 112)
        grille_color = (73, 83, 94)
        flow_color = (119, 225, 245, 220)

        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, frame_color, body_rect, border_radius=border_radius)
        pygame.draw.rect(self.image, outline_color, body_rect, width=2, border_radius=border_radius)

        center = body_rect.center
        hub_radius = max(4, min(width, height) // 6)
        blade_length = max(hub_radius + 4, min(width, height) // 2 - 2)
        blade_width = max(4, min(width, height) // 6)

        blades = [
            ((center[0], center[1] - blade_length), (center[0] - blade_width, center[1]), (center[0] + blade_width, center[1])),
            ((center[0] + blade_length, center[1]), (center[0], center[1] - blade_width), (center[0], center[1] + blade_width)),
            ((center[0], center[1] + blade_length), (center[0] - blade_width, center[1]), (center[0] + blade_width, center[1])),
            ((center[0] - blade_length, center[1]), (center[0], center[1] - blade_width), (center[0], center[1] + blade_width)),
        ]
        for blade in blades:
            pygame.draw.polygon(self.image, grille_color, blade)

        pygame.draw.circle(self.image, outline_color, center, hub_radius + 2)
        pygame.draw.circle(self.image, (220, 227, 234), center, hub_radius)
        self._draw_flow_markers(flow_color)

    def _draw_flow_markers(self, color):
        width, height = self.image.get_size()
        direction_x, direction_y = self.direction

        if direction_x != 0:
            arrow_span = max(8, width // 3)
            shaft_start = 5 if direction_x > 0 else width - 5
            shaft_end = width - 9 if direction_x > 0 else 9
            y_positions = [height // 4, height // 2, (height * 3) // 4]
            for y in y_positions:
                pygame.draw.line(self.image, color, (shaft_start, y), (shaft_end, y), 3)
                if direction_x > 0:
                    tip = [(width - 5, y), (width - arrow_span, y - 5), (width - arrow_span, y + 5)]
                else:
                    tip = [(5, y), (arrow_span, y - 5), (arrow_span, y + 5)]
                pygame.draw.polygon(self.image, color, tip)
        elif direction_y != 0:
            arrow_span = max(8, height // 3)
            shaft_start = 5 if direction_y > 0 else height - 5
            shaft_end = height - 9 if direction_y > 0 else 9
            x_positions = [width // 4, width // 2, (width * 3) // 4]
            for x in x_positions:
                pygame.draw.line(self.image, color, (x, shaft_start), (x, shaft_end), 3)
                if direction_y > 0:
                    tip = [(x, height - 5), (x - 5, height - arrow_span), (x + 5, height - arrow_span)]
                else:
                    tip = [(x, 5), (x - 5, arrow_span), (x + 5, arrow_span)]
                pygame.draw.polygon(self.image, color, tip)



#Logic Sprites 

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.released_color = (0, 255, 0)
        self.pressed_color = (0, 180, 0)
        self.image = pygame.Surface((width, height))
        self.image.fill(self.released_color)  # Green color for button
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'button' # Type identifier for button objects
        self.linked_objects = []  # List of objects that this button controls
        self.pressed = False

    def set_pressed(self, pressed):
        self.pressed = pressed
        self.image.fill(self.pressed_color if pressed else self.released_color)
        self.mask = pygame.mask.from_surface(self.image)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.closed_color = (139, 69, 19)
        self.base_topleft = (x, y)
        self.original_width = width
        self.original_height = height
        self.closed_image = pygame.Surface((width, height))
        self.closed_image.fill(self.closed_color)  # Spruce color for door
        self.image = self.closed_image.copy()
        self.rect = self.image.get_rect(topleft = self.base_topleft)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'door' # Type identifier for door objects
        self.open = False
        self.linked_button = None

    def set_open(self, is_open):
        self.open = is_open
        if self.open:
            self.image = pygame.Surface((self.original_width, self.original_height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            self.rect = pygame.Rect(self.base_topleft[0], self.base_topleft[1], self.original_width, 0)
        else:
            self.image = self.closed_image.copy()
            self.rect = pygame.Rect(
                self.base_topleft[0],
                self.base_topleft[1],
                self.original_width,
                self.original_height,
            )
        self.mask = pygame.mask.from_surface(self.image)

class TrapDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.closed_color = (110, 60, 18)
        self.base_topleft = (x, y)
        self.original_width = width
        self.original_height = height
        self.closed_image = pygame.Surface((width, height))
        self.closed_image.fill(self.closed_color)  # Spruce color for trap door
        self.image = self.closed_image.copy()
        self.rect = self.image.get_rect(topleft = self.base_topleft)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'trap_door' # Type identifier for trap door objects
        self.open = False
        self.linked_button = None

    def set_open(self, is_open):
        self.open = is_open
        if self.open:
            self.image = pygame.Surface((self.original_width, self.original_height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            self.rect = pygame.Rect(self.base_topleft[0], self.base_topleft[1], self.original_width, 0)
        else:
            self.image = self.closed_image.copy()
            self.rect = pygame.Rect(
                self.base_topleft[0],
                self.base_topleft[1],
                self.original_width,
                self.original_height,
            )
        self.mask = pygame.mask.from_surface(self.image)

class ControllableFan(Fan):
    def __init__(self, x, y, width, height, direction, force, range):
        super().__init__(x, y, width, height, direction, force, range)
        self.active = False  # Fan starts inactive

    def set_active(self, active):
        self.active = active
        if self.active:
            self._draw_body()  # Draw normal fan when active
        else:
            self.image.fill((0, 0, 0, 0))  # Make invisible when inactive
            self.mask = pygame.mask.from_surface(self.image)
class PushableBlock(pygame.sprite.Sprite):
    SPEED = 0
    JUMP_VEL = -700
    ICE_ACCEL = 600       # How fast the player accelerates on ice (px/s²)
    ICE_FRICTION = 300   # How fast the player decelerates on ice when no input (px/s²)
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 0))  # Olive color for pushable block
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'pushable_block' # Type identifier for pushable block objects
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.on_ice = False
        self.on_ground = False
        self.vel = pygame.math.Vector2(0, 0)
        self.on_updown_elevator = False
        self.on_leftright_elevator = False
        self.portal_lock = None
        self.ice = None
        self.ground = None
        self.spawn_point = pygame.math.Vector2(x, y)
        self.delta_x = 0
        self.delta_y = 0

    def handle_input(self, dt=1/60):
        direction = 0
        if self.on_ice:
            # On ice: gradually accelerate / decelerate (sliding feel)
            if direction != 0:
                self.vel.x += direction * self.ICE_ACCEL * dt
                # Clamp to max speed
                if self.vel.x > self.SPEED:
                    self.vel.x = self.SPEED
                elif self.vel.x < -self.SPEED:
                    self.vel.x = -self.SPEED
            else:
                # No input: apply friction to slow down
                if self.vel.x > 0:
                    self.vel.x = max(0, self.vel.x - self.ICE_FRICTION * dt)
                elif self.vel.x < 0:
                    self.vel.x = min(0, self.vel.x + self.ICE_FRICTION * dt)
        else:
            self.vel.x = 0


class PressTrap(pygame.sprite.Sprite):
    ANGLE_TO_DIRECTION = {
        0: "up",
        90: "right",
        180: "down",
        270: "left",
    }

    def __init__(self, x, y, width, height, angle):
        super().__init__()
        self.color = (207, 207, 207, 255)
        self.angle = angle % 360
        self.direction = self.ANGLE_TO_DIRECTION.get(self.angle, "down")
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(self.color)  # Light gray color for press trap
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'press_trap' # Type identifier for press trap objects
        self.original_x = self.rect.x
        self.original_y = self.rect.y
        self.original_width = self.rect.width
        self.original_height = self.rect.height
        self.range = 100
        self.amplitude = self.range
        self.move_duration = 0.5
        self.extended_wait_time = 1.0
        self.retracted_wait_time = 1.0
        self.state = "waiting_retracted"
        self.state_timer = 0.0
        self.phase = 0.0
        self.extension = 0




class AlterStand(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((110, 9, 9))  # Deep Red color for alter stand
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'alter_stand' # Type identifier for alter stand objects

# Gravity Jump Pad is a version of class jump pad, which switches the player's gravity, while launched.

class GravityJumpPad(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, launch_vel):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 255))  # Magenta color for gravity jump pad
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'gravity_jump_pad' # Type identifier for gravity jump pad objects
        self.launch_vel = launch_vel

class AlterPlayer(Player):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = (0, 0, 0)
        anchor_y = self.rect.bottom if self.gravity_direction == "down" else self.rect.top
        self._apply_body_size(self.full_width, self.full_height, anchor_y)
        self.type = 'alter_player' # Type identifier for alter player objects
        self.frozen = True # Alter player starts frozen until the player switches to it for the first time

    def handle_input(self, dt=1/60):
        super().handle_input(dt)

#Mr. Jekyll and Mr. Hyde. Alter player is a clone of the normal player, but with different color
#and type indentifier. Both players have the same physics.
# Mr.Hyde always spawns on the alter stand.
#You can switch players by pressing "1" for normal, player amd "2" for alter player.
#Important Rule!! When playing as one character, the other character is frozen in place and becomes a solid object and you can't use it, until you switch back to it.

class FinishLevelTrigger(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 215, 0))  # Gold color for finish level trigger
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'finish_level_trigger' # Type identifier for finish level trigger objects

#Tip cloud is a sprite that shows tips to the player when they meet new mechanics for the first time

class TipCloud(pygame.sprite.Sprite):
      def __init__(self, x, y, width, height, text):
          super().__init__()
          self.image = pygame.Surface((width, height), pygame.SRCALPHA)
          self.image.fill((255, 255, 224, 200))
          self.rect = self.image.get_rect(topleft=(x, y))
          self.type = "tip_cloud"

          font = pygame.font.SysFont(None, 24)
          lines = text.split("\n")
          y_offset = 10
          for line in lines:
              text_surface = font.render(line, True, (20, 20, 20))
              self.image.blit(text_surface, (10, y_offset))
              y_offset +=24



ACCELERATION_SPEED = 400
DECELERATION_SPEED = 600

#Sprites for chapter 6 and 7: 

#sky objects
class Void(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))  # Black color for void
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'void' # Type identifier for void objects
class NetherSky(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((30, 0, 0))  # Dark red color for nether sky
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'nether_sky' # Type identifier for nether sky objects

#ground objects
class SoulGround(Ground):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((128, 128, 128))  # Ash color for soul ground
        self.type = 'soul_ground' # Type identifier for soul ground objects
class CaveStone(Ground):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((105, 105, 105))  # Dim gray color for cave stone
        self.type = 'cave_stone' # Type identifier for cave stone objects
class NetherWall(Ground):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((139, 0, 0))  # Dark red color for nether wall
        self.type = 'nether_wall' # Type identifier for nether wall objects
class DarkFloor(Ground):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((47, 79, 79))  # Dark slate gray color for dark floor
        self.type = 'dark_floor' # Type identifier for dark floor objects

#Liquids
#Blood is a unique liquid that slows the player down.
class Blood(Water):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((138, 7, 7))  # Dark red color for blood
        self.type = 'blood' # Type identifier for blood objects
        self.slow_factor = 0.5  # Player's speed is reduced to 50% when in blood
class Acid(Water):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((0, 255, 0))  # Bright green color for acid
        self.type = 'acid' # Type identifier for acid objects

#Hazards
#Eising Lava rises and falls in a wavelike motion. Like dynamic spikes or press traps.


class EmberCrystal(Spike):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 140, 0), [(0, height), (width // 2, 0), (width, height)])
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'ember_crystal' # Type identifier for ember crystal objects

class Dripstone(Spike):
    def __init__(self, x, y, width, height, angle):
        super().__init__(x, y, width, height, angle)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (169, 169, 169), [(0, height), (width // 2, 0), (width, height)])
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'dripstone' # Type identifier for dripstone objects


### ========== NEW MECHANICS ========== ###
class DynamicLava(Lava):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((255, 69, 0))  # Orange red color for dynamic lava
        self.type = 'dynamic_lava' # Type identifier for dynamic lava objects
        self.original_y = y  # Store the original y position for oscillation
        self.range = 50  # Oscillation range in pixels
        self.amplitude = self.range  # Oscillation amplitude in pixels
        self.frequency = 0.5  # Oscillation frequency in Hz
        self.phase = 0.0  # Phase offset for oscillation


#New Traps
#Mace is hanging from the ceiling  and rotatesin a certain segment of a circle. It has a certain speed and requires timing.
class MaceTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle=0, speed=90, arm_length=100, max_angle=60):
        super().__init__()
        self.angle = angle
        self.angular_velocity = speed
        self.arm_length = arm_length
        self.max_angle = abs(max_angle)
        self.pivot = pygame.math.Vector2(x, y)
        self.original_x = x
        self.original_y = y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (105, 105, 105), (width // 2, height // 2), min(width, height) // 2)  # Draw a circle for the mace
        self.rect = self.image.get_rect(center=(x, y + arm_length))
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.type = 'mace_trap' # Type identifier for mace trap objects

#A huge rock is a large circular rock that rolls down with acceleration and can crush the player, boxes and can even be used to break fragile surafaces.
class HugeRock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, roll_direction=1):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (120, 120, 120), self.image.get_rect())
        pygame.draw.ellipse(self.image, (70, 70, 70), self.image.get_rect(), 3)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'huge_rock' # Type identifier for huge rock objects
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, 0)
        self.spawn_point = pygame.math.Vector2(x, y)
        self.roll_direction = 1 if roll_direction >= 0 else -1
        self.acceleration = 200  # Acceleration in px/s²
        self.gravity = 2500
        self.max_speed = 400
        self.max_fall_speed = 1400
        self.active = True
        self.delta_x = 0
        self.delta_y = 0

#Arrow Launcher shoots triangle arrows at a certain angle and speed. The player must dodge as good as they can to avoid getting hit.
class ArrowLauncher(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle, launch_speed, shoot_interval=2.0):
        super().__init__()
        self.angle = angle % 360
        self.launch_speed = launch_speed
        self.shoot_interval = shoot_interval
        self.shoot_timer = 0.0
        self.active = True
        self.linked_button = None
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (160, 82, 45), (0, 0, width, height))  # Draw a rectangle for the launcher
        self.image = pygame.transform.rotate(self.image, self.angle)  # Rotate the launcher to the specified angle
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'arrow_launcher' # Type identifier for arrow launcher objects
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, angle, speed, lifetime=5.0):
        super().__init__()
        self.angle = angle % 360
        self.speed = speed
        self.lifetime = lifetime
        self.age = 0.0
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (105, 55, 25), [(0, 0), (width, height // 2), (0, height)])  # Draw a triangle pointing right
        self.image = pygame.transform.rotate(self.image, -self.angle)  # Rotate the arrow to the specified angle
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'arrow' # Type identifier for arrow objects
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, 0)

#Activated by a button, the spike falls down. Player has seconds to dodge it if they don't want to get smashed.
class SpikeTrap(Spike):
    def __init__(self, x, y, width, height, angle, fall_speed=0):
        super().__init__(x, y, width, height, angle)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (169, 169, 169), [(0, height), (width // 2, 0), (width, height)])
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'spike_trap' # Type identifier for spike trap objects
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, fall_speed)
        self.spawn_point = pygame.math.Vector2(x, y)
        self.start_y = y
        self.gravity = 2500
        self.max_fall_speed = 900
        self.active = False
        self.linked_button = None

#New Gameplay Mechanics
#A special type of ground which looks weathered enough to be broken by the player or other objects like box, arrow or huge rock.
class FragileSurface(Ground):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((169, 169, 169))  # Dark gray color for fragile surface
        self.type = 'fragile_surface' # Type identifier for fragile surface objects
        self.break_timer = 0  
        self.break_delay = 0.5
        self.respawn_timer = 0
        self.breaking = False
        self.broken = False
class Glass(FragileSurface):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((135, 206, 250))  # Light sky blue color for glass
        self.type = 'glass' # Type identifier for glass objects

#The Nether's alternative to fans. They erupt sulfur gas which pushes the player up. The should only be placed on the top of surfaces.
class SulfurGeiser(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, force, direction=(0, -1), range=250):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((255, 255, 0, 128))  # Semi-transparent yellow color for sulfur geiser
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'sulfur_geiser' # Type identifier for sulfur geiser objects
        self.force = force
        self.direction = direction
        self.range = range

#The dynamic version of the ladder. It is hanging from the ceiling and stands still until player interacts with it. It starts to move back and forth like a pendulum. Player can climb and jump off it like a normal ladder.
class Vine(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, amplitude=50, frequency=0.5):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((89, 47, 25))  # Brown color for vine
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'vine' # Type identifier for vine objects
        self.original_x = x
        self.original_y = y
        self.amplitude = amplitude  # Oscillation amplitude in pixels
        self.frequency = frequency  # Oscillation frequency in Hz
        self.phase = 0.0  # Phase offset for oscillation
        self.active = False
        self.delta_x = 0
        self.delta_y = 0


class Vein(Vine):
    def __init__(self, x, y, width, height, amplitude=50, frequency=0.5):
        super().__init__(x, y, width, height, amplitude, frequency)
        self.image.fill((139, 0, 0))  # Dark red color for nether vein
        self.type = 'vein' # Backward-compatible type identifier

#This type of lava rises uncontrollably and the player must escape it. It will be used in the final level of chapter 7 as the final exam.
class RisingLava(Lava):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((255, 69, 0))  # Orange red color for rising lava
        self.type = 'rising_lava' # Type identifier for rising lava objects
        self.rise_speed = 50  # Speed at which the lava rises in pixels per second


#Decoration: Fire, portals, elevators, dead trees, fog

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((255, 69, 0, 128))  # Semi-transparent orange color for fire
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'fire' # Type identifier for fire objects

class Fog(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((169, 169, 169, 128))  # Semi-transparent gray color for fog
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'fog' # Type identifier for fog objects

class DeadTree(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((139, 69, 19))  # Brown color for dead tree
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'dead_tree' # Type identifier for dead tree objects

class PurplePortal(StartPortal):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((128, 0, 128))  # Purple color for purple portal
        self.type = 'purple_portal' # Type identifier for purple portal objects
class GreenPortal(EndPortal):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((0, 128, 0))  # Green color for green portal
        self.type = 'green_portal' # Type identifier for green portal objects

class DustyElevatorUpDown(ElevatorUpDown):
    def __init__(self, x, y, width, height, range):
        super().__init__(x, y, width, height, range)
        self.image.fill((169, 169, 169))  # Dusty gray color for dusty elevator up-down
        self.type = 'dusty_elevator_up_down' # Type identifier for dusty elevator up-down objects

class DustyElevatorLeftRight(ElevatorLeftRight):
    def __init__(self, x, y, width, height, range):
        super().__init__(x, y, width, height, range)
        self.image.fill((169, 169, 169))  # Dusty gray color for dusty elevator left-right
        self.type = 'dusty_elevator_left_right' # Type identifier for dusty elevator left-right objects


#Endgame sprites: The mysterious guy, credits cloud

class MysteriousGuy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))  # Black color for mysterious guy
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'mysterious_guy' # Type identifier for mysterious guy objects

class CreditsCloud(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 200))  # Semi-transparent black color for credits cloud
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = 'credits_cloud' # Type identifier for credits cloud objects

        font = pygame.font.SysFont(None, 24)
        lines = text.split("\n")
        y_offset = 10
        for line in lines:
            text_surface = font.render(line, True, (0, 0, 0))
            self.image.blit(text_surface, (10, y_offset))
            y_offset += 24
def retrieve_speeds(_type: str):
    return ACCELERATION_SPEED, DECELERATION_SPEED
