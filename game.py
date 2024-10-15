import random

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

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

    def run(self):

        for mushroom in range(15):
            self.list_mushrooms.append(
                Entities(self, (random.randint(0, 500), random.randint(0, 400)))
            )

        running = True
        while running:

            self.display.fill((0, 0, 0))
            self.screen.blit(pygame.transform.scale(self.display, (1000, 800)), (0, 0))

            for mushroom in self.list_mushrooms:
                mushroom.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement[0] = True
                    if event.key == pygame.K_s:
                        self.movement[1] = True

            pygame.transform.scale(self.display, (1000, 800), self.screen)
            pygame.display.update()
            self.clock.tick(60)


Game().run()
