from typing import TYPE_CHECKING

from pygame import Rect, Surface

if TYPE_CHECKING:
    from ..game import Game


class Entities:
    def __init__(
        self, game: "Game", pos: tuple[int, int], size: tuple[int, int] = (12, 12)
    ) -> None:
        self.game = game
        self.pos = pos
        self.size = size

    def update(self, movement: tuple[int, int]):
        pass

    def render(self, surf: Surface):
        surf.fill((255, 255, 255), Rect(self.pos, self.size))
