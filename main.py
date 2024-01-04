from tech import dispy, BetterGroup, Cursor, FPS, screen, play_music
from level_contains import Platform, Box, Border
from player_and_ai import MainCharacter, AI
import pygame

if __name__ == '__main__':
    running = True

    clock = pygame.time.Clock()

    gravipopa = []

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

    character = MainCharacter(main_sprite, all_objects, (width // 2, height // 2), dispy, (vert, horiz), other_sprites)
    character.jumping = True

    Platform(other_sprites, all_objects, 450, 0, dispy, border_sprites, True)
    Platform(other_sprites, all_objects, 300, 550, dispy, border_sprites, False)
    Box(other_sprites, all_objects, 200, 350, dispy, border_sprites, True)

    Border(0, height - 1, width, height - 1, border_sprites, vert, horiz)
    Border(-1, 0, -1, height, border_sprites, vert, horiz)
    Border(width, 0, width, height, border_sprites, vert, horiz)

    other_sprites.add(vert)

    particles_group = pygame.sprite.Group()

    # play_music('Business_Em.mp3', -1)
    # pygame.mixer.music.set_volume(0.1)
    # pygame.mixer.music.set_pos(120)

    movement_coeff = 1

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
                    AI(main_sprite, all_objects, pygame.mouse.get_pos(), dispy, (vert, horiz), other_sprites,
                       player=character,
                       player_group=main_sprite)

        enemies.update(cursor)
        enemies.draw(dispy.display)

        other_sprites.draw(dispy.display)
        other_sprites.update()

        main_sprite.draw(dispy.display)
        main_sprite.update(cursor)

        mouse_g.draw(dispy.display)
        mouse_g.update()

        particles_group.update()
        particles_group.draw(dispy.display)

        for gravipipa in gravipopa:
            gravipipa.render()

        pygame.display.flip()
        clock.tick(FPS)
