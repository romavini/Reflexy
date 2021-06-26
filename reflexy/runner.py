import pygame
import sys
import time
from reflexy.menus import main_menu, restart
from reflexy.constants import (
    MAX_SPAWN_SPIDER,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAPTION,
    CLOCK_TICK_GAME_SPEED,
    CLOCK_TICK_REFERENCE,
    FONT_SIZE,
    TIME_SPAWN_SPIDER,
    COOLDOWN_PLAYER_IMMUNE,
)
from reflexy.helpers import (
    create_text,
    get_image_path,
    create_pygame_font,
    get_minor_distance,
)
from reflexy.models.player import Player
from reflexy.models.laser_spider import LaserSpider


class Runner:
    def __init__(
        self,
        autonomous=False,
        show_vision=False,
        allow_restart=True,
        W_player_matrix=None,
        b_player_matrix=None,
        W_enemy_matrix=None,
        b_enemy_matrix=None,
    ):
        self.autonomous = autonomous
        self.show_vision = show_vision
        self.W_enemy_matrix = W_enemy_matrix
        self.b_enemy_matrix = b_enemy_matrix
        self.started = False
        self.exit = False

        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.clock = pygame.time.Clock()
        self.background = self.create_background("background-field.png")

        self.time_refence = time.time()
        self.time_display = self.time_refence - self.time_refence
        self.time = self.time_refence
        self.last_time = self.time
        self.time_game()

        self.text = create_pygame_font(size=FONT_SIZE, bold=True)

        self.allow_restart = allow_restart

        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.laser_draw_group = pygame.sprite.Group()
        self.laser_hit_group = pygame.sprite.Group()
        self.effect_group = pygame.sprite.Group()

        self.player = Player(
            self.screen,
            self.time,
            self.autonomous,
            self.show_vision,
            W_player_matrix,
            b_player_matrix,
        )
        self.enemy_group.add(
            LaserSpider(
                self.screen,
                self.time,
                self.autonomous,
                self.show_vision,
                self.W_enemy_matrix,
                self.b_enemy_matrix,
            )
        )
        self.player_group.add(self.player)
        self.player_hit = False
        self.cd_player_hit = 0
        self.cd_spawn_spider = self.time

    @staticmethod
    def create_background(bg_image: str) -> pygame.surface.Surface:
        """Create the background surface of the window.

        Keyword arguments:
        bg_image -- name of background image
        """
        if bg_image is None:
            raise TypeError("Missing bg_image argument.")
        elif not isinstance(bg_image, str):
            raise TypeError(
                "background image name must be a string."
                + f" Got {type(bg_image)}."
            )

        bg = pygame.image.load(get_image_path(bg_image))

        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def time_game(self):
        """Clock of the game."""
        self.time = (
            self.time
            + (time.time() - self.last_time)
            * CLOCK_TICK_GAME_SPEED
            / CLOCK_TICK_REFERENCE
        )
        self.time_display = round(self.time - self.time_refence, 1)
        self.last_time = time.time()

    def has_collision(self) -> bool:
        """Check collisions in each frame."""
        if self.player.attacking:
            [
                self.kill_spider(sprite)
                for sprite in self.enemy_group.sprites()
                if pygame.sprite.spritecollide(
                    sprite,
                    self.player_group,
                    False,
                    pygame.sprite.collide_mask,  # type: ignore
                )
            ]

            return False

        [
            self.kill_spider(sprite)
            for sprite in self.enemy_group.sprites()
            for laser in self.laser_hit_group
            if pygame.sprite.collide_mask(
                sprite,
                laser,
            )
            and sprite.id != laser.id
        ]

        bool_collision = bool(
            pygame.sprite.groupcollide(
                self.player_group,
                self.enemy_group,
                False,
                False,
                pygame.sprite.collide_mask,  # type: ignore
            )
        )

        return bool_collision

    def has_hit(self) -> bool:
        """Check if has hit in each frame."""
        for enemy in self.enemy_group.sprites():
            if enemy.ray:
                if enemy.ray not in self.enemy_group.sprites():
                    self.laser_draw_group.add(enemy.ray)

                if enemy.ray not in self.enemy_group.sprites() and (
                    int(enemy.ray.current_image) >= 5
                ):
                    self.laser_hit_group.add(enemy.ray)

        bool_hit = bool(
            pygame.sprite.groupcollide(
                self.laser_hit_group,
                self.player_group,
                False,
                False,
                pygame.sprite.collide_mask,  # type: ignore
            )
        )

        return bool_hit

    def hp(self):
        """Update player's lives and blinking state."""
        if self.enemy_group.sprites():
            if (self.has_collision() or self.has_hit()) and not self.player_hit:
                self.player.hp -= 1
                self.player_hit = True
                self.cd_player_hit = self.time
                self.player.set_spawn()
                self.player.dead = True

            if self.player.dead:
                self.player.blink_damage()

            if (
                self.player_hit
                and self.time - self.cd_player_hit > COOLDOWN_PLAYER_IMMUNE
            ):
                self.player.dead = False
                self.player.blinking_damage = False
                self.player_hit = False
                self.player.blinking_damage = 0

    def respawn_spider(self):
        """Add a Spider."""
        self.enemy_group.add(
            LaserSpider(
                self.screen,
                self.time,
                self.autonomous,
                self.show_vision,
                self.W_enemy_matrix,
                self.b_enemy_matrix,
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
        self.player.score += 1

    def check_events(self):
        """Check game events in each frame."""
        if (
            self.time - self.cd_spawn_spider > TIME_SPAWN_SPIDER
            and len(self.enemy_group) <= MAX_SPAWN_SPIDER
        ):
            self.respawn_spider()
            self.cd_spawn_spider = self.time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self.player.keydown(event.key)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if self.autonomous:
                        self.exit = True
                    else:
                        self.exit_game()

                if event.key == pygame.K_SPACE:
                    self.player.attack()

                self.player.keyup(event.key)

    def update_score_lives(self):
        """Update player's lives and score."""
        create_text(
            self,
            "Lives = " + str(self.player.hp),
            (SCREEN_WIDTH // 10, SCREEN_HEIGHT // 8),
        )
        create_text(
            self,
            str(self.player.score),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8),
        )
        create_text(
            self,
            f"Time = {str(self.time_display)}",
            (SCREEN_WIDTH - SCREEN_WIDTH // 10, SCREEN_HEIGHT // 8),
        )

    def update_generation(self, generation, pop, max_pop):
        create_text(
            self,
            "Geneation = " + str(generation + 1),
            (SCREEN_WIDTH - SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8 * 2),
        )

        create_text(
            self,
            f"Pop = {str(pop + 1)}/{max_pop}",
            (SCREEN_WIDTH - SCREEN_WIDTH // 10, SCREEN_HEIGHT // 8 * 3),
        )

    def update_frame(self, generation, pop, max_pop):
        """Draw all elements on the screen."""
        self.screen.blit(self.background, (0, 0))
        self.time_game()

        for group in [
            self.enemy_group,
            self.player_group,
            self.laser_draw_group,
        ]:
            group.draw(self.screen)

        self.enemy_group.update(self.time, self.player, self.enemy_group)
        self.player_group.update(self.time, self.enemy_group)
        self.update_score_lives()
        if not (generation is None):
            self.update_generation(generation, pop, max_pop)

        pygame.display.update()

    def run(self, time=None, generation=None, pop=None, max_pop=None):
        """Loop each frame of the game."""
        main_menu(self)

        while self.player.hp > 0:
            self.clock.tick(CLOCK_TICK_GAME_SPEED)
            self.check_events()
            self.update_frame(generation, pop, max_pop)
            self.hp()

            if self.exit:
                break

            if not (time is None):
                if self.time_display >= time:
                    break

        if self.autonomous:
            return (
                self.time_display,
                self.player.score,
                self.player.hp,
                self.exit,
            )

        restart(self)
