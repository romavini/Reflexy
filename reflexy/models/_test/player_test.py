import pytest
from reflexy.models.player import Player


def test_init():
    with pytest.raises(TypeError):
        player = Player()
    with pytest.raises(TypeError):
        player = Player("0")


def test_update():
    player = Player(time=0)
    with pytest.raises(TypeError):
        player.update()


def test_keydown():
    player = Player(time=0)
    with pytest.raises(TypeError):
        player.keydown()


def test_keyup():
    player = Player(time=0)
    with pytest.raises(TypeError):
        player.keyup()
