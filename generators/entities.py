import math
from typing import TYPE_CHECKING, Final

from pygame import FRect, Surface, Vector2

if TYPE_CHECKING:
    from ..game import Game


class Entities:

    def __init__(
        self, game: "Game", pos: list[int | float] | tuple[int, int], size: float = 12.0
    ) -> None:
        self.game = game
        self.pos = Vector2(pos)
        self.size = size
        self.speed = 2
        self.target = None
        self.velocities = Vector2(0, 0)

    def check_collision(
        self, new_pos: Vector2, ent_list: list["Entities"]
    ) -> tuple[bool, bool]:

        new_rect = FRect(new_pos, (self.size, self.size))
        collision_x, collision_y = False, False

        for ent in ent_list:
            if ent != self:
                other_rect = ent.get_rect()
                if new_rect.colliderect(other_rect):
                    if self.pos.x < ent.pos.x:
                        collision_x = new_rect.right > other_rect.left
                    else:
                        collision_x = new_rect.left < other_rect.right

                    if self.pos.y < ent.pos.y:
                        collision_y = new_rect.bottom > other_rect.top
                    else:
                        collision_y = new_rect.top < other_rect.bottom

                    if collision_x and collision_y:
                        break

        print(f"Collision X: {collision_x}, Collision Y: {collision_y}")
        return collision_x, collision_y

    def get_rect(self):
        return FRect(self.pos, (self.size, self.size))

    def set_target(self, target_pos: tuple[int, int]):
        self.target = Vector2(target_pos)

    def update(self, ent_list: list["Entities"]) -> None:

        if self.target:
            direction = self.target - self.pos

            if direction.length() > self.speed:
                self.velocity = direction.normalize() * self.speed
            else:
                self.velocity = direction
                self.target = None

            new_pos = self.pos + self.velocity
            collision_x, collision_y = self.check_collision(new_pos, ent_list)

            if not collision_x:
                self.pos.x = new_pos.x
            else:
                self.velocity.x = 0

            if not collision_y:
                self.pos.y = new_pos.y
            else:
                self.velocity.y = 0

            if collision_x and collision_y:
                slide_x = Vector2(self.velocity.x, 0)
                slide_y = Vector2(0, self.velocity.y)

                if not self.check_collision(self.pos + slide_x, ent_list)[0]:
                    self.pos += slide_x
                elif not self.check_collision(self.pos + slide_y, ent_list)[1]:
                    self.pos += slide_y

    def render(self, surf: Surface):
        surf.fill((255, 255, 255), FRect(self.pos, (self.size, self.size)))
