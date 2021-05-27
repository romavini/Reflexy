import math
import pygame
import random
from typing import Sequence, Optional
from reflexy.helpers import (
    get_surface,
    get_image_path,
    calc_acceleration,
)
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPIDER_SPEED,
    SPIDER_WIDTH,
    SPIDER_HEIGHT,
    SPIDER_EYE_X,
    SPIDER_EYE_Y,
    SPIDER_ACCELERATION,
    SPIDER_ACCELERATION_FUNC,
    SPIDER_DECELERATION,
    SPIDER_DECELERATION_FUNC,
    COOLDOWN_SPIDER_FIRE,
    RAY_ANIMATION_TIME,
)
from reflexy.models.ray import Ray
from reflexy.logic.brain import SpiderBrain


class LaserSpider(pygame.sprite.Sprite):
    def __init__(self, time: Optional[int]):
        if time is None:
            raise TypeError("Missing argument.")
        elif not (isinstance(time, int) or isinstance(time, float)):
            raise TypeError(f"Timemust be float or integer. Got {type(time)}.")

        pygame.sprite.Sprite.__init__(self)

        self.brain = SpiderBrain()

        self.time = time

        self.images = [get_surface(filename) for filename in ("laser-spider.png",)]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.spawn_spider()
        self.eye_aim = (self.rect[0], self.rect[1])

        self.firing = False
        self.cooldown_spider_fire = True
        self.cd_tracker = self.time
        self.cd_init_fire = None
        self.ray = None
        self.speed = 0
        self.acc_tracker = None

        self.x_correction = None
        self.y_correction = None

        self.state_of_movement = "accelerating"

    def aim(self, player_center_coordinates: Sequence[int]):
        """Aim system.

        Keyword arguments:
        player_center_coordinates -- Sequence of player's center coordinates
        """
        if player_center_coordinates is None:
            raise TypeError("Missing argument.")
        elif not (
            isinstance(player_center_coordinates, list)
            or isinstance(player_center_coordinates, tuple)
        ):
            raise TypeError(
                f"player_center_coordinates must be list or tuple. Got {type(player_center_coordinates)}."
            )

        x_aim = int(self.eye_aim[0] + SPIDER_EYE_X - player_center_coordinates[0])
        y_aim = int(self.eye_aim[1] + SPIDER_EYE_Y - player_center_coordinates[1])
        self.aim_angle_rad = math.atan2(y_aim, -x_aim)

    def update(  # type: ignore
        self,
        screen: pygame.Surface,
        player_center_coordinates: Sequence[int],
        time: int,
    ):
        """Update spider

        Keyword arguments:
        screen -- surface to print
        player_center_coordinates -- Sequence of player's center coordinates
        time -- current game time
        """
        arguments = [screen, player_center_coordinates, time]
        if None in arguments:
            raise TypeError("Missing argument.")

        self.time = time

        self.set_velocity()
        self.set_state_of_movement()

        self.eye_aim = (self.rect[0], self.rect[1])

        if not self.state_of_movement == "recoil":
            self.aim(player_center_coordinates)

        self.move_spider()

        if not self.firing and self.state_of_movement == "stoped":
            self.firing = True
        elif not self.firing and self.time - self.cd_tracker > COOLDOWN_SPIDER_FIRE:
            self.state_of_movement = "decelerating"

        if self.firing:
            if self.state_of_movement == "stoped":
                self.state_of_movement = "recoil"

            if not self.cd_init_fire:
                self.call_ray(screen, player_center_coordinates)
                self.cd_init_fire = self.time

            elif self.time - self.cd_init_fire < RAY_ANIMATION_TIME:
                self.ray.next_sprite(
                    screen,
                    self.rect[0] - self.x_correction,
                    self.rect[1] - self.y_correction,
                )

            else:
                self.state_of_movement = "accelerating"
                self.cd_tracker = self.time
                self.firing = False
                self.cd_init_fire = None
                self.acc_tracker = None
                self.x_correction = None
                self.y_correction = None
                self.ray.kill()
                self.ray = None

    def set_velocity(self):
        """ Set velocity."""
        if self.state_of_movement == "accelerating" and self.speed < SPIDER_SPEED:
            if not self.acc_tracker:
                self.acc_tracker = self.time

            self.speed = (
                calc_acceleration(
                    SPIDER_ACCELERATION_FUNC,
                    self.time,
                    self.acc_tracker,
                    SPIDER_ACCELERATION,
                )
                * SPIDER_SPEED
            )

        elif self.state_of_movement == "decelerating":
            if not self.acc_tracker:
                self.acc_tracker = self.time

            self.speed = (
                1
                - calc_acceleration(
                    SPIDER_DECELERATION_FUNC,
                    self.time,
                    self.acc_tracker,
                    SPIDER_DECELERATION,
                )
            ) * SPIDER_SPEED

        elif self.state_of_movement == "recoil":
            if not self.acc_tracker:
                self.acc_tracker = self.time

            if not self.x_correction or not self.y_correction:
                self.x_correction = self.rect[0]
                self.y_correction = self.rect[1]

            if self.time - self.acc_tracker < RAY_ANIMATION_TIME:
                self.speed = -(
                    calc_acceleration(
                        "exp",
                        self.time,
                        self.acc_tracker,
                        RAY_ANIMATION_TIME * 0.8,
                    )
                    * SPIDER_SPEED
                    * 2
                )

    def set_state_of_movement(self):
        """ Set the state of movement."""
        if self.speed > SPIDER_SPEED or self.state_of_movement == "keep":
            self.speed = SPIDER_SPEED
            self.state_of_movement = "keep"
            self.acc_tracker = None

        elif self.state_of_movement == "decelerating" and self.speed <= 0.001:
            self.state_of_movement = "stoped"
            self.speed = 0
            self.acc_tracker = None

    def move_spider(self):
        """Move system"""
        move_through = self.brain.move(self.aim_angle_rad, self.cd_init_fire)
        self.rect[0] += round(math.cos(move_through) * self.speed)
        self.rect[1] -= round(math.sin(move_through) * self.speed)

    def call_ray(
        self, screen: pygame.Surface, player_center_coordinates: Sequence[int]
    ):
        """Shoot laser.

        Keyword arguments:
        screen -- surface to print
        player_center_coordinates -- Sequence of player's center coordinates
        """
        angle = self.brain.shot(
            math.degrees(self.aim_angle_rad),
            self.cd_init_fire,
            self.eye_aim,
            player_center_coordinates,
        )
        self.ray = Ray(
            screen,
            self.eye_aim,
            angle,
            (SPIDER_EYE_X, SPIDER_EYE_Y),
        )

    def spawn_spider(self):
        """spawn the spider sprite in a random position"""
        axis = random.randint(0, 1)
        side = random.randint(0, 1) if axis else random.randint(0, 1)

        if axis:
            if side:
                y = random.randint(0, SCREEN_HEIGHT)
                x = -SPIDER_WIDTH

            else:
                y = random.randint(0, SCREEN_HEIGHT)
                x = SCREEN_WIDTH

        else:
            if side:
                x = random.randint(0, SCREEN_WIDTH)
                y = -SPIDER_HEIGHT

            else:
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT

        self.rect = pygame.Rect(x, y, 128, 64)
