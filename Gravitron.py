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


class Gravitron:
    __slots__ = ['x', 'y', 'power', 'rad', 'gravity', 'sucker', 'display']

    def __init__(self, cords: tuple, power: float, rad: float, display: Display):
        self.x, self.y = cords
        self.power = power
        self.gravity = True
        self.sucker = False
        self.display = display
        self.rad = rad

    def render(self):
        pygame.draw.circle(self.display.display, (0, 0, 0), (self.x, self.y), self.rad)


class BlackHole(Gravitron):
    def __init__(self, cords: tuple, power: float, rad: int, display: Display):
        super().__init__(cords, power, rad, display)
        self.sucker = True

    def render(self):
        pygame.draw.circle(self.display.display, (0, 0, 0), (self.x, self.y), self.rad)

    def grow(self, rad):
        self.rad += rad / 10
        self.power += rad / 5
