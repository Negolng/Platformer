from random import randint
import sqlite3
import pygame
import sys
import os

pygame.init()
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


class Cursor(pygame.sprite.Sprite):
    image = load_image('criss_cross.png')

    def __init__(self, my_group, all_objects, cords):
        super().__init__(my_group, all_objects)
        self.image = self.__class__.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords


def rand_pos():
    return tuple((randint(0, width), randint(0, height)))


def rand_col():
    return tuple((randint(0, 255), randint(0, 255), randint(0, 255)))


def play_music(music, loops):
    pygame.mixer.music.load(os.path.join('music', music))
    pygame.mixer.music.play(loops)


def save_game(all_objects, name):
    pass
    '''    connection = sqlite3.connect('saves.db')
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO names(name) VALUES("{name}")')
        req = """
        
        """
        for obj in all_objects:
            pass
        connection.commit()'''


save_game([0], 'a')
FPS = 120

dispy = Display(screen, screensize, FPS, 0.001, 9.802, 0.1, 1, 3)
