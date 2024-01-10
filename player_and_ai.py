import random

import tech
import math
from tech import Display, load_image, BetterGroup
from weapons import Guns
from level_contains import Border
import pygame


class MainCharacter(pygame.sprite.Sprite):
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
        self.c = 0
        self.right = False
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.normal_image = self.image
        self.gun = pygame.sprite.Group()
        Guns.AK47(self.gun, all_objects, self, 10, 10, 10, 10)

    def update(self, cursor):
        self.c += 1
        self.turn_to_cursor(cursor)
        self.gravity()  # goddamn boolshit, this func is complete crap
        self.gun.update()
        self.gun.draw(self.display.display)

    def move(self, direction, coeff):
        speed = round(self.display.movement_speed * coeff)
        if direction == 2:
            speed = -speed
            self.right = True
        else:
            self.right = False

        if self.right:
            self.image = self.flipped_image
            if self.gun.sprites():
                self.gun.sprites()[0].image = self.gun.sprites()[0].flipped_image

        else:
            self.image = self.normal_image
            if self.gun.sprites():
                self.gun.sprites()[0].image = self.gun.sprites()[0].normal_image

        self.mask = pygame.mask.from_surface(self.image)

        if direction % 2 == 0:
            # a = math.log(10, 1 + random.random() * 10000)
            # print(a)
            self.rect.x -= speed

            if any([pygame.sprite.collide_mask(self, sprite) and self.rect.y > sprite.rect.y
                    for sprite in self.other_sprites]):
                self.rect.x += speed

        else:
            self.rect.y -= 1
            self.y_vel -= speed * 1.5

    def gravity(self):
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
                            self.jumping = True
                            if sx > ox:
                                bunny.rect.x += 1
                            else:
                                bunny.rect.x -= 1
                    else:
                        bunny.rect.y -= 1

                self.rect.y = bunny.rect.y + 1
                self.rect.x = bunny.rect.x

        if grav:
            self.rect.y += self.y_vel
            self.y_vel += self.display.gravity_c / self.display.fps

    def turn_to_cursor(self, cursor):
        if cursor:
            if cursor.rect.x > self.rect.x:
                self.image = self.flipped_image
                self.gun.sprites()[0].image = self.gun.sprites()[0].normal_image
                self.right = True
            else:
                self.image = self.normal_image
                self.gun.sprites()[0].image = self.gun.sprites()[0].flipped_image

                self.right = False

    def kill(self):
        if type(self) == MainCharacter:
            print("DEAD")
        pygame.sprite.Sprite.kill(self)
        pygame.sprite.Sprite.kill(self.gun.sprites()[0])

    def fire(self):
        if self.gun.sprites():
            self.gun.sprites()[0].fire(*pygame.mouse.get_pos(), *self.rect.center)


class AI(MainCharacter):
    def __init__(self, *args, player, player_group):
        super().__init__(*args)
        self.player = player
        self.player_group = player_group
        self.draw_vision = False
        self.vision = None
        self.hp = 10
        self.gun = pygame.sprite.Group()
        Guns.EnemyGun(self.gun, args[1], self, 10, 10, 10, 10)
        self.peaceful = False
        self.all_sprites = args[1]

    def update(self, cursor):
        if self.hp <= 0:
            self.kill()
        super().update(None)
        # self.vision_rect()
        self.chase()
        if not self.peaceful:
            self.murder()

    def do_we_see(self):
        if self.vision and pygame.sprite.spritecollideany(self.vision, self.player_group):
            return True
        return False

    def chase(self):
        if ((self.rect.x - self.player.rect.x) ** 2 + (self.rect.y - self.player.rect.y) ** 2)**0.5 > 20:
            sx, sy = self.rect.x, self.rect.y
            px, py = self.player.rect.x, self.player.rect.y
            direction = 0
            if sx > px:
                direction = 4
            elif sx < px:
                direction = 2

            if sy > py:
                if not self.jumping:
                    self.move(1, 0.5)
                    self.jumping = True
            self.move(direction, 0.5)

    def vision_rect(self):
        g = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite(g)
        vision_size = (tech.width, 200)
        pers_size = self.image.get_size()
        sprite.image = pygame.surface.Surface((vision_size[0] + pers_size[0], vision_size[1] + pers_size[1]))
        sprite.image.fill((0, 255, 0))
        if self.right:
            sprite.rect = pygame.rect.Rect((self.rect.x - pers_size[0],
                                            self.rect.y - pers_size[1] - vision_size[1] // 2),
                                           (vision_size[0] + pers_size[0], vision_size[1] + pers_size[1]))
        else:
            sprite.rect = pygame.rect.Rect((self.rect.x - vision_size[0] + pers_size[0],
                                            self.rect.y - pers_size[1] - vision_size[1] // 2),
                                           (vision_size[0] + pers_size[0], vision_size[1] + pers_size[1]))

        if self.draw_vision:
            g.draw(self.display.display)

        self.vision = sprite

    def vision_line(self):
        # Too much lag!!!!
        g = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite(g)
        xsiz = self.rect.x - self.player.rect.x
        ysiz = self.rect.y - self.player.rect.y

        sprite.image = pygame.surface.Surface((abs(xsiz), abs(ysiz) + 1))
        sprite.rect = self.rect.copy()
        sprite.rect.y -= 1
        if ysiz > 0:
            sprite.rect.y -= abs(ysiz)

        if xsiz > 0:
            sprite.rect.x -= abs(xsiz)

        sprite.image.set_colorkey((0, 0, 0))
        sprite.image = sprite.image.convert_alpha()
        pygame.draw.line(sprite.image, (255, 0, 0), (0, 0),
                         (sprite.image.get_size()[0], sprite.image.get_size()[1] - 1), 1)

        if (ysiz > 0 > xsiz) or (ysiz < 0 < xsiz):
            sprite.image = pygame.transform.flip(sprite.image, True, False)

        sprite.mask = pygame.mask.from_surface(sprite.image)
        if self.draw_vision:
            g.draw(self.display.display)

        # print(pygame.sprite.spritecollideany(self, self.all_sprites))
        print(self.all_sprites.sprites())

        if any([pygame.sprite.collide_mask(self, sprite) for sprite in self.other_sprites if
                not pygame.sprite.collide_mask(self, sprite)]):
            print(([sprite for sprite in self.other_sprites if pygame.sprite.collide_mask(self, sprite)]))

            return False

        return True

    def murder(self):
        if self.gun.sprites():
            self.gun.sprites()[0].fire(*self.player.rect.center, *self.rect.center)
