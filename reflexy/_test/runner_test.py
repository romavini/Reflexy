import pygame
import pytest
from reflexy.helpers import get_image_path
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from reflexy.runner import Runner


def test_create_background():
    runner = Runner()
    with pytest.raises(TypeError):
        runner.create_background()
    with pytest.raises(TypeError):
        runner.create_background(42)

def test_create_text():
    runner = Runner()
    with pytest.raises(TypeError):
        runner.create_text()
    with pytest.raises(TypeError):
        runner.create_text(42)

def test_kill_spider():
    runner = Runner()
    with pytest.raises(TypeError):
        runner.kill_spider()
