import random
import sys

import pygame

from generators.entities import Entities


class Game:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption("For the Forest")
        self.screen = pygame.display.set_mode((1000, 800))
        self.display = pygame.Surface((500, 400))
        self.num_mushrooms = 15
        self.list_mushrooms = []
        self.mouse_pos = []

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        for _ in range(15):
            self.list_mushrooms.append(
                Entities(self, (random.randint(0, 500), random.randint(0, 400)))
            )

    def run(self):

        while True:

            self.display.fill((0, 0, 0))
            self.screen.blit(pygame.transform.scale(self.display, (1000, 800)), (0, 0))

            for mushroom in self.list_mushrooms:
                if self.mouse_pos:
                    mushroom.set_target(self.mouse_pos)
                    mushroom.update(self.list_mushrooms)
                mushroom.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        screen_mouse_pos = pygame.mouse.get_pos()
                        self.mouse_pos = [
                            screen_mouse_pos[0] * 500 // 1000,
                            screen_mouse_pos[1] * 400 // 800,
                        ]

            pygame.transform.scale(self.display, (1000, 800), self.screen)
            pygame.display.update()
            self.clock.tick(60)


Game().run()
