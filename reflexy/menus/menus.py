from reflexy.runner import Runner
from reflexy.menus.elements import createButton
import pygame
from reflexy.helpers.general import create_text, exit_game
from reflexy.constants import (
    CAPTION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_WIDTH_AI,
    TITLE_FONT,
    TITLE_FONT_SIZE,
)


def restart(runner, allow_restart=True):
    """Draw the restart screen.

    Keyword arguments
    runner -- Screen to print
    allow_restart -- bool value (default True)
    """
    if not allow_restart:
        exit_game()

    fill_screen(runner.screen)

    play_button = createButton("Play", "play", (100, 100), (160, 60))
    settings_button = createButton("Settings", "settings", (100, 200), (160, 60))
    ai_button = createButton("AI", "ai", (100, 300), (160, 60))
    quit_button = createButton("Quit", "quit", (100, 400), (160, 60))
    main_menu_buttons = [
        play_button,
        settings_button,
        ai_button,
        quit_button,
    ]

    runner.screen.blit(runner.background, (0, 0))

    while True:
        check_events(runner.screen, main_menu_buttons)

        create_text(
            runner.screen,
            "Reflexy",
            (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 4),
            size=TITLE_FONT_SIZE,
            font_name=TITLE_FONT,
        )

        create_text(
            runner.screen,
            "You Died!",
            (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2),
        )
        create_text(
            runner.screen,
            f"Score: {runner.player.score}",
            (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 50),
        )

        pygame.display.update()


def fill_screen(screen):
    """"""
    bgcolor = (25, 25, 50)
    screen.fill(bgcolor)


def create_screen():
    """"""
    screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_WIDTH_AI, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    fill_screen(screen)
    pygame.display.flip()

    return screen, clock


def check_mouse(button, mouse_pos):
    """Return and check a button was clickd

    Keyword arguments:
    button -- bottun to check
    mouse_pos -- mouse posistion
    """

    return (
        button.button_pos[0]
        <= mouse_pos[0]
        <= button.button_pos[0] + button.button_width_n_height[0]
        and button.button_pos[1]
        <= mouse_pos[1]
        <= button.button_pos[1] + button.button_width_n_height[1]
    )


def check_events(screen, buttons):
    """"""
    mouse_pos = pygame.mouse.get_pos()
    button_return = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit_game()

        # checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if check_mouse(button, mouse_pos):
                    if button.id == "play":
                        runner = Runner(
                            autonomous=False, show_vision=True, allow_restart=True
                        )
                        while True:
                            runner.run()
                            restart(runner)

                    elif button.id == "ai":
                        ai_menu(screen)

                    elif button.id == "settings":
                        pass

                    elif button.id == "train":
                        pass

                    elif button.id == "execute":
                        pass

                    elif button.id == "return":
                        button_return = True

                    elif button.id == "quit":
                        exit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit_game()

        for button in buttons:
            if check_mouse(button, mouse_pos):
                pygame.draw.rect(
                    screen,
                    button.color_light,
                    [
                        button.button_pos[0],
                        button.button_pos[1],
                        button.button_width_n_height[0],
                        button.button_width_n_height[1],
                    ],
                )

            else:
                pygame.draw.rect(
                    screen,
                    button.color_dark,
                    [
                        button.button_pos[0],
                        button.button_pos[1],
                        button.button_width_n_height[0],
                        button.button_width_n_height[1],
                    ],
                )

            create_text(
                screen,
                button.text,
                button.center_rect,
                button.text_color,
                button.text_size,
                button.font_name,
            )

    return button_return


def ai_menu(screen):
    """"""
    train_button = createButton("Train", "train", (100, 100), (160, 60))
    execute_button = createButton("Execute", "execute", (100, 200), (160, 60))
    return_button = createButton("Return", "return", (100, 300), (160, 60))
    ai_menu_buttons = [
        train_button,
        execute_button,
        return_button,
    ]
    fill_screen(screen)

    while True:
        create_text(
            screen,
            "Reflexy",
            (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 4),
            size=TITLE_FONT_SIZE,
            font_name=TITLE_FONT,
        )

        button_return = check_events(screen, ai_menu_buttons)

        if button_return:
            fill_screen(screen)
            break

        pygame.display.update()


def main_menu():
    """"""
    pygame.init()
    screen, clock = create_screen()

    play_button = createButton("Play", "play", (100, 100), (160, 60))
    settings_button = createButton("Settings", "settings", (100, 200), (160, 60))
    ai_button = createButton("AI", "ai", (100, 300), (160, 60))
    quit_button = createButton("Quit", "quit", (100, 400), (160, 60))

    main_menu_buttons = [
        play_button,
        settings_button,
        ai_button,
        quit_button,
    ]

    while True:
        create_text(
            screen,
            "Reflexy",
            (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 4),
            size=TITLE_FONT_SIZE,
            font_name=TITLE_FONT,
        )

        check_events(screen, main_menu_buttons)

        pygame.display.update()
