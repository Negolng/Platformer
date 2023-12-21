from Gravitron import Gravitron, BlackHole, Display
from random import randint
import pygame
import sys
import os

fps = 120

pygame.init()
width, height = screensize = (900, 600)
screen = pygame.display.set_mode(screensize)
dispy = Display(screen, screensize, fps, 0.001, 9.802, 0.1, 1, 3)


def rand_col():
    return tuple((randint(0, 255), randint(0, 255), randint(0, 255)))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"АХ ТЫЖ СУКА! ГДЕ {fullname}, БЛЯТЬ?!?!!? ГДЕ?!?!?!\nAAAAAAAAAAAAAAA")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):
    __slots__ = ['display', 'x', 'y', 'rad', 'x_vel', 'y_vel', 'colour', 'bounce_c', 'others', 'gravy_objects']
    image = load_image('ball.png', -1)

    def __init__(self, display: Display, cords: tuple, radius: int, x_velocity: int | float, y_velocity: int | float,
                 grav_objects: list, other_sprites: pygame.sprite.Group, bounce_c: float = 0.8):
        super().__init__(other_sprites)
        self.rect = Ball.image.get_rect()
        pygame.transform.scale(dispy.display, (radius, radius))

        self.display = display
        self.x, self.y = cords
        self.rad = radius
        self.x_vel = x_velocity
        self.y_vel = y_velocity
        self.bounce_c = bounce_c
        self.spawn_check()

        self.gravy_objects = grav_objects

    def draw(self):
        pygame.draw.circle(self.display.display, self.colour, (self.x, self.y), self.rad)

    def spawn_check(self):
        status = self.check_borders(self.x, self.y)
        if status == 1:
            self.y = self.display.size[1] - self.rad - 1
            self.bounce()
        elif status == 2:
            self.x = self.rad + 1
            self.bounce_wall()
        elif status == 3:
            self.y = self.rad + 1
            self.bounce()
        elif status == 4:
            self.x = self.display.size[0] - self.rad - 1
            self.bounce_wall()

    def render(self):
        if self.x_vel != 0 or self.y_vel != 0:
            self.velocity_air_friction()
            self.change_cords()
            self.clear()
        self.be_gavitated()
        self.friction()
        self.draw()

    def update(self, *args, **kwargs):
        if self.x_vel != 0 or self.y_vel != 0:
            self.velocity_air_friction()
            self.change_cords()
            self.clear()
        self.be_gavitated()
        self.friction()

        self.rect.x = self.x - self.rad
        self.rect.y = self.y - self.rad

    def bounce(self):
        self.y_vel = -(self.y_vel * self.bounce_c - self.y_vel * self.display.friction_c)

    def bounce_wall(self):
        self.x_vel = -(self.x_vel * self.bounce_c - self.x_vel * self.display.friction_c)

    def check_borders(self, x, y):
        if x - self.rad <= 0:
            return 2
        elif x + self.rad >= self.display.size[0]:
            return 4
        elif y + self.rad >= self.display.size[1]:
            return 1
        elif y - self.rad <= 0:
            return 3

    def change_cords(self):
        new_x = self.x + self.x_vel / self.display.fps
        new_y = self.y + self.y_vel / self.display.fps
        status = self.check_borders(new_x, new_y)
        if status:
            if status % 2 == 0:
                self.bounce_wall()
            else:
                self.bounce()
        else:
            self.x = new_x
            self.y = new_y
        # print('I calculated my points: ', self.x_vel, self.y_vel, id(self))

    def be_sucked_to_a_point(self, obj, distance):
        self.x_vel += (obj.power / distance) * (1 if self.x < obj.x else -1)
        self.y_vel += (obj.power / distance) * (1 if self.y < obj.y else -1)

    def gravy_point_collision(self, obj):
        if isinstance(obj, BlackHole):
            obj.grow(self.rad)
            self.kill()

    def be_gavitated(self):
        for obj in self.gravy_objects:
            if isinstance(obj, Gravitron):
                if obj.gravity:
                    distance = (abs(self.y - obj.y)**2 + abs(self.x - obj.x)**2)**0.5
                    if distance > self.rad + obj.rad:
                        self.be_sucked_to_a_point(obj, distance)
                    else:
                        self.gravy_point_collision(obj)
        if self.display.gravity_c != 0:
            self.gravity_on_direction()

    def friction(self):
        if self.y + self.rad >= self.display.size[1] - 1 or self.y - self.rad <= 1:
            self.x_vel -= self.x_vel * self.display.friction_c
        if self.x - self.rad <= 1 or self.x + self.rad >= self.display.size[0] - 1:
            self.y_vel -= self.y_vel * self.display.friction_c

    def gravity_on_direction(self):
        if self.y + self.rad < self.display.size[1] and self.display.gravity_direction == 1:
            self.y_vel += self.display.gravity_c
        if self.y - self.rad > 0 and self.display.gravity_direction == 3:
            self.y_vel -= self.display.gravity_c
        if self.x - self.rad > 0 and self.display.gravity_direction == 2:
            self.x_vel -= self.display.gravity_c
        if self.x + self.rad < self.display.size[0] and self.display.gravity_direction == 4:
            self.x_vel += self.display.gravity_c

    def clear(self):
        if abs(round(self.x_vel / self.display.fps, 3)) < 0.05:
            self.x_vel = 0
        if abs(round(self.y_vel / self.display.fps, 3)) < 0.05:
            self.y_vel = 0

    def velocity_air_friction(self):
        self.x_vel -= round(self.x_vel * (self.display.air_loss / self.display.fps), 3)
        self.y_vel -= round(self.y_vel * (self.display.air_loss / self.display.fps), 3)

    def __str__(self):
        return str(id(self))

    def __repr__(self):
        return self.__str__()


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


class BetterGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def move(self, direction, speed):
        for sprite in self.sprites():
            if direction == 1:
                sprite.rect.y += speed
            elif direction == 2:
                sprite.rect.x -= speed
            elif direction == 3:
                sprite.rect.y -= speed
            elif direction == 4:
                sprite.rect.x += speed


class Box(pygame.sprite.Sprite):
    image = load_image('box.png')
    __slots__ = ['y_vel', 'display', 'border', 'other_sprites', 'falling']

    def __init__(self, my_group: pygame.sprite.Group, x: int, y: int, display: Display,
                 border: pygame.sprite.Group, falling: bool = False):
        super().__init__(my_group)
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
            while (pygame.sprite.spritecollideany(self, self.border) or
                    pygame.sprite.spritecollideany(self, self.other_sprites)):
                self.rect.y -= 1
                self.y_vel = 0


class MainCharacter(pygame.sprite.Sprite):
    __slots__ = ['rect', 'display', 'y_vel', 'borders', 'jumping', 'shrinked']
    image = load_image('charly_1.png')

    def __init__(self, my_group: pygame.sprite.Group, cords: tuple, display: Display,
                 borders: tuple[pygame.sprite.Group, pygame.sprite.Group], other_sprites: BetterGroup):
        super().__init__(my_group)
        self.image = MainCharacter.image
        self.rect = MainCharacter.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.y_vel = 0
        self.x_vel = 0
        self.display = display
        self.borders = borders
        self.other_sprites = other_sprites
        self.jumping = False
        self.mask = pygame.mask.from_surface(self.image)
        self.shrinked = False
        self.c = 0
        self.right = False
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.normal_image = self.image

    def update(self, cursor):

        if cursor:
            if cursor.rect.x > self.rect.x:
                self.image = self.flipped_image
                self.right = True

            else:
                self.image = self.normal_image
                self.right = False

        self.c += 1
        grav = True
        all_sprites = (pygame.sprite.spritecollide(self, self.other_sprites, False) +
                       pygame.sprite.spritecollide(self, self.borders[1], False))
        bunny = pygame.sprite.Sprite()
        bunny.rect = self.image.get_rect()
        bunny.image = self.image
        bunny.mask = pygame.mask.from_surface(bunny.image)
        bunny.rect.y, bunny.rect.x = self.rect.y, self.rect.x
        for sprite in all_sprites:
            ox, oy = sprite.rect.x, sprite.rect.y
            sx, sy = self.rect.x, self.rect.y
            if pygame.sprite.collide_mask(self, sprite):
                if oy > sy - 1:
                    self.jumping = False
                self.y_vel = 0
                grav = False

                while pygame.sprite.collide_mask(bunny, sprite):

                    if not isinstance(sprite, Border):
                        if sprite.falling is True and sprite.y_vel > 2:
                            bunny.rect.y -= 1
                        else:
                            if sy < oy:
                                bunny.rect.y -= 1
                            elif sy > oy:
                                bunny.rect.y += 1
                            else:
                                bunny.rect.y = -100
                    else:
                        bunny.rect.y -= 1

                self.rect.y = bunny.rect.y + 1
                self.rect.x = bunny.rect.x

        if grav:
            self.rect.y += self.y_vel
            self.y_vel += self.display.gravity_c / self.display.fps

    def move(self, direction, coeff):
        speed = self.display.movement_speed * coeff

        if direction == 4:
            if self.right:
                self.image = self.normal_image
                self.mask = pygame.mask.from_surface(self.image)
                self.right = False
            self.rect.x -= speed
            if any([pygame.sprite.collide_mask(self, sprite) and self.rect.y > sprite.rect.y
                    for sprite in self.other_sprites]):
                self.rect.x += speed

        elif direction == 1:
            self.rect.y -= 1
            self.y_vel -= speed * 1.5

        elif direction == 2:
            if not self.right:
                self.image = self.flipped_image
                self.mask = pygame.mask.from_surface(self.image)
                self.right = True
            self.rect.x += speed

            if any([pygame.sprite.collide_mask(self, sprite) and self.rect.y > sprite.rect.y
                    for sprite in self.other_sprites]):
                self.rect.x -= speed


