import pygame
from sprites import ElevatorUpDown, ElevatorLeftRight
def updown_elevator_movement(elevator, range,  dt):
    previous_y = elevator.rect.y
    elevator.delta_x = 0
    elevator.pos.y += elevator.direction * 100 * dt  # Move at 100 pixels per second
    if elevator.pos.y < elevator.start_y - range:
        elevator.pos.y = elevator.start_y - range
        elevator.direction = 1  # Change direction to down
    elif elevator.pos.y > elevator.start_y + range:
        elevator.pos.y = elevator.start_y + range
        elevator.direction = -1  # Change direction to up
    elevator.rect.y = round(elevator.pos.y)
    elevator.delta_y = elevator.rect.y - previous_y

        

def leftright_elevator_movement(elevator, range, dt):
    previous_x = elevator.rect.x
    elevator.delta_y = 0
    elevator.pos.x += elevator.direction * 100 * dt  # Move at 100 pixels per second
    if elevator.pos.x < elevator.start_x - range:
        elevator.pos.x = elevator.start_x - range
        elevator.direction = 1  # Change direction to right
    elif elevator.pos.x > elevator.start_x + range:
        elevator.pos.x = elevator.start_x + range
        elevator.direction = -1  # Change direction to left
    elevator.rect.x = round(elevator.pos.x)
    elevator.delta_x = elevator.rect.x - previous_x
