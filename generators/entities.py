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
        self.max_speed = 2
        self.max_force = 0.1
        self.target = None
        self.velocity = Vector2(0, 0)

    def check_collision(self, new_pos: Vector2, ent_list: list["Entities"]) -> bool:

        new_rect = FRect(new_pos.x, new_pos.y, self.size, self.size)
        for ent in ent_list:
            if ent != self and new_rect.colliderect(ent.get_rect()):
                return True
        return False

    def get_rect(self):
        return FRect(self.pos, (self.size, self.size))

    def set_target(self, target_pos: tuple[int, int]):
        self.target = Vector2(target_pos)

    def seek(self, target: Vector2) -> Vector2:
        desired = target - self.pos
        if desired.length() > 0:
            desired = desired.normalize() * self.max_speed
        return desired - self.velocity

    def avoid_obstacles(self, ent_list: list["Entities"]) -> Vector2:
        if self.velocity.length() != 0:
            ahead = self.pos + self.velocity.normalize() * 30  # Look ahead
        else:
            ahead = self.pos * 30
        avoidance = Vector2(0, 0)
        for ent in ent_list:
            if ent != self:
                to_obstacle = ent.pos - self.pos
                dist = to_obstacle.length()
                if dist < 50:  # Detection radius
                    if ahead.distance_to(ent.pos) <= self.size + ent.size:
                        avoidance -= to_obstacle.normalize()
        return (
            avoidance.normalize() * self.max_force
            if avoidance.length() > 0
            else avoidance
        )

    def update(self, ent_list: list["Entities"]) -> None:

        if self.target:
            steering = Vector2(0, 0)

            steering += self.seek(self.target)

            steering += self.avoid_obstacles(ent_list) * 1.5

            if steering.length() > self.max_force:
                steering = steering.normalize() * self.max_force

            self.velocity += steering
            if self.velocity.length() > self.max_speed:
                self.velocities = self.velocity.normalize() * self.max_speed

            new_pos = self.pos + self.velocity
            if not self.check_collision(new_pos, ent_list):
                self.pos = new_pos
            else:
                # If collision, try to slide along the collision
                new_pos_x = Vector2(new_pos.x, self.pos.y)
                new_pos_y = Vector2(self.pos.x, new_pos.y)

                if not self.check_collision(new_pos_x, ent_list):
                    self.pos = new_pos_x
                    self.velocity.y = 0
                elif not self.check_collision(new_pos_y, ent_list):
                    self.pos = new_pos_y
                    self.velocity.x = 0
                else:
                    self.velocity = Vector2(0, 0)  # Stop if can't move in any direction

            if self.pos.distance_to(self.target) < self.max_speed:
                self.target = None
                self.velocity = Vector2(0, 0)

    def render(self, surf: Surface):
        surf.fill((255, 255, 255), self.get_rect())
