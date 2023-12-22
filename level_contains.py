from tech import load_image, Display
from random import randint
import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, sprites, vertical_borders, horizontal_borders):
        super().__init__(sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Box(pygame.sprite.Sprite):
    image = load_image('box.png')
    __slots__ = ['y_vel', 'display', 'border', 'other_sprites', 'falling']

    def __init__(self, my_group: pygame.sprite.Group, all_objects: pygame.sprite.Group,
                 x: int, y: int, display: Display,
                 border: pygame.sprite.Group, falling: bool = False):
        super().__init__(my_group, all_objects)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0
        self.display = display
        self.border = border
        self.other_sprites = pygame.sprite.Group()
        self.falling = falling
        self.mask = pygame.mask.from_surface(self.image)
        for sprite in my_group:
            if sprite != self:
                self.other_sprites.add(sprite)

    def update(self):
        if self.falling:
            self.rect.y += self.y_vel
            self.y_vel += self.display.gravity_c / self.display.fps

            while self._collides_with_border_or_sprites():
                self.rect.y -= 1
                self.y_vel = 0

    def _collides_with_border_or_sprites(self):
        return (pygame.sprite.spritecollideany(self, self.border) or
                pygame.sprite.spritecollideany(self, self.other_sprites))


class Platform(Box):
    image = load_image('platform.png')


class Particles(pygame.sprite.Sprite):
    def __init__(self, particle_group, cords):
        super().__init__(particle_group)
        self.cords = cords
        self.frame_c = 0
        self.particles = []
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