class AI(MainCharacter):
    def __init__(self, *args, player):
        super().__init__(*args)
        self.player = player

    def update(self, cursor):
        MainCharacter.update(self, None)
        self.chase()

    def chase(self):
        sx, sy = self.rect.x, self.rect.y
        px, py = self.player.rect.x, self.player.rect.y
        distance = (abs(sx - px)**2 + abs(sy - py))**0.5
        if sx > px:
            if distance > 20:
                self.move(4, 0.5)
        elif sx < px:
            if distance > 20:
                self.move(2, 0.5)


class Platform(Box):
    image = load_image('platform.png')


class Cursor(pygame.sprite.Sprite):
    image = load_image('criss_cross_2.png')

    def __init__(self, my_group, cords):
        super().__init__(my_group)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords


class Particles(pygame.sprite.Sprite):
    def __init__(self, particle_group, cords):
        super().__init__(particle_group)
        self.cords = cords
        self.frame_c = 0
        self.particles = []
        self.image = pygame.Surface((randint(5, 10), randint(5, 10)))
        self.rect = self.image.get_rect()
        self.summon()

    def summon(self):
        for i in range(10):
            particle = pygame.sprite.Sprite()
            particle.image = pygame.Surface((randint(5, 10), randint(5, 10)))
            particle.image.fill((0, 0, 0))
            particle.rect = particle.image.get_rect()
            particle.rect.x, particle.rect.y = self.cords
            self.particles.append(particle)

    def update(self):
        self.frame_c += 1
        for particle in self.particles:
            if self.frame_c % 60 == 0:
                particle.rect.x += randint(-3, 3)
                particle.rect.y += randint(-3, 3)
