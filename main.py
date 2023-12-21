from Objects import Ball, screen, dispy, fps, MainCharacter, Border, BetterGroup, Box, AI, Platform, Cursor
from Gravitron import BlackHole
import pygame
import random


if __name__ == '__main__':
    godmod = False
    running = True

    clock = pygame.time.Clock()

    gravipopa = []

    main_sprite = BetterGroup()

    other_sprites = BetterGroup()

    enemies = BetterGroup()

    border_sprites = pygame.sprite.Group()
    vert, horiz = pygame.sprite.Group(), pygame.sprite.Group()
    width, height = dispy.size

    mouse_g = pygame.sprite.Group()
    cursor = Cursor(mouse_g, (0, 0))
    pygame.mouse.set_visible(False)

    character = MainCharacter(main_sprite, (width // 2, height // 2), dispy, (vert, horiz), other_sprites)

    # chaser = AI(enemies, (200, 300), dispy, (vert, horiz), other_sprites, player=character)

    Platform(other_sprites, 450, 0, dispy, border_sprites, True)
    Platform(other_sprites, 300, 550, dispy, border_sprites, False)
    Box(other_sprites, 200, 350, dispy, border_sprites, True)

    Border(0, height - 1, width, height - 1, border_sprites, vert, horiz)
    Border(-1, 0, -1, height, border_sprites, vert, horiz)
    Border(width, 0, width, height, border_sprites, vert, horiz)

    other_sprites.add(vert)

    particles_group = pygame.sprite.Group()

    pygame.mixer.music.load('music/Homicide.mp3')
    pygame.mixer.music.play(-1)


    throw_power = 3
    while running:
        print(character.rect.x, character.rect.y)
        screen.fill((255, 255, 255))

        keys = pygame.key.get_pressed()
        if pygame.mouse.get_focused():
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
        if keys[pygame.K_F8]:
            pass
            # godmod = not godmod
        if keys[pygame.K_d]:
            character.move(2, 1)
        if keys[pygame.K_s]:
            character.move(3, 1)
        if keys[pygame.K_a]:
            character.move(4, 1)
        if keys[pygame.K_SPACE]:
            if not character.jumping:
                character.move(1, 1)
                character.jumping = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # Particles(particles_group, pygame.mouse.get_pos())

            if godmod:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gravipopa.append(BlackHole(pygame.mouse.get_pos(), 6000, 15, dispy))
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_DELETE]:
                        sprites = pygame.sprite.Group()
                        gravipopa = []
                    elif keys[pygame.K_i]:
                        dispy.gravity_direction = 3
                    elif keys[pygame.K_j]:
                        dispy.gravity_direction = 2
                    elif keys[pygame.K_k]:
                        dispy.gravity_direction = 1
                    elif keys[pygame.K_l]:
                        dispy.gravity_direction = 4
                    elif keys[pygame.K_RIGHT]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, fps * throw_power, 0, gravipopa, other_sprites)
                    elif keys[pygame.K_LEFT]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, -fps * throw_power, 0, gravipopa, other_sprites)
                    elif keys[pygame.K_UP]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, 0, -fps * throw_power, gravipopa, other_sprites)
                    elif keys[pygame.K_DOWN]:
                        Ball(dispy, pygame.mouse.get_pos(), 15, 0, fps * throw_power, gravipopa, other_sprites)

                    elif keys[pygame.K_1]:
                        throw_power = 1
                    elif keys[pygame.K_2]:
                        throw_power = 2
                    elif keys[pygame.K_3]:
                        throw_power = 3
                    elif keys[pygame.K_4]:
                        throw_power = 4
                    elif keys[pygame.K_5]:
                        throw_power = 5
                    elif keys[pygame.K_6]:
                        throw_power = 6
                    elif keys[pygame.K_7]:
                        throw_power = 7
                    elif keys[pygame.K_8]:
                        throw_power = 8
                    elif keys[pygame.K_9]:
                        throw_power = 9
                    elif keys[pygame.K_0]:
                        throw_power = 0

        other_sprites.draw(dispy.display)
        other_sprites.update()

        enemies.draw(dispy.display)
        enemies.update(cursor)

        main_sprite.draw(dispy.display)
        main_sprite.update(cursor)

        mouse_g.draw(dispy.display)
        mouse_g.update()

        particles_group.draw(dispy.display)
        particles_group.update()

        for gravipipa in gravipopa:
            gravipipa.render()

        pygame.display.flip()
        clock.tick(fps)
