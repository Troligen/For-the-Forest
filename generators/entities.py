import math
from typing import TYPE_CHECKING

from pygame import Rect, Surface

if TYPE_CHECKING:
    from ..game import Game


class Entities:
    def __init__(
        self, game: "Game", pos: list[int | float], size: tuple[int, int] = (12, 12)
    ) -> None:
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.speed = 2

    def update(self, mouse_pos: list[int]) -> None:

        dx = mouse_pos[0] - self.pos[0]
        dy = mouse_pos[1] - self.pos[1]

        length = math.sqrt(dx**2 + dy**2)

        if length > self.speed:
            normalized_dx = (dx / length) * self.speed
            normalized_dy = (dy / length) * self.speed

            self.pos[0] += normalized_dx
            self.pos[1] += normalized_dy

    def render(self, surf: Surface):
        surf.fill((255, 255, 255), Rect(self.pos, self.size))
