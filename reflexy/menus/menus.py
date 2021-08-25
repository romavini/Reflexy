import sys
import pygame
from reflexy.helpers.general import create_text
from reflexy.main import start
from reflexy.constants import (
    CLOCK_TICK_GAME_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


def restart(runner, allow_restart=True):
    """Draw the restart screen.

    Keyword arguments
    runner -- Screen to print
    allow_restart -- bool value (default True)
    """
    if not allow_restart:
        pygame.quit()
        sys.exit()

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
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    start()


def in_game_menu(runner):
    """"""
    pass


def main_menu(runner):
    """"""
    pass
