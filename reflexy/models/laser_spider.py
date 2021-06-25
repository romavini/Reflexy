import math
import pygame
import random
from typing import Optional
from reflexy.helpers import (
    aim,
    get_hit_box,
    get_surface,
    calc_acceleration,
    vision,
)
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPIDER_SPEED,
    SPIDER_VISION_RANGE,
    SPIDER_VISION_CHANNELS,
    LAYERS,
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
    SPIDER_OUTPUTS,
)
from reflexy.models.ray import Ray
from reflexy.logic.brain import Brain


class LaserSpider(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: pygame.Surface,
        time: Optional[int],
        autonomous: bool = False,
        show_vision: bool = True,
        W=None,
        b=None,
    ):
        if time is None:
            raise TypeError("Missing argument.")
        elif not (isinstance(time, int) or isinstance(time, float)):
            raise TypeError(f"Timemust be float or integer. Got {type(time)}.")

        pygame.sprite.Sprite.__init__(self)

        self.W = W
        self.b = b

        self.screen = screen
        self.time = time
        self.autonomous = autonomous
        self.show_vision = show_vision
        self.brain = None

        self.images = [
            get_surface(filename) for filename in ("laser-spider.png",)
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.spawn_spider()
        self.eye_aim = (self.rect[0], self.rect[1])

        self.to_fire = True
        self.firing = False
        self.cooldown_spider_fire = True
        self.cd_tracker = self.time
        self.cd_init_fire = None
        self.ray = None
        self.speed = 0
        self.acc_tracker = None

        self.x_correction = None
        self.y_correction = None

        self.hit_box = get_hit_box(self)

        self.state_of_movement = "accelerating"

    def update(  # type: ignore
        self,
        time: int,
        player_sprite,
        enemy_group,
    ):
        """Update spider

        Keyword arguments:
        time -- current game time
        player_sprite -- Sequence of player's center coordinates
        """
        arguments = [self.screen, player_sprite.center, time]
        if None in arguments:
            raise TypeError("Missing argument.")

        self.hit_box = get_hit_box(self)

        if self.show_vision or self.autonomous:
            spider_vision = vision(
                self.screen,
                self,
                player_sprite,
                SPIDER_VISION_RANGE,
                self_allies=enemy_group,
                other_has_group=False,
                draw=self.show_vision,
            )

        if self.autonomous and self.brain is None:
            layers = [SPIDER_VISION_CHANNELS]
            layers.extend(LAYERS)
            layers.extend([SPIDER_OUTPUTS])
            if not (self.W is None) and not (self.b is None):
                self.brain = Brain(
                    W=self.W,
                    b=self.b,
                    layers=layers,
                )
            else:
                self.brain = Brain(layers=layers)

        self.time = time
        if self.autonomous and not (self.brain is None):
            [
                self.move_left,
                self.move_right,
                self.move_up,
                self.move_down,
                self.to_fire,
                self.to_angle,
            ] = self.brain.analyze(spider_vision)

            [
                self.move_left,
                self.move_right,
                self.move_up,
                self.move_down,
                self.to_fire,
            ] = self.brain.action_ativation(
                [
                    self.move_left,
                    self.move_right,
                    self.move_up,
                    self.move_down,
                    self.to_fire,
                ]
            )
            if not self.state_of_movement == "recoil":
                self.aim_angle_rad = self.to_angle

        else:
            if not self.state_of_movement == "recoil":
                self.aim_angle_rad = aim(
                    player_sprite.center,
                    self.eye_aim,
                    SPIDER_EYE_X,
                    SPIDER_EYE_Y,
                )

        self.set_velocity()
        self.set_state_of_movement()

        self.eye_aim = (self.rect[0], self.rect[1])

        self.move_spider()
        if (self.to_fire or self.firing) and (
            self.firing or self.time - self.cd_tracker > COOLDOWN_SPIDER_FIRE
        ):
            self.fire(player_sprite)

    def fire(self, player_sprite):
        if not self.firing and self.state_of_movement == "stoped":
            self.firing = True
        elif (
            not self.firing
            and self.time - self.cd_tracker > COOLDOWN_SPIDER_FIRE
        ):
            self.state_of_movement = "decelerating"

        if self.firing:
            if self.state_of_movement == "stoped":
                self.state_of_movement = "recoil"

            if not self.cd_init_fire:
                self.call_ray(self.screen, player_sprite)
                self.cd_init_fire = self.time

            elif self.time - self.cd_init_fire < RAY_ANIMATION_TIME:
                self.ray.next_sprite(
                    self.screen,
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
        """Set velocity."""
        if (
            self.state_of_movement == "accelerating"
            and self.speed < SPIDER_SPEED
        ):
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
        """Set the state of movement."""
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
        if self.autonomous and not (self.brain is None):
            move_through_deg = 0

            if self.move_left and self.move_right:
                if random.randint(0, 1):
                    self.move_left = False
                else:
                    self.move_right = False

            if self.move_up and self.move_down:
                if random.randint(0, 1):
                    self.move_up = False
                else:
                    self.move_down = False

            if self.move_left:
                move_through_deg = 180
                if self.move_up:
                    move_through_deg -= 45
                elif self.move_down:
                    move_through_deg += 45
            elif self.move_left:
                if self.move_up:
                    move_through_deg += 45
                elif self.move_down:
                    move_through_deg -= 45
            elif self.move_up:
                move_through_deg = 90
            elif self.move_down:
                move_through_deg = -90

            if self.state_of_movement == "recoil":
                move_through = self.aim_angle_rad
            else:
                move_through = math.radians(move_through_deg)

            if True in [
                self.move_left,
                self.move_right,
                self.move_up,
                self.move_down,
            ]:
                self.rect[0] += round(math.cos(move_through) * self.speed)
                self.rect[1] -= round(math.sin(move_through) * self.speed)

        else:
            move_through = self.aim_angle_rad
            self.rect[0] += round(math.cos(move_through) * self.speed)
            self.rect[1] -= round(math.sin(move_through) * self.speed)

        if self.rect[0] < -SPIDER_WIDTH:
            self.rect[0] = -SPIDER_WIDTH
        elif self.rect[0] > SCREEN_WIDTH + SPIDER_WIDTH:
            self.rect[0] = SCREEN_WIDTH + SPIDER_WIDTH

        if self.rect[1] < -SPIDER_HEIGHT:
            self.rect[1] = -SPIDER_HEIGHT
        elif self.rect[1] > SCREEN_HEIGHT + SPIDER_HEIGHT:
            self.rect[1] = SCREEN_HEIGHT + SPIDER_HEIGHT

        self.center = (
            self.rect[0] + SPIDER_WIDTH / 2,
            self.rect[1] + SPIDER_HEIGHT / 2,
        )

    def call_ray(self, screen: pygame.Surface, player_sprite):
        """Shoot laser.

        Keyword arguments:
        screen -- surface to print
        player_sprite -- Sequence of player's center coordinates
        """
        angle = math.degrees(self.aim_angle_rad)
        self.ray = Ray(
            screen,
            self.eye_aim,
            angle,
            (SPIDER_EYE_X, SPIDER_EYE_Y),
            self.show_vision,
        )

    def spawn_spider(self):
        """spawn the spider sprite in a random position"""
        axis = ["top", "bot"][random.randint(0, 1)]
        side = ["left", "right"][random.randint(0, 1)]

        if axis == "top":
            if side == "left":
                y = random.randint(0, SCREEN_HEIGHT)
                x = -SPIDER_WIDTH

            elif side == "right":
                y = random.randint(0, SCREEN_HEIGHT)
                x = SCREEN_WIDTH

        elif axis == "bot":
            if side == "left":
                x = random.randint(0, SCREEN_WIDTH)
                y = -SPIDER_HEIGHT

            elif side == "right":
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT

        self.rect = pygame.Rect(x, y, SPIDER_WIDTH, SPIDER_HEIGHT)
        self.center = (
            self.rect[0] + SPIDER_WIDTH / 2,
            self.rect[1] + SPIDER_HEIGHT / 2,
        )
