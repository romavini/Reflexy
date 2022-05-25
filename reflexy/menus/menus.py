import pygame  # type: ignore
from reflexy.constants import (
    CAPTION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_WIDTH_AI,
    TITLE_FONT,
    TITLE_FONT_SIZE,
)
from reflexy.helpers.general_helpers import create_text, exit_game, get_sound_path
from reflexy.logic.ai.ai_ga.ga.ga_player import GeneticAlgorithm
from reflexy.menus.elements import createButton
from reflexy.runner import Runner


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
    menu = Menu(runner.volume)

    while True:
        menu.check_events(runner.screen, main_menu_buttons, runner.volume)

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
        high_score = max(
            [runner.channel_stats[channel]["high_score"] for channel in runner.all_channels]
        )
        create_text(
            runner.screen,
            f"Score: {high_score}",
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
    """Return and check a button was clicked

    Keyword arguments:
    button -- button to check
    mouse_pos -- mouse position
    """
    return (
        button.button_pos[0]
        <= mouse_pos[0]
        <= button.button_pos[0] + button.button_width_n_height[0]
        and button.button_pos[1]
        <= mouse_pos[1]
        <= button.button_pos[1] + button.button_width_n_height[1]
    )


class Menu:
    def __init__(self, volume={"master": 1, "music": 1, "effects": 1}):
        pygame.init()
        self.volume = volume
        self.sound_running = False
        self.button_sound_switch = None
        self.screen, self.clock = create_screen()
        self.play_bg_sound()

    def check_events(self, screen, buttons, volume):
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
                            self.sound.stop()
                            runner = Runner(
                                volume=volume,
                                screen=screen,
                                autonomous=True,
                                show_vision=True,
                                allow_restart=False,
                                channels=[0, 1, 2],
                            )
                            while True:
                                runner.run()
                                restart(runner)

                        elif button.id == "ai":
                            self.ai_menu(screen)

                        elif button.id == "settings":
                            self.settings_menu(screen, self.volume)

                        elif button.id == "train":
                            ga = GeneticAlgorithm(screen)
                            ga.run()
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
                    if self.button_sound_switch is None:
                        self.play_button_sound()
                        self.button_sound_switch = button

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
                    if self.button_sound_switch == button:
                        self.button_sound_switch = None

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

    def ai_menu(self, screen):
        """"""
        self.button_sound_switch = None

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

            button_return = self.check_events(screen, ai_menu_buttons, self.volume)

            if button_return:
                self.button_sound_switch = None
                fill_screen(screen)
                break

            pygame.display.update()

    def settings_menu(self, screen, volume):
        """"""
        pass

    def play_button_sound(self):
        sound_path = get_sound_path("menu button 2 sound effect 33505250.wav")
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
        sound.set_volume(self.volume["master"] * self.volume["effects"])

    def play_bg_sound(self):
        if not self.sound_running:
            self.sound_running = True
            sound_path = get_sound_path("BG.wav")
            self.sound = pygame.mixer.Sound(sound_path)
            self.sound.play(-1)

        self.sound.set_volume(self.volume["master"] * self.volume["music"])

    def main_menu(self):
        """"""
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
                self.screen,
                "Reflexy",
                (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 4),
                size=TITLE_FONT_SIZE,
                font_name=TITLE_FONT,
            )

            self.check_events(self.screen, main_menu_buttons, self.volume)

            pygame.display.update()
