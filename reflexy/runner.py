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

    def handle_keys(self, player):
        """ Handles Keys """

        if pygame.key.get_pressed()[pygame.K_DOWN]: # down key
            player.rect[1] += PLAYER_SPEED # move down

        elif pygame.key.get_pressed()[pygame.K_UP]: # up key
            player.rect[1] -= PLAYER_SPEED # move up

        if pygame.key.get_pressed()[pygame.K_RIGHT]: # right key
            player.rect[0] += PLAYER_SPEED # move right

        elif pygame.key.get_pressed()[pygame.K_LEFT]: # left key
            player.rect[0] -= PLAYER_SPEED # move left


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

        pygame.draw.circle(
            self.screen,
            pygame.Color(0, 64, 64, 64),
            (
                self.enemy_group.sprites()[0].rect.center[0],
                self.enemy_group.sprites()[0].rect.center[1] - 9,
            ),
            SPIDER_VISION,
            1,
        )
        pygame.draw.line(
            self.screen,
            pygame.Color("black"),
            (
                self.enemy_group.sprites()[0].rect.center[0],
                self.enemy_group.sprites()[0].rect.center[1] - 9,
            ),
            (50, 50),
            1,
        )

        self.laser_group.update()
        for group in self.laser_group:
            self.laser_group.image = group.blitRotate(
                self.screen,
                group.image,
                (group.rect[0], group.rect[1]),
                (group.rect[2] / 2, group.rect[3] / 2),
                group.current_angle,
            )

        self.enemy_group.update(self.screen)
        self.player_group.update()

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
