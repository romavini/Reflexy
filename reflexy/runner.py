import pygame
import os
import time
from typing import List, Tuple, Dict
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAPTION,
    GAME_SPEED,
    CLOCK_TICK,
    FONT_SIZE,
    SPIDER_VISION,
    SPAWN_SPIDER,
    PLAYER_SPEED,
    COOLDOWN_IMMUNE,
)
from reflexy.helpers import get_image_path, create_pygame_font
from reflexy.models.player import Player
from reflexy.models.laser_spider import LaserSpider
from reflexy.main import start


class Runner:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.clock = pygame.time.Clock()
        self.background = self.create_background()

        self.text = create_pygame_font(FONT_SIZE, bold=True)

        self.allow_restart = False

        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()

        self.player = Player()
        self.enemy_group.add(LaserSpider())
        self.player_group.add(self.player)
        self.player_hit = False
        self.cd_player_hit = 0
        self.cd_spawn_spider = time.time()

    @staticmethod
    def create_background():
        bg = pygame.image.load(get_image_path("background-field.png"))
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_text(self, text):
        return self.text.render(text, True, (255, 255, 255))

    def has_collision(self):
        if self.player.attacking:
            [
                self.kill_spider(sprite)
                for sprite in self.enemy_group.sprites()
                if pygame.sprite.spritecollide(
                    sprite,
                    self.player_group,
                    False,
                    pygame.sprite.collide_mask,
                )
            ]

            return False

        return pygame.sprite.groupcollide(
            self.player_group,
            self.enemy_group,
            False,
            False,
            pygame.sprite.collide_mask,
        )

    def has_hit(self):
        # if self.player.attacking:
        #     return False

        for enemy in self.enemy_group.sprites():
            if enemy.ray and enemy.ray not in self.enemy_group.sprites():
                self.laser_group.add(enemy.ray)

        hit = pygame.sprite.groupcollide(
            self.laser_group,
            self.player_group,
            False,
            False,
            pygame.sprite.collide_mask,
        )
        return hit

    def hp(self):
        if self.enemy_group.sprites():
            if (self.has_collision() or self.has_hit()) and not self.player_hit:
                self.player.hp -= 1
                self.player_hit = True
                self.cd_player_hit = time.time()
                self.player.set_spawn()
                self.player.dead = True

            if self.player.dead:
                self.player.blink_damage()

            if self.player_hit and time.time() - self.cd_player_hit > COOLDOWN_IMMUNE:
                self.player.dead = False
                self.player.blinking_damage = False
                self.player_hit = False
                self.player.blinking_damage = 0

    def respawn_spider(self):
        self.enemy_group.add(LaserSpider())

    def kill_spider(self, sprite):
        sprite.kill()
        self.player.score += 1

    def kill_ray(self):
        pass

    def check_events(self):
        if time.time() - self.cd_spawn_spider > SPAWN_SPIDER:
            self.respawn_spider()
            self.cd_spawn_spider = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_SPACE:
                    self.player.attack()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.moveLeft = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.moveRight = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.moveUp = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.moveDown = False

    def update_score(self):
        self.screen.blit(
            self.create_text("Lifes = " + str(self.player.hp)),
            (FONT_SIZE, SCREEN_HEIGHT / 8),
        )
        self.screen.blit(
            self.create_text(str(self.player.score)),
            ((SCREEN_WIDTH - (FONT_SIZE / 2)) / 2, SCREEN_HEIGHT / 8),
        )

    def update_frame(self):
        self.screen.blit(self.background, (0, 0))

        for group in [self.enemy_group, self.player_group]:
            group.draw(self.screen)

        self.enemy_group.update(self.screen, self.player.center)
        self.player_group.update()

        self.kill_ray()
        self.update_score()
        pygame.display.update()


    def restart(self):
        if not self.allow_restart:
            pygame.quit()

        restart_game = False

        self.screen.fill((0,0,0))
        text = self.create_text('You Died! Press R to restart')
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        while not restart_game:
            self.clock.tick(CLOCK_TICK)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game = True

            pygame.display.update()

        start()



    def run(self):
        while self.player.hp > 0:
            self.clock.tick(CLOCK_TICK)
            self.check_events()
            self.update_frame()
            self.hp()

        self.restart()
