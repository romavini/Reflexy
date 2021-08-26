from reflexy.runner import Runner
from reflexy.menus.elements import createButton
import sys
import time
import pygame
from reflexy.helpers.general import create_text, exit_game
from reflexy.constants import (
    CAPTION,
    CLOCK_TICK_GAME_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_WIDTH_AI,
)


def restart(runner, allow_restart=True):
    """Draw the restart screen.

    Keyword arguments
    runner -- Screen to print
    allow_restart -- bool value (default True)
    """
    if not allow_restart:
        exit_game()

    restart_game = False

    runner.screen.fill((0, 0, 0))

    while not restart_game:
        runner.clock.tick(CLOCK_TICK_GAME_SPEED)
        runner.screen.blit(runner.background, (0, 0))
        create_text(
            runner.screen,
            "You Died! Press R to restart",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            size=26,
        )
        create_text(
            runner.screen,
            f"Score: {runner.player.score}",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5),
            size=26,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game = True
                if event.key == pygame.K_ESCAPE:
                    exit_game()

        pygame.display.update()

    runner = Runner(autonomous=False, show_vision=True, allow_restart=True)
    runner.run()


def in_game_menu():
    """"""
    pass


def create_screen():
    """"""
    screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_WIDTH_AI, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    bgcolor = (25, 25, 50)
    screen.fill(bgcolor)
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


def main_menu():
    """"""
    pygame.init()
    screen, clock = create_screen()

    play_button = createButton("Play", "play", (200, 100), (160, 60))
    settings_button = createButton("Settings", "settings", (200, 200), (160, 60))
    ai_button = createButton("AI", "ai", (200, 300), (160, 60))
    quit_button = createButton("Quit", "quit", (200, 400), (160, 60))
    main_menu_buttons = [
        play_button,
        settings_button,
        ai_button,
        quit_button,
    ]

    while True:
        check_events(screen, main_menu_buttons)

        pygame.display.update()
