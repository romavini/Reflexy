import math
import pygame
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAPTION,
    GAME_SPEED,
    CLOCK_TICK,
    FONT_SIZE,
    SPIDER_VISION,
)
from reflexy.helpers import get_image_path, create_pygame_font
from reflexy.models.player import Player
from reflexy.models.laser_spider import LaserSider
from reflexy.models.ray import Ray
from reflexy.ann.ann import Ann


class Runner:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.clock = pygame.time.Clock()
        self.background = self.create_background()

        self.text = create_pygame_font(FONT_SIZE, bold=True)

        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()

        self.player_group.add(Player())
        self.enemy_group.add(LaserSider())
        self.laser_group.add(Ray())

        self.score = 0

    @staticmethod
    def create_background():
        bg = pygame.image.load(get_image_path("background-field.png"))
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_score_text(self, score):
        return self.text.render(score, True, (255, 255, 255))

    def has_collision(self):
        for group in [self.enemy_group]:
            if pygame.sprite.groupcollide(
                self.player_group, group, False, False, pygame.sprite.collide_mask
            ):
                return True

        return False

    def has_hit(self):
        for group in [self.laser_group]:
            if (
                pygame.sprite.groupcollide(
                    self.player_group, group, False, False, pygame.sprite.collide_mask
                )
                and self.laser_group.sprites()[0].current_image == 3
            ):
                return True

        return False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                for player in self.player_group.sprites():
                    player.down()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                for player in self.player_group.sprites():
                    player.up()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                for player in self.player_group.sprites():
                    player.left()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                for player in self.player_group.sprites():
                    player.right()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for ray in self.laser_group.sprites():
                    ray.animate()

    def update_score(self):
        for player in self.player_group:
            pass

    def update_frame(self):
        self.screen.blit(self.background, (0, 0))

        [direction, aim] = Ann().update(
            self.player_group.sprites()[0].rect.center,
            self.enemy_group.sprites()[0].rect.center,
        )

        pygame.draw.circle(
            self.screen,
            pygame.Color(0, 64, 64, 64),
            (
                self.enemy_group.sprites()[0].rect.center[0],
                self.enemy_group.sprites()[0].rect.center[1],
            ),
            SPIDER_VISION,
            1,
        )

        radar = self.enemy_group.sprites()[0].rect.center
        radar_len = 200
        x = radar[0] + math.cos(math.radians(aim + 90)) * radar_len
        y = radar[1] + math.sin(math.radians(aim + 90)) * radar_len

        # then render the line radar->(x,y)
        pygame.draw.line(self.screen, pygame.Color("black"), radar, (x,y), 1)

        self.enemy_group.update()
        self.laser_group.update(self.enemy_group.sprites()[0].rect.center, aim)
        self.player_group.update

        for group in [self.enemy_group, self.player_group, self.laser_group]:
            group.draw(self.screen)

        self.update_score()

        self.screen.blit(
            self.create_score_text(str(self.score)),
            ((SCREEN_WIDTH - (FONT_SIZE / 2)) / 2, SCREEN_HEIGHT / 8),
        )
        pygame.display.update()

    def run(self):
        while not self.has_collision() and not self.has_hit():
            self.clock.tick(CLOCK_TICK)
            self.check_events()
            self.update_frame()

        pygame.quit()
