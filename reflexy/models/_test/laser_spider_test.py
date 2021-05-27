from time import time
import pytest
from reflexy.models.laser_spider import LaserSpider


def test_init():
    with pytest.raises(TypeError):
        laserspider = LaserSpider()


def test_aim():
    laserspider = LaserSpider(time=0)
    with pytest.raises(TypeError):
        laserspider.aim()
    with pytest.raises(TypeError):
        laserspider.aim(player_center_coordinates="0")


def test_update():
    laserspider = LaserSpider(time=0)
    with pytest.raises(TypeError):
        laserspider.update()
