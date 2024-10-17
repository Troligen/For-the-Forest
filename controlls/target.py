from pygame import Rect, Surface, draw
from pygame.math import Vector2


class Cursor:
    def __init__(self, start_pos: Vector2 = Vector2(0, 0), draw: bool = False):
        self.start_pos = start_pos
        self.draw = draw

    def rect(self, end_pos: Vector2):
        return Rect(self.start_pos, end_pos - self.start_pos)

    def render(self, sur: Surface, end_pos: Vector2):
        draw.rect(sur, (255, 0, 0), self.rect(end_pos), 1)
