import pygame
from reflexy.helpers import (
    get_hit_box,
    get_surface,
    calc_acceleration,
    vision,
)
from reflexy.constants import (
    PLAYER_VISION,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    COOLDOWN_PLAYER_SWORD,
    TIME_PLAYER_BLINK,
    PLAYER_ACCELERATION,
    PLAYER_ACCELERATION_FUNC,
    PLAYER_DECELERATION,
    PLAYER_DECELERATION_FUNC,
)
from reflexy.logic.brain import Brain


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: pygame.Surface,
        time: int,
        autonomous: bool = False,
        show_vision: bool = True,
    ):
        if time is None:
            raise TypeError("Missing argument.")
        elif not (isinstance(time, int) or isinstance(time, float)):
            raise TypeError(f"Timemust be float or integer. Got {type(time)}.")

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.time = time
        self.autonomous = autonomous
        self.show_vision = show_vision
        self.brain = None

        self.images = [
            get_surface(filename, scale=1)
            for filename in (
                [
                    "player-w-sword-00.png",
                    "player-w-sword-01.png",
                    "player-w-sword-02.png",
                    "player-w-sword-03.png",
                    "player-w-sword-04.png",
                    "player-w-sword-05.png",
                    "player-w-sword-06.png",
                    "player-w-sword-07.png",
                ]
            )
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.set_spawn()

        self.mouse = pygame.mouse.get_pos()
        self.hp = 3
        self.score = 0

        self.cd_attack = 0

        self.dead = False
        self.blinking_damage = False
        self.count_blinking = 0
        self.attacking = False

        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        self.horizontal_acc = None
        self.vertical_acc = None

        self.speed = 0
        self.current_speed = None
        self.acc_tracker = None
        self.state_of_moviment = "accelerating"
        self.last_state_of_moviment = None

        self.hit_box = get_hit_box(self)

    def update(
        self,
        time: int,
        enemy_group,
    ):
        """Update player.

        Keyword arguments:
        time -- current game time
        """
        if time is None:
            raise TypeError("Missing time argument.")

        self.hit_box = get_hit_box(self)

        if self.show_vision or self.autonomous:
            player_vision = vision(
                self.screen,
                self,
                enemy_group,
                PLAYER_VISION,
                other_has_group=True,
                draw=self.show_vision,
            )

        if self.autonomous and self.brain is None:
            self.brain = Brain(
                layers=[len(player_vision), 100, 5],
            )

        self.time = time
        self.image = self.images[self.current_image]

        self.center = [
            self.rect[0] + PLAYER_WIDTH / 2,
            self.rect[1] + PLAYER_HEIGHT / 2,
        ]

        if self.autonomous and not (self.brain is None):
            [
                self.move_left,
                self.move_right,
                self.move_up,
                self.move_down,
                to_attack,
            ] = self.brain.action_ativation(self.brain.analyze(player_vision))

            if to_attack:
                self.attack()

        self.update_state_of_moviment()
        self.set_velocity()
        self.move_player()

        if self.attacking:
            self.attack()

    def set_spawn(self):
        """Spawn player."""
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.center = (self.x + PLAYER_WIDTH / 2, self.y + PLAYER_HEIGHT / 2)
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def blink_damage(self):
        """Give invulnerability to the player after taking damage."""
        if self.count_blinking == 0:
            self.count_blinking = self.time

        if self.time - self.count_blinking > TIME_PLAYER_BLINK:
            self.blinking_damage = not self.blinking_damage
            self.count_blinking = self.time

            if self.blinking_damage:
                self.image = get_surface("player-w-sword-damage.png", scale=1)

    def attack(self):
        """Sword attack."""
        if self.attacking or self.time - self.cd_attack > COOLDOWN_PLAYER_SWORD:
            self.attacking = True
            self.current_image += 1

            if self.current_image > len(self.images) - 1:
                self.current_image = 0
                self.attacking = False
                self.cd_attack = self.time

            self.image = self.images[self.current_image]

    def update_state_of_moviment(self):
        if (
            True
            in [
                self.move_left,
                self.move_right,
                self.move_up,
                self.move_down,
            ]
            and self.state_of_moviment in ["stoped", "decelerating"]
        ):
            self.state_of_moviment = "accelerating"

        if True not in [
            self.move_left,
            self.move_right,
            self.move_up,
            self.move_down,
        ]:
            self.state_of_moviment = "decelerating"

    def keydown(self, key):
        """key system

        Keyword arguments:
        key -- key pressed
        """
        if key is None:
            raise TypeError("Missing time argument.")

        if key == pygame.K_LEFT or key == pygame.K_a:
            self.move_right = False
            self.move_left = True
            self.horizontal_acc = "left"
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.move_left = False
            self.move_right = True
            self.horizontal_acc = "right"

        if key == pygame.K_UP or key == pygame.K_w:
            self.move_down = False
            self.move_up = True
            self.vertical_acc = "up"
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.move_up = False
            self.move_down = True
            self.vertical_acc = "down"

        self.update_state_of_moviment()

    def keyup(self, key):
        """key system

        Keyword arguments:
        key -- key released
        """
        if key is None:
            raise TypeError("Missing time argument.")

        if key == pygame.K_LEFT or key == pygame.K_a:
            self.move_left = False
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.move_right = False

        if key == pygame.K_UP or key == pygame.K_w:
            self.move_up = False
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.move_down = False

        self.update_state_of_moviment()

    def set_velocity(self):
        """Acceleration system, set the state of movement."""
        if not (self.move_up or self.move_down) and (self.move_left or self.move_right):
            self.vertical_acc = None

        if not (self.move_left or self.move_right) and (self.move_up or self.move_down):
            self.horizontal_acc = None

        if self.state_of_moviment == "accelerating" and self.speed < PLAYER_SPEED:
            if not self.acc_tracker or self.last_state_of_moviment == "decelerating":
                self.acc_tracker = self.time

            if not self.speed:
                self.current_speed = PLAYER_SPEED

            elif self.speed != PLAYER_SPEED and self.current_speed is None:
                self.current_speed = self.speed

            elif self.current_speed is None:
                self.current_speed = PLAYER_SPEED

            self.speed = (
                calc_acceleration(
                    PLAYER_ACCELERATION_FUNC,
                    self.time,
                    self.acc_tracker,
                    PLAYER_ACCELERATION,
                )
                * self.current_speed
            )

            self.last_state_of_moviment = "accelerating"

        if self.speed > PLAYER_SPEED or self.state_of_moviment == "keep":
            self.speed = PLAYER_SPEED
            self.state_of_moviment = "keep"
            self.acc_tracker = None
            self.current_speed = None
            self.last_state_of_moviment = "keep"

        elif self.state_of_moviment == "decelerating":
            if not self.acc_tracker or self.last_state_of_moviment == "accelerating":
                self.acc_tracker = self.time

            if self.speed != PLAYER_SPEED and self.current_speed is None:
                self.current_speed = self.speed
            elif self.current_speed is None:
                self.current_speed = PLAYER_SPEED

            self.speed = (
                1
                - calc_acceleration(
                    PLAYER_DECELERATION_FUNC,
                    self.time,
                    self.acc_tracker,
                    PLAYER_DECELERATION,
                )
            ) * self.current_speed

            self.last_state_of_moviment = "decelerating"

        if self.speed < 0 and self.state_of_moviment == "decelerating":
            self.state_of_moviment = "stoped"
            self.speed = 0
            self.acc_tracker = None
            self.current_speed = None
            self.horizontal_acc = None
            self.vertical_acc = None
            self.last_state_of_moviment = "stoped"

    def move_player(self):
        """Movement system."""
        if self.rect.bottom < SCREEN_HEIGHT and (
            self.move_down
            or (
                self.state_of_moviment == "decelerating" and self.vertical_acc == "down"
            )
        ):
            self.rect.top += self.speed

        if self.rect.top > -18 and (
            self.move_up
            or (self.state_of_moviment == "decelerating" and self.vertical_acc == "up")
        ):
            self.rect.top -= self.speed

        if self.rect.left > -30 and (
            self.move_left
            or (
                self.state_of_moviment == "decelerating"
                and self.horizontal_acc == "left"
            )
        ):
            self.rect.left -= self.speed

        if self.rect.right < SCREEN_WIDTH and (
            self.move_right
            or (
                self.state_of_moviment == "decelerating"
                and self.horizontal_acc == "right"
            )
        ):
            self.rect.right += self.speed
