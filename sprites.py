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


        if keys[K_x]:
            self.pos = pygame.math.Vector2(self.spawn_point)
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
            self.vel = pygame.math.Vector2(0, 0)
            self.gravity_direction = "down"

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
        self.image.fill((255, 20, 147))  # Deep pink color for alter stand
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
        self.color = (255, 20, 147)
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

def retrieve_speeds(_type: str):
    return ACCELERATION_SPEED, DECELERATION_SPEED
