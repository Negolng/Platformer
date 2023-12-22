from tech import Display, load_image, BetterGroup
from level_contains import Border
import pygame


class MainCharacter(pygame.sprite.Sprite):
    __slots__ = ['rect', 'display', 'y_vel', 'borders', 'jumping', 'shrinked']
    image = load_image('charly.png')

    def __init__(self, my_group: pygame.sprite.Group, all_objects: pygame.sprite.Group, cords: tuple, display: Display,
                 borders: tuple[pygame.sprite.Group, pygame.sprite.Group], other_sprites: BetterGroup):
        super().__init__(my_group, all_objects)
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
                        if sprite.falling and sprite.y_vel > 2:
                            bunny.rect.y -= 1
                        elif sy < oy:
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
        if distance > 20:
            if sx > px:
                self.move(4, 0.5)
            elif sx < px:
                self.move(2, 0.5)
