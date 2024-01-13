from tech import dispy, BetterGroup, Cursor, FPS, screen, generate_level, starting_screen
from level_contains import Platform, Border
import level_contains
import player_and_ai
from player_and_ai import MainCharacter, AI
import pygame
import tech

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
                   tech.level)
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

        if not enemies.sprites() and tech.level > 0:
            tech.middle_screen(character)
            tech.level += 1
            generate_level((other_sprites, all_objects, border_sprites), level_contains, player_and_ai, (vert, horiz),
                           character, main_sprite, enemies,
                           tech.level)

        font_suffer = font_of_score.render("SCORE: " + str(int(tech.SCORE // 1 + 1)), True, (0, 0, 0))
        dispy.display.blit(font_suffer, (0, 0))

        font_surfer = font_of_score.render("FPS: " + str(int(round(clock.get_fps()))), True, (0, 0, 0))
        dispy.display.blit(font_surfer, (0, 30))

        font_surfer = font_of_score.render("LEVEL: " + str(tech.level), True, (0, 0, 0))
        dispy.display.blit(font_surfer, (0, 60))

        pygame.display.flip()
        clock.tick(FPS)
        tech.SCORE += 10 / FPS
