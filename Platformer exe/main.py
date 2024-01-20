import math
from random import randint, choice
import random
import datetime
import pygame
import sys
import os


pygame.init()
pygame.font.init()
width, height = screensize = (900, 600)
screen = pygame.display.set_mode(screensize)
SCORE = 0
level = 1


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
                 friction: float, direction: int, speed):
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
                sys.exit()

        disp.fill((0, 0, 0))
        disp.blit(surrealism, (width // 2 - surrealism.get_width() // 2, 0))
        pygame.display.flip()
    logger('Game started')


def ending_screen():
    disp = pygame.display.set_mode(screensize)
    font_of_death = pygame.font.SysFont('Papyrus', 40)
    surrealism = font_of_death.render('YOU  ARE  DEAD', False, (255, 255, 255))
    imfunny = font_of_death.render('(haha lol)', False, (255, 255, 255))
    score = font_of_death.render(f'SCORE: {int(SCORE // 1 + 1)}', False, (255, 255, 255))
    levle = font_of_death.render(f'LEVEL: {level}', False, (255, 255, 255))
    helpp = font_of_death.render('(To quit press esc)', False, (255, 255, 255))
    start_screen = True
    while start_screen:
        start_screen = not pygame.key.get_pressed()[pygame.K_ESCAPE]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False

        disp.fill((0, 0, 0))
        disp.blit(surrealism, (width // 2 - surrealism.get_width() // 2, 0))
        disp.blit(imfunny, (width // 2 - imfunny.get_width() // 2, 50))
        disp.blit(score, (width // 2 - score.get_width() // 2, 100))
        disp.blit(levle, (width // 2 - levle.get_width() // 2, 150))
        disp.blit(helpp, (width // 2 - helpp.get_width() // 2, 350))
        pygame.display.flip()
    logger('Game ended')
    sys.exit()


class RunningCircle(pygame.sprite.Sprite):
    def __init__(self, group, cords):
        super().__init__(group)
        self.size = 50
        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, (255, 255, 255), (self.size // 2, self.size // 2), self.size // 2)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.actual_x, self.actual_y = self.rect.centerx, self.rect.centery
        self.speed = [120, 120]

    def update(self, *args, **kwargs):
        self.actual_x += self.speed[0] / FPS
        self.actual_y += self.speed[1] / FPS
        self.rect.centerx, self.rect.centery = self.actual_x, self.actual_y
        self.decide_and_bounce()

    def decide_and_bounce(self):
        if self.actual_x - self.size // 2 < 0 or self.actual_x + self.size // 2 > width:
            self.bounce_wall()
        if self.actual_y - self.size // 2 < 0 or self.actual_y + self.size // 2 > height:
            self.bounce_ceiling()
        self.speed = [self.speed[0], self.speed[1]]

    def bounce_wall(self):
        self.speed[0] = -self.speed[0]

    def bounce_ceiling(self):
        self.speed[1] = -self.speed[1]


def middle_screen(player):
    disp = pygame.display.set_mode(screensize)
    pygame.mouse.set_visible(True)
    if player:
        player.rect.x, player.rect.y = (width // 2, 50)
    font_of_death = pygame.font.SysFont('Papyrus', 50)
    surrealism = font_of_death.render(f'Congratulations, you completed level {level}', False, (255, 255, 255))
    ababa = font_of_death.render(f'Click the circle to continue', False, (255, 255, 255))
    start_screen = True

    circl = pygame.sprite.Group()
    sprit = RunningCircle(circl, (width // 2, height // 2))

    mous = pygame.sprite.Sprite()
    mous.image = pygame.Surface((1, 1))
    mous.rect = mous.image.get_rect()
    while start_screen:
        mous.rect.x, mous.rect.y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollideany(mous, circl):
                start_screen = False
        sprit.rect.x += sprit.speed[0] / FPS
        sprit.rect.y += sprit.speed[1] / FPS

        disp.fill((0, 0, 0))
        disp.blit(surrealism, (width // 2 - surrealism.get_width() // 2, 0))
        disp.blit(ababa, (width // 2 - ababa.get_width() // 2, 100))

        circl.draw(disp)
        circl.update()

        pygame.display.flip()
    pygame.mouse.set_visible(False)


def logger(log_message):
    with open('log.txt', 'a') as file:
        file.write(f'{log_message} | [{datetime.datetime.now()}]\n')
    file.close()


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
        Guns.MachineGun(self.gun, all_objects, self, 10, 10, 10, 10)

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
        global SCORE
        if type(self) is MainCharacter:
            logger('Player died')
            ending_screen()

        elif self is AI:
            SCORE += 100
            logger('AI killed')
            logger('player received 100 points')
        pygame.sprite.Sprite.kill(self)
        pygame.sprite.Sprite.kill(self.gun.sprites()[0])

    def fire(self):
        if self.gun.sprites():
            self.gun.sprites()[0].fire(*pygame.mouse.get_pos(), *self.rect.center, 5)


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
        vision_size = (width, 200)
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, my_group, all_objects, cords, sender, size, speed=(10, 0)):
        super().__init__(my_group, all_objects)
        self.all_objects = all_objects
        self.image = pygame.surface.Surface((size, size))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.actual_x, self.actual_y = self.rect.x, self.rect.y
        self.speed = list(speed)
        self.sender = sender
        self.c = 0
        self.bounce = False

    def update(self):
        self.c += 1
        self.actual_x, self.actual_y = self.actual_x + self.speed[0], self.actual_y + self.speed[1]
        self.rect.x, self.rect.y = self.actual_x, self.actual_y
        self.destroy()
        if self.is_outside():
            if self.bounce:
                if 0 < self.rect.y < height:
                    self.speed = [-self.speed[0], self.speed[1]]
                elif 0 < self.rect.x < width:
                    self.speed = [self.speed[0], -self.speed[1]]
            else:
                self.kill()

    def destroy(self):
        collided = pygame.sprite.spritecollide(self, self.all_objects, False)
        for sprite in collided:
            if sprite != self and not isinstance(sprite, Cursor) and not isinstance(sprite, Gun):
                if not isinstance(sprite, Bullet):
                    if sprite == self.sender:
                        return None
                    if isinstance(sprite, AI) or isinstance(sprite, level_contains.Box):
                        sprite.hp -= 1
                        self.kill()
                        return None

                    sprite.kill()
                else:
                    if sprite.sender != self.sender:
                        sprite.kill()
                self.kill()

    def is_outside(self):
        return self.rect.x > width or self.rect.x < 0 or self.rect.y > height or self.rect.y < 0


class Gun(pygame.sprite.Sprite):
    image = None

    def __init__(self, my_group: pygame.sprite.Group, all_objects: pygame.sprite.Group, player, bullet_speed,
                 bullet_size, aim, cooldown):
        super().__init__(my_group, all_objects)
        self.image = self.__class__.image
        self.owner = player
        self.all_objects = all_objects
        self.rect = self.owner.rect.copy()
        self.rect.y += player.image.get_height() // 3
        self.rect.x += player.image.get_width() // 3.5
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.normal_image = self.image
        self.bullets = pygame.sprite.Group()
        self.right = True
        self.c = 0
        self.bullet_vel = bullet_speed
        self.bullet_size = bullet_size
        self.aim = aim
        self.cooldown = cooldown

    def update(self):
        self.c += 1
        self.rect = self.owner.rect.copy()
        self.rect.y += self.owner.image.get_height() // 3
        self.rect.x += self.owner.image.get_width() // 3.5
        self.bullets.update()
        self.bullets.draw(dispy.display)

    def fire(self, target_x, target_y, sender_x, sender_y, number_of_bullets=1):
        if self.c / FPS > self.cooldown:
            for _ in range(number_of_bullets):
                xx = (math.log2((random.random() + 1) * self.aim**2))
                yy = (math.log2((random.random() + 1) * self.aim**2))
                xv = ((target_x - sender_x) / FPS) * xx
                yv = ((target_y - sender_y) / FPS) * yy
                if xv != 0 and yv != 0:
                    mult = math.sqrt(self.bullet_vel**2 / (xv**2 + yv**2))
                else:
                    mult = 1
                speed = (xv * mult, yv * mult)
                cords = (self.owner.rect.center[0] +
                         random.randint(-self.aim, self.aim), self.owner.rect.center[1] +
                         random.randint(-self.aim, self.aim))
                Bullet(self.bullets, self.all_objects, cords, self.owner, self.bullet_size, speed)
                self.c = 1


class Guns:
    class AK47(Gun):
        image = load_image("gun.png")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bullet_vel = 15
            self.cooldown = 0.1
            self.aim = 3
            self.bullet_size = 4

    class EnemyGun(Gun):
        image = load_image("gun.png")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bullet_vel = 5
            self.cooldown = 0.2
            self.aim = 1
            self.bullet_size = 5

    class MachineGun(Gun):
        image = load_image("gun.png")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bullet_vel = 10
            self.cooldown = 0.001
            self.aim = 2
            self.bullet_size = 3


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
        self.hp = 100
        self.start_hp = 100
        self.dc = 0
        self.dead = False

        for sprite in my_group:
            if sprite != self:
                self.other_sprites.add(sprite)

    def update(self):
        if self.hp <= 0:
            self.kill()

        if self.falling:
            self.rect.y += self.y_vel
            self.y_vel += self.display.gravity_c / self.display.fps

            while self._collides_with_border_or_sprites():
                self.rect.y -= 1
                self.y_vel = 0
        if self.hp < self.start_hp // 2:
            self.image = load_image(f'cracked_{self.__class__.__name__}.png')

    def _collides_with_border_or_sprites(self):
        return (pygame.sprite.spritecollideany(self, self.border) or
                pygame.sprite.spritecollideany(self, self.other_sprites))

    def change_image(self, image: pygame.surface.Surface):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def kill(self):
        global SCORE
        SCORE += 50
        logger(f'A {self.__class__.__name__} died T_T')
        logger('Player received 50 points')
        super().kill()


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


class level_contains:
    class Platform(Box):
        image = load_image('platform.png')

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
            self.hp = 100
            self.start_hp = 100
            self.dc = 0
            self.dead = False

            for sprite in my_group:
                if sprite != self:
                    self.other_sprites.add(sprite)


class player_and_ai:
    class MainCharacter(pygame.sprite.Sprite):
        image = load_image('charly.png')

        def __init__(self, my_group: pygame.sprite.Group, all_objects: pygame.sprite.Group, cords: tuple,
                     display: Display,
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
            Guns.MachineGun(self.gun, all_objects, self, 10, 10, 10, 10)

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
            global SCORE
            if type(self) is MainCharacter:
                logger('Player died')
                ending_screen()

            elif self is AI:
                SCORE += 100
                logger('AI killed')
                logger('player received 100 points')
            pygame.sprite.Sprite.kill(self)
            pygame.sprite.Sprite.kill(self.gun.sprites()[0])

        def fire(self):
            if self.gun.sprites():
                self.gun.sprites()[0].fire(*pygame.mouse.get_pos(), *self.rect.center, 5)

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
            if ((self.rect.x - self.player.rect.x) ** 2 + (self.rect.y - self.player.rect.y) ** 2) ** 0.5 > 20:
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
            vision_size = (width, 200)
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


if __name__ == '__main__':
    starting_screen()
    running = True

    clock = pygame.time.Clock()

    all_objects = pygame.sprite.Group()

    main_sprite = BetterGroup()

    other_sprites = BetterGroup()

    enemies = BetterGroup()

    border_sprites = pygame.sprite.Group()
    vert, horiz = pygame.sprite.Group(), pygame.sprite.Group()
    width, height = dispy.size

    mouse_g = pygame.sprite.Group()
    cursor = Cursor(mouse_g, all_objects, (0, 0))
    pygame.mouse.set_visible(False)

    character = MainCharacter(main_sprite, all_objects, (width // 2, 50), dispy, (vert, horiz), other_sprites)

    svp = Platform(other_sprites, all_objects, character.rect.x - 50, character.rect.y + 35, dispy, border_sprites,
                   False)
    svp.hp = 2**2**10
    image = pygame.transform.scale(svp.image, (svp.rect.width * 2, svp.rect.height))
    svp.change_image(image)

    character.jumping = True

    Border(0, height - 1, width, height - 1, border_sprites, vert, horiz)
    Border(-1, 0, -1, height, border_sprites, vert, horiz)
    Border(width, 0, width, height, border_sprites, vert, horiz)

    other_sprites.add(vert)

    particles_group = pygame.sprite.Group()

    movement_coeff = 1
    font_of_score = pygame.font.SysFont('8-bit', 30)

    generate_level((other_sprites, all_objects, border_sprites), level_contains, player_and_ai, (vert, horiz),
                   character, main_sprite, enemies,
                   level)
    while running:
        # print(character.rect.x, character.rect.y)
        screen.fill((255, 255, 255))

        keys = pygame.key.get_pressed()
        if pygame.mouse.get_focused():
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
        if keys[pygame.K_d]:
            character.move(2, movement_coeff)
        if keys[pygame.K_s]:
            character.move(3, movement_coeff)
        if keys[pygame.K_a]:
            character.move(4, movement_coeff)
        if keys[pygame.K_SPACE]:
            if not character.jumping:
                character.move(1, movement_coeff)
                character.jumping = True

        if pygame.mouse.get_pressed()[0]:
            character.fire()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    for i in range(10):
                        AI(enemies, all_objects, pygame.mouse.get_pos(), dispy, (vert, horiz), other_sprites,
                           player=character,
                           player_group=main_sprite)

                elif pygame.mouse.get_pressed()[1]:
                    Platform(other_sprites, all_objects, *pygame.mouse.get_pos(), dispy, border_sprites, False)

        enemies.update(cursor)
        enemies.draw(dispy.display)

        other_sprites.draw(dispy.display)
        other_sprites.update()

        main_sprite.update(cursor)
        main_sprite.draw(dispy.display)

        mouse_g.draw(dispy.display)
        mouse_g.update()

        particles_group.update()
        particles_group.draw(dispy.display)

        if not enemies.sprites() and level > 0:
            middle_screen(character)
            level += 1
            generate_level((other_sprites, all_objects, border_sprites), level_contains, player_and_ai, (vert, horiz),
                           character, main_sprite, enemies,
                           level)

        font_suffer = font_of_score.render("SCORE: " + str(int(SCORE // 1 + 1)), True, (0, 0, 0))
        dispy.display.blit(font_suffer, (0, 0))

        font_surfer = font_of_score.render("FPS: " + str(int(round(clock.get_fps()))), True, (0, 0, 0))
        dispy.display.blit(font_surfer, (0, 30))

        font_surfer = font_of_score.render("LEVEL: " + str(level), True, (0, 0, 0))
        dispy.display.blit(font_surfer, (0, 60))

        pygame.display.flip()
        clock.tick(FPS)
        SCORE += 10 / FPS
