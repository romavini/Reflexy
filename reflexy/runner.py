import pygame
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAPTION,
    GAME_SPEED,
    CLOCK_TICK,
    FONT_SIZE,
    SPIDER_VISION,
    PLAYER_SPEED,
)
from reflexy.helpers import get_image_path, create_pygame_font
from reflexy.models.player import Player
from reflexy.models.laser_spider import LaserSpider
from reflexy.models.bullet import Bullet
from reflexy.logic.brain import brain, calc_angle


class Runner:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.clock = pygame.time.Clock()
        self.background = self.create_background()

        self.text = create_pygame_font(FONT_SIZE, bold=True)
        self.current_angle = 0

        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()

        self.player = Player()
        self.enemy_group.add(LaserSpider())
        self.player_group.add(self.player)

    @staticmethod
    def create_background():
        bg = pygame.image.load(get_image_path("background-field.png"))
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_score_text(self, score):
        return self.text.render(score, True, (255, 255, 255))

    def has_collision(self):
        return pygame.sprite.groupcollide(
            self.player_group,
            self.enemy_group,
            False,
            False,
            pygame.sprite.collide_mask,
        )

    def has_hit(self):
        bullet = self.enemy_group.sprites()[0].bullet

        if not bullet:
            return False

        return (
            pygame.sprite.spritecollide(
                bullet, self.player_group, False, pygame.sprite.collide_mask
            )
            and bullet.current_image == 3
        )

    def handle_keys(self, player):
        """Handles keys."""

        if pygame.key.get_pressed()[pygame.K_DOWN]:  # down key
            player.rect[1] += PLAYER_SPEED  # move down

        elif pygame.key.get_pressed()[pygame.K_UP]:  # up key
            player.rect[1] -= PLAYER_SPEED  # move up

        if pygame.key.get_pressed()[pygame.K_RIGHT]:  # right key
            player.rect[0] += PLAYER_SPEED  # move right

        elif pygame.key.get_pressed()[pygame.K_LEFT]:  # left key
            player.rect[0] -= PLAYER_SPEED  # move left

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Change the keyboard variables.
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moveRight = False
                    self.player.moveLeft = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moveLeft = False
                    self.player.moveRight = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moveDown = False
                    self.player.moveUp = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moveUp = False
                    self.player.moveDown = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moveLeft = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moveRight = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moveUp = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moveDown = False

    def update_score(self):
        pass

    def update_frame(self):
        self.screen.blit(self.background, (0, 0))

        self.laser_group.update()
        for group in self.laser_group:
            self.laser_group.image = group.blitRotate(
                self.screen,
                group.image,
                (group.rect[0], group.rect[1]),
                (group.rect[2] / 2, group.rect[3] / 2),
                group.current_angle,
            )

        self.enemy_group.update(self.screen, self.player.rect)
        self.player_group.update()

        for group in [self.enemy_group, self.player_group, self.laser_group]:
            group.draw(self.screen)

        self.update_score()

        self.screen.blit(
            self.create_score_text(str(self.player.score)),
            ((SCREEN_WIDTH - (FONT_SIZE / 2)) / 2, SCREEN_HEIGHT / 8),
        )
        pygame.display.update()

    def run(self):
        while not self.has_collision() and not self.has_hit():
            self.clock.tick(CLOCK_TICK)
            self.check_events()
            self.update_frame()

        pygame.quit()
