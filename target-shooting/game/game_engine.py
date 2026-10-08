"""
GameEngine: owns the targets and handles player clicks.
"""

import random
import pygame

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
POINTS_PER_COMBO = 10
ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.start_round()

    def start_round(self):
        self.targets = [self._random_target(i) for i in range(NUM_TARGETS)]
        self.score = 0
        self.combo = 0
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = ROUND_DURATION
        self.round_over = False

    def _random_target(self, index=0):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        speed = 2 if index % 2 == 0 else 4

        return Target(x, y, radius=TARGET_RADIUS, speed=speed)

    def handle_click(self, pos):
        if self.round_over:
            return

        target = check_hit(self.targets, pos)

        if target is not None:
            self.combo += 1
            self.score += POINTS_PER_COMBO * self.combo

            self.targets.remove(target)
            self.targets.append(self._random_target(len(self.targets)))
        else:
            self.combo = 0

    def update(self):
        if self.round_over:
            return

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_remaining = max(0, ROUND_DURATION - elapsed)

        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.round_over = True
            return

        for target in self.targets:
            target.x += target.speed_x
            target.y += target.speed_y

            if target.x - target.radius <= 0:
                target.x = target.radius
                target.speed_x *= -1
            elif target.x + target.radius >= WIDTH:
                target.x = WIDTH - target.radius
                target.speed_x *= -1

            if target.y - target.radius <= 0:
                target.y = target.radius
                target.speed_y *= -1
            elif target.y + target.radius >= HEIGHT:
                target.y = HEIGHT - target.radius
                target.speed_y *= -1

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}  Combo: x{self.combo}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {self.time_remaining:.1f}s",
            (10, 40)
        )

        if self.round_over:
            renderer.draw_banner(
                surface,
                font,
                f"TIME'S UP! Final Score: {self.score} | Press R to restart"
            )