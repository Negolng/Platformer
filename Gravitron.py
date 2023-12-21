import pygame


class Display:
    __slots__ = ['display', 'size', 'fps', 'air_loss', 'gravity_c', 'friction_c', 'gravity_direction', 'movement_speed']

    def __init__(self, display: pygame.display, size: tuple, frps: int, loss: float, gravitation: float,
                 friction: float, direction: int, speed: float | int):
        self.display = display
        self.size = size
        self.fps = frps
        self.air_loss = loss
        self.gravity_c = gravitation
        self.friction_c = friction
        self.gravity_direction = direction
        self.movement_speed = speed
