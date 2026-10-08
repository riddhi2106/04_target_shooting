"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70), speed=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed
        self.speed_y = speed

    def get_bounding_rect(self):
        """A square bounding box around the circle."""
        return pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)