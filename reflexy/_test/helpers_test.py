import os
import pygame
import pytest
from reflexy.helpers import (
    get_image_path,
    create_pygame_font,
    calc_acceleration,
)


def test_get_image_path():
    """Test the get_image_path function."""
    # assert get_image_path("") == os.path.normpath(
    #     os.path.join(os.path.dirname(__file__), "../..", "images")
    # )
    pass

def test_create_pygame_font():
    """Assert the type of the font."""
    # pygame.font.init()
    # assert "<class 'pygame.font.Font'>" == str(
    #     type(create_pygame_font(name=None, size=15))
    # )
    pass

def test_calc_acceleration():
    with pytest.raises(TypeError):
        calc_acceleration(0, 0, 0, 0)

    with pytest.raises(TypeError):
        calc_acceleration(0, "0", 0, 0)

    with pytest.raises(TypeError):
        calc_acceleration(0, 0, "0", 0)

    with pytest.raises(TypeError):
        calc_acceleration(0, 0, 0, "0")

    with pytest.raises(ValueError):
        calc_acceleration("0", 0, 0, 0)
