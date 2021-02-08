import pygame
import time
from reflexy.helpers import get_image_path
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    COOLDOWN_SWORD,
    TIME_BLINK,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            self.get_surface(filename)
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

        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

    def update(self):
        self.image = self.images[self.current_image]
        self.move_player()

        self.center = (
            self.rect[0] + PLAYER_WIDTH / 2,
            self.rect[1] + PLAYER_HEIGHT / 2,
        )

        if self.attacking:
            self.attack()

    def set_spawn(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.center = (self.x - PLAYER_WIDTH / 2, self.y - PLAYER_HEIGHT / 2)
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def blink_damage(self):
        if self.count_blinking == 0:
            self.count_blinking = time.time()

        if time.time() - self.count_blinking > TIME_BLINK:
            self.blinking_damage = not self.blinking_damage
            self.count_blinking = time.time()

            if self.blinking_damage:
                self.image = self.get_surface("player-w-sword-damage.png")

    def attack(self):
        if self.attacking or time.time() - self.cd_attack > COOLDOWN_SWORD:
            self.attacking = True
            self.current_image += 1

            if self.current_image > len(self.images) - 1:
                self.current_image = 0
                self.attacking = False
                self.cd_attack = time.time()

            self.image = self.images[self.current_image]

    def move_player(self):
        if self.moveDown and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.top += PLAYER_SPEED
        if self.moveUp and self.rect.top > -18:
            self.rect.top -= PLAYER_SPEED
        if self.moveLeft and self.rect.left > -30:
            self.rect.left -= PLAYER_SPEED
        if self.moveRight and self.rect.right < SCREEN_WIDTH:
            self.rect.right += PLAYER_SPEED

    def get_surface(self, filename, angle=0, scale=1.2):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
