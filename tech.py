import math
from random import randint, choice
import pygame
import sys
import os

pygame.init()
pygame.font.init()
width, height = screensize = (900, 600)
screen = pygame.display.set_mode(screensize)


def load_image(name, colorkey=None):
    fullname = os.path.join('textures', name)
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

    def draw(
        self, surface, bgsurf=None, special_flags=0
    ):
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect)

            if hasattr(sprite, 'gun'):
                sprite.gun.draw(surface)


class Cursor(pygame.sprite.Sprite):
    image = load_image('criss_cross.png')

    def __init__(self, my_group, all_objects, cords):
        super().__init__(my_group, all_objects)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords


def rand_pos():
    return tuple((randint(0, width - 30), randint(0, height - 30)))


def rand_col():
    return tuple((randint(0, 255), randint(0, 255), randint(0, 255)))


def play_music(music, loops):
    pygame.mixer.music.load(os.path.join('music', music))
    pygame.mixer.music.play(loops)


FPS = 120

dispy = Display(screen, screensize, FPS, 0.001, 9.802, 0.1, 1, 3)


def generate_level(necessary_objects, level_contains, player_and_ai, dick, player, player_group, ai_group, number):

    other_sprites, all_objects, border_sprites = necessary_objects
    bools = (True, False)
    number_of_boxes = randint(1, 50) * round(math.log10(number**2 + 1)) + 2
    for _ in range(number_of_boxes):
        y = randint(120, height)
        x = randint(0, width // 2 - 35) if choice(bools) else randint(width // 2 + 35, width - 30)
        if choice(bools):
            level_contains.Box(other_sprites, all_objects, x, y, dispy, border_sprites, True)
        else:
            level_contains.Platform(other_sprites, all_objects, x, y, dispy, border_sprites, True)

    for _ in range(FPS * 5):
        other_sprites.update()

    for _ in range(number):
        y = randint(120, height)
        x = randint(0, width // 2 - 35) if choice(bools) else randint(width // 2 + 35, width - 30)
        player_and_ai.AI(ai_group, all_objects, (x, y), dispy, dick, other_sprites, player=player,
                         player_group=player_group)


def starting_screen():
    disp = pygame.display.set_mode(screensize)
    font_of_death = pygame.font.SysFont('Papyrus', 50)
    surrealism = font_of_death.render('To start press SPACE', False, (255, 255, 255))
    start_screen = True
    while start_screen:
        start_screen = not pygame.key.get_pressed()[pygame.K_SPACE]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False

        disp.fill((0, 0, 0))
        disp.blit(surrealism, (0, 0))
        pygame.display.flip()
