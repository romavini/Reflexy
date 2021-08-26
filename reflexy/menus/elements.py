from reflexy.helpers.general import create_text


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
        text_size=35,
        font_name="Corbel",
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
