from tech import Display, load_image, BetterGroup
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
        self.shrinked = False
        self.c = 0
        self.right = False
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.normal_image = self.image

    def update(self, cursor):
        self.c += 1

        self.turn_to_cursor(cursor)
        self.gravity()  # goddamn boolshit, this func is complete crap

    def move(self, direction, coeff):
        speed = self.display.movement_speed * coeff
        if self.right:
            self.image = self.normal_image

        else:
            self.image = self.flipped_image

        self.mask = pygame.mask.from_surface(self.image)
        self.right = not self.right

        if direction == 2:
            speed = -speed

        if direction % 2 == 0:
            self.rect.x -= round(speed)

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
                            bunny.rect.y = -100
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
                self.right = True
            else:
                self.image = self.normal_image
                self.right = False


class AI(MainCharacter):
    def __init__(self, *args, player, player_group):
        super().__init__(*args)
        self.player = player
        self.player_group = player_group
        self.draw_vision = False
        self.vision = None

    def update(self, cursor):
        super().update(None)
        self.vision_rect()
        self.chase()

    def chase(self):
        if self.vision and pygame.sprite.spritecollideany(self.vision, self.player_group):
            sx, sy = self.rect.x, self.rect.y
            px, py = self.player.rect.x, self.player.rect.y
            direction = 0
            if sx > px:
                direction = 4
            elif sx < px:
                direction = 2
            self.move(direction, 0.5)

    def vision_rect(self):
        g = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite(g)
        vision_size = (250, 200)
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
