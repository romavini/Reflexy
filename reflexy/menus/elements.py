from reflexy.constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_WIDTH_AI,
    TEXT_FONT,
    TEXT_FONT_SIZE,
)


class createButton:
    def __init__(
        self,
        text,
        id,
        button_pos,
        button_width_n_height=(200, 50),
        color_light=(170, 170, 170),
        color_dark=(100, 100, 100),
        text_color=(255, 255, 255),
        text_size=TEXT_FONT_SIZE,
        font_name=TEXT_FONT,
    ):
        """Create a button.

        Keyword arguments
        text -- text displayed
        id -- id of the button
        button_pos -- button position
        button_width_n_height -- (default (200, 50))
        color_light -- (default (170, 170, 170))
        color_dark -- (default (100, 100, 100))
        text_color -- (default (255, 255, 255))
        text_size -- (default 35)
        font_name -- (default "Corbel")
        """
        self.text = text
        self.id = id
        self.button_pos = button_pos
        self.button_width_n_height = button_width_n_height
        self.color_light = color_light
        self.color_dark = color_dark
        self.text_color = text_color
        self.text_size = text_size
        self.font_name = font_name
        self.center_rect = (
            button_pos[0] + button_width_n_height[0] // 2,
            button_pos[1] + button_width_n_height[1] // 2,
        )


def keyboard_keys():
    up_key = createButton(
        "up",
        "up",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 2, SCREEN_HEIGHT // 8 * 6),
        (50, 50),
        color_light=(255, 255, 255),
        color_dark=(255, 0, 0),
        text_color=(0, 0, 0),
    )
    down_key = createButton(
        "down",
        "down",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 2, SCREEN_HEIGHT // 8 * 7),
        (50, 50),
        color_light=(255, 255, 255),
        color_dark=(255, 0, 0),
        text_color=(0, 0, 0),
    )
    right_key = createButton(
        "right",
        "right",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 4 * 3, SCREEN_HEIGHT // 8 * 7),
        (50, 50),
        color_light=(255, 255, 255),
        color_dark=(255, 0, 0),
        text_color=(0, 0, 0),
    )
    left_key = createButton(
        "left",
        "left",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 4, SCREEN_HEIGHT // 8 * 7),
        (50, 50),
        color_light=(255, 255, 255),
        color_dark=(255, 0, 0),
        text_color=(0, 0, 0),
    )
    space_key = createButton(
        "space",
        "space",
        (SCREEN_WIDTH + SCREEN_WIDTH_AI // 5 * 4, SCREEN_HEIGHT // 8 * 6),
        (50, 50),
        color_light=(255, 255, 255),
        color_dark=(255, 0, 0),
        text_color=(0, 0, 0),
    )
    keyboard_keys = [
        up_key,
        down_key,
        right_key,
        left_key,
        space_key,
    ]

    return keyboard_keys
