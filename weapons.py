import math
import random

import level_contains
import tech
import player_and_ai
from tech import load_image
import pygame


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
        self.bullet_gravity()
        if self.is_outside():
            if self.bounce:
                if 0 < self.rect.y < tech.height:
                    self.speed = [-self.speed[0], self.speed[1]]
                elif 0 < self.rect.x < tech.width:
                    self.speed = [self.speed[0], -self.speed[1]]
            else:
                self.kill()

    def bullet_gravity(self):
        self.speed[1] += tech.dispy.gravity_c / tech.FPS**2

    def destroy(self):
        collided = pygame.sprite.spritecollide(self, self.all_objects, False)
        for sprite in collided:
            if sprite != self and not isinstance(sprite, tech.Cursor) and not isinstance(sprite, Gun):
                if not isinstance(sprite, Bullet):
                    if sprite == self.sender:
                        if self.c / tech.FPS < 0.5:
                            return None
                    if isinstance(sprite, player_and_ai.AI) or isinstance(sprite, level_contains.Box):
                        sprite.hp -= 1
                        self.kill()
                        return None

                    sprite.kill()
                else:
                    if sprite.sender != self.sender:
                        sprite.kill()
                self.kill()

    def is_outside(self):
        return self.rect.x > tech.width or self.rect.x < 0 or self.rect.y > tech.height or self.rect.y < 0


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
        self.bullets.draw(tech.dispy.display)

    def fire(self, target_x, target_y, sender_x, sender_y, number_of_bullets=1):
        if self.c / tech.FPS > self.cooldown:
            for _ in range(number_of_bullets):
                xx = (math.log2((random.random() + 1) * self.aim**2))
                yy = (math.log2((random.random() + 1) * self.aim**2))
                xv = ((target_x - sender_x) / tech.FPS) * xx
                yv = ((target_y - sender_y) / tech.FPS) * yy
                mult = math.sqrt(self.bullet_vel / (xv ** 2 + yv ** 2))
                speed = (xv * mult, yv * mult)
                Bullet(self.bullets, self.all_objects, self.owner.rect.center, self.owner, self.bullet_size, speed)
                self.c = 1


class Guns:
    class AK47(Gun):
        image = load_image("gun.png")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bullet_vel = 30
            self.cooldown = 0.1
            self.aim = 3
            self.bullet_size = 4

    class EnemyGun(Gun):
        image = load_image("gun.png")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.bullet_vel = 10
            self.cooldown = 0.2
            self.aim = 1
            self.bullet_size = 5
