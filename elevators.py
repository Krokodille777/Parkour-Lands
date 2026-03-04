import pygame
from sprites import ElevatorUpDown, ElevatorLeftRight
def updown_elevator_movement(elevator, range,  dt):
    elevator.rect.y += elevator.direction * 100 * dt  # Move at 100 pixels per second
    if elevator.rect.y < elevator.start_y - range:
        elevator.rect.y = elevator.start_y - range
        elevator.direction = 1  # Change direction to down
    elif elevator.rect.y > elevator.start_y + range:
        elevator.rect.y = elevator.start_y + range
        elevator.direction = -1  # Change direction to up
        

def leftright_elevator_movement(elevator, range, dt):
    elevator.rect.x += elevator.direction * 100 * dt  # Move at 100 pixels per second
    if elevator.rect.x < elevator.start_x - range:
        elevator.rect.x = elevator.start_x - range
        elevator.direction = 1  # Change direction to right
    elif elevator.rect.x > elevator.start_x + range:
        elevator.rect.x = elevator.start_x + range
        elevator.direction = -1  # Change direction to left