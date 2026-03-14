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
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
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
        self.portal_lock = None

    def handle_input(self, dt=1/60):
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
            self.vel.y = self.JUMP_VEL
            self.on_ground = False

        # Crouching
        bottom = self.rect.bottom
        if keys[K_c]:
                self.crouching = True
                self.image = pygame.Surface((self.full_width, self.full_height // 2))
                self.image.fill((0, 0, 255))
        elif not self.crouching:
                self.image = pygame.Surface((self.full_width, self.full_height))
                self.image.fill((0, 0, 255))
       

        if keys[K_v]:
            self.squashed = True

            self.image = pygame.Surface((self.full_width // 2, self.full_height))
            self.image.fill((0, 0, 255))
        elif not self.crouching:
            self.image = pygame.Surface((self.full_width, self.full_height))
            self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(bottomleft = (round(self.pos.x), bottom))
        self.pos.y = float(self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)



class JumpPad (pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, launch_vel):
        super().__init__()
        self.image = pygame.Surface((width, height))
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


class Accelerator(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))  # Yellow color for accelerator
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'accelerator'

class Decelerator(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 128))  # Gray color for decelerator
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'decelerator'

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
    def __init__(self, x, y, width, height, direction):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((192, 192, 192))  # Silver color for fan
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'fan' # Type identifier for fan objects
        self.direction = direction  # Direction should be a normalized vector (e.g., (0, -1) for up)
        self.force =7500
        self.range = 1050


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
    SPEED = 400
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
    def __init__(self, x, y, width, height, angle):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((207, 207, 207, 255))  # Light gray color for press trap
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'press_trap' # Type identifier for press trap objects
class RestartButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Emerald color for restart button
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'restart_button' # Type identifier for restart button objects

class SwingingVine(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((34, 139, 34))  # Forest green color for vine
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'swinging_vine' # Type identifier for swinging vine objects

class AlterCreator(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 20, 147))  # Deep pink color for alter creator
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'alter_creator' # Type identifier for alter creator objects

class AlterRemover(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 105, 180))  # Hot pink color for alter remover
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'alter_remover' # Type identifier for alter remover objects

#Alterplayer is a special type of player which can be created and removed by alter creator and alter remover.
# Alter player can serve as a temporary helper you can take control of to reach certain places. 
# Alter player has the same physics as normal player, but different color and type identifier, so we can add different physics if needed in the future.
# To take control of alter player, player needs to press "2" key. It will automatically freeze the original player and move it to the older player's posittion.
# Alter players may be very useful during puzzle-solving parts.
# I don't know how I am going to implement this yet, It will be so interesting if it finally works. 
        
class AlterPlayer(pygame.sprite.Sprite):
    SPEED = 400
    JUMP_VEL = -750
    ICE_ACCEL = 600       # How fast the player accelerates on ice (px/s²)
    ICE_FRICTION = 300    # How fast the player decelerates on ice when no input (px/s²)

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0)) #Yellow
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
        self.portal_lock = None

    def handle_input(self, dt=1/60):
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
            self.vel.y = self.JUMP_VEL
            self.on_ground = False

        # Crouching
        bottom = self.rect.bottom
        if keys[K_c]:
                self.crouching = True
                self.image = pygame.Surface((self.full_width, self.full_height // 2))
                self.image.fill((0, 0, 255))
        elif not self.crouching:
                self.image = pygame.Surface((self.full_width, self.full_height))
                self.image.fill((0, 0, 255))
       

        if keys[K_v]:
            self.squashed = True

            self.image = pygame.Surface((self.full_width // 2, self.full_height))
            self.image.fill((0, 0, 255))
        elif not self.crouching:
            self.image = pygame.Surface((self.full_width, self.full_height))
            self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(bottomleft = (round(self.pos.x), bottom))
        self.pos.y = float(self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)


class FinishLevelTrigger(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 215, 0))  # Gold color for finish level trigger
        self.rect = self.image.get_rect(topleft = (x ,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.type = 'finish_level_trigger' # Type identifier for finish level trigger objects

ACCELERATION_SPEED = 400
DECELERATION_SPEED = 600

def retrieve_speeds(_type: str):
    return ACCELERATION_SPEED, DECELERATION_SPEED


