import time
from typing import Dict

import pygame  # type: ignore
from ann.helpers.general_ann_helpers import update_generation  # type: ignore

from reflexy.constants import (
    CAPTION,
    CLOCK_TICK_GAME_SPEED,
    CLOCK_TICK_REFERENCE,
    COOLDOWN_PLAYER_IMMUNE,
    MAX_SPAWN_SPIDER,
    SCORE_FONT,
    SCORE_FONT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_WIDTH_AI,
    TIME_SPAWN_SPIDER,
)
from reflexy.helpers.general_helpers import create_text, exit_game, get_image_path, get_sound_path
from reflexy.menus.elements import keyboard_keys
from reflexy.models.laser_spider import LaserSpider
from reflexy.models.player import Player


class Runner:
    def __init__(
        self,
        volume: Dict[str, float],
        screen=None,
        autonomous=False,
        training=False,
        show_vision=False,
        allow_restart=True,
        channels=[0],
        W_player_matrix=None,
        b_player_matrix=None,
    ):
        self.autonomous = autonomous
        self.training = training
        self.show_vision = show_vision
        self.all_channels = channels.copy()
        self.live_channels = channels.copy()
        self.started = False
        self.exit = False

        pygame.init()

        if training:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH + SCREEN_WIDTH_AI, SCREEN_HEIGHT))
            pygame.display.set_caption("Training", CAPTION)
        elif screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(CAPTION)
        else:
            self.screen = screen

        self.clock = pygame.time.Clock()
        self.background = self.create_background("background-field.png")

        self.volume = volume

        self.time_reference = time.time()
        self.time_display = self.time_reference - self.time_reference
        self.time = self.time_reference
        self.last_time = self.time
        self.time_game()
        self.play_bg_sound(volume=volume["master"] * volume["music"])

        self.allow_restart = allow_restart

        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.laser_draw_group = pygame.sprite.Group()
        self.laser_hit_group = pygame.sprite.Group()
        self.effect_group = pygame.sprite.Group()

        [
            self.player_group.add(
                Player(
                    screen=self.screen,
                    time=self.time,
                    volume=(self.volume["master"] * self.volume["effects"]),
                    autonomous=self.autonomous if channel == 0 else True,
                    show_vision=self.show_vision,
                    channel=channel,
                    W=W_player_matrix,
                    b=b_player_matrix,
                )
            )
            for channel in self.live_channels
        ]
        self.channel_stats = {}
        for channel in self.live_channels:
            self.channel_stats[channel] = {
                "player_hit": False,
                "cd_player_hit": 0,
                "cd_spawn_spider": self.time,
                "high_score": 0,
                "time_display": self.time_display,
            }

    @staticmethod
    def create_background(bg_image: str) -> pygame.surface.Surface:
        """Create the background surface of the window.

        Keyword arguments:
        bg_image -- name of background image
        """
        if bg_image is None:
            raise TypeError("Missing bg_image argument.")
        elif not isinstance(bg_image, str):
            raise TypeError("background image name must be a string." + f" Got {type(bg_image)}.")

        bg = pygame.image.load(get_image_path(bg_image))

        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def time_game(self):
        """Clock of the game."""
        self.time = (
            self.time
            + (time.time() - self.last_time) * CLOCK_TICK_GAME_SPEED / CLOCK_TICK_REFERENCE
        )
        self.time_display = round(self.time - self.time_reference, 1)
        self.last_time = time.time()

    def play_bg_sound(self, volume: float):
        sound_path = get_sound_path("BG.wav")
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.play(-1)
        self.sound.set_volume(volume)

    def has_collision(self, channel: int) -> bool:
        """Check collisions in each frame, for a passing channel."""
        for player in self.player_group.sprites():
            if player.attacking:
                for enemy in self.enemy_group.sprites():
                    if pygame.sprite.collide_mask(
                        enemy,
                        player,
                    ) and ((enemy.channel == player.channel) and (enemy.channel == channel)):
                        self.kill_spider(enemy)
                        player.score += 1

                return False

        for enemy in self.enemy_group.sprites():
            for laser in self.laser_hit_group.sprites():
                if (
                    pygame.sprite.collide_mask(
                        enemy,
                        laser,
                    )
                    and enemy.id != laser.id
                    and enemy.channel == laser.channel
                ):
                    self.kill_spider(enemy)
                    player.score += 1

        bool_collision = any(
            [
                pygame.sprite.collide_mask(
                    enemy,
                    player,
                )
                for enemy in self.enemy_group.sprites()
                for player in self.player_group.sprites()
                if enemy.channel == player.channel and enemy.channel == channel
            ]
        )

        return bool_collision

    def has_hit(self, channel) -> bool:
        """Check if has hit in each frame."""
        for enemy in self.enemy_group.sprites():
            if enemy.ray:
                if enemy.ray not in self.enemy_group.sprites():
                    self.laser_draw_group.add(enemy.ray)

                if enemy.ray not in self.enemy_group.sprites() and (
                    int(enemy.ray.current_image) >= 5
                ):
                    self.laser_hit_group.add(enemy.ray)

        # bool_hit = bool(
        #     pygame.sprite.groupcollide(
        #         self.laser_hit_group,
        #         self.player_group,
        #         False,
        #         False,
        #         pygame.sprite.collide_mask,  # type: ignore
        #     )
        # )

        bool_hit = any(
            [
                pygame.sprite.collide_mask(
                    laser,
                    player,
                )
                for laser in self.laser_hit_group.sprites()
                for player in self.player_group.sprites()
                if laser.channel == player.channel and laser.channel == channel
            ]
        )

        return bool_hit

    def hp(self):
        """Update player's lives and blinking state."""
        if self.enemy_group.sprites():
            for channel in self.live_channels:
                for player in self.player_group.sprites():
                    if player.channel != channel:
                        continue

                    if (
                        self.has_collision(channel) or self.has_hit(channel)
                    ) and not self.channel_stats[channel]["player_hit"]:
                        player.hp -= 1
                        self.channel_stats[channel]["player_hit"] = True
                        self.channel_stats[channel]["cd_player_hit"] = self.time

                        if player.hp <= 0:
                            self.clear_channel(channel)
                            player.dead = True
                        else:
                            player.set_spawn()
                            player.dead = True

                    if player.dead:
                        player.blink_damage()

                    if (
                        self.channel_stats[channel]["player_hit"]
                        and self.time - self.channel_stats[channel]["cd_player_hit"]
                        > COOLDOWN_PLAYER_IMMUNE
                    ):
                        player.dead = False
                        player.blinking_damage = False
                        self.channel_stats[channel]["player_hit"] = False
                        player.blinking_damage = 0

    def respawn_spider(self, channel: int):
        """Add a Spider."""
        self.enemy_group.add(
            LaserSpider(
                screen=self.screen,
                time=self.time,
                volume=(self.volume["master"] * self.volume["effects"]),
                autonomous=False,
                show_vision=self.show_vision,
                channel=channel,
            )
        )

    def kill_spider(self, sprite: pygame.sprite.Sprite):
        """Remove killed spider sprite."""

        if sprite is None:
            raise TypeError("Missing sprite argument.")

        if sprite.ray:  # type: ignore
            sprite.ray.kill()  # type: ignore
            sprite.ray  # type: ignore

        sprite.kill()  # type: ignore

    def clear_channel(self, channel):
        """Clear channel."""
        for enemy in self.enemy_group.sprites():
            if enemy.channel == channel:
                self.kill_spider(enemy)

        for player in self.player_group.sprites():
            if player.channel == channel:
                self.channel_stats[channel]["high_score"] = player.score
                player.kill()

        self.channel_stats[channel]["time_display"] = self.time_display
        try:
            self.live_channels.remove(channel)
        except ValueError:
            pass

    def check_events(self):
        """Check game events in each frame."""
        for channel in self.live_channels:
            if (
                self.time - self.channel_stats[channel]["cd_spawn_spider"] > TIME_SPAWN_SPIDER
                and (len(self.enemy_group) + 1) <= MAX_SPAWN_SPIDER
            ):
                self.respawn_spider(channel)
                self.channel_stats[channel]["cd_spawn_spider"] = self.time

            for player in self.player_group.sprites():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game()

                    if event.type == pygame.KEYDOWN:
                        player.key_down(event.key)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_ESCAPE:
                            if self.autonomous:
                                self.exit = True
                            else:
                                exit_game()

                        if event.key == pygame.K_SPACE:
                            player.attack()

                        player.key_up(event.key)

    def update_score_lives(self):
        """Update player's lives and score."""
        create_text(
            self.screen,
            "Lives = " + str([player.hp for player in self.player_group.sprites()][0]),
            (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 8),
            size=SCORE_FONT_SIZE,
            font_name=SCORE_FONT,
        )
        create_text(
            self.screen,
            str([player.score for player in self.player_group.sprites()][0]),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8),
            size=SCORE_FONT_SIZE,
            font_name=SCORE_FONT,
        )
        create_text(
            self.screen,
            f"Time = {str(self.time_display)}",
            (SCREEN_WIDTH - SCREEN_WIDTH // 10, SCREEN_HEIGHT // 8),
            size=SCORE_FONT_SIZE,
            font_name=SCORE_FONT,
        )

    def update_frame(self, generation, pop, max_pop, best_score, keyboard):
        """Draw all elements on the screen."""
        self.screen.blit(self.background, (0, 0))
        self.time_game()

        for group in [
            self.enemy_group,
            self.player_group,
            self.laser_draw_group,
        ]:
            group.draw(self.screen)

        self.enemy_group.update(self.time, self.player_group, self.enemy_group)
        self.player_group.update(self.time, self.enemy_group)
        self.update_score_lives()

        if self.autonomous:
            update_generation(self, generation, pop, max_pop, best_score, keyboard)

        pygame.display.update()

    def run(self, time=None, generation=None, pop=None, max_pop=None, best_score=None):
        """Loop each frame of the game."""
        keyboard = keyboard_keys()
        while sum([player.hp for player in self.player_group.sprites()]) > 0:

            self.clock.tick(CLOCK_TICK_GAME_SPEED)
            self.check_events()
            self.update_frame(generation, pop, max_pop, best_score, keyboard)
            self.hp()

            if self.exit:
                break

            if not (time is None):
                if self.time_display >= time:
                    break

        self.sound.stop()

        if self.autonomous:
            return (
                self.time_display,
                self.player.score,
                self.player.hp,
                self.exit,
            )
