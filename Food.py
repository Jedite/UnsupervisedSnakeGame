import pygame
import random

from Constants import *


class Food:
    def __init__(self):
        self.x = (random.randint(0, 1000) // 40) * 40
        self.y = (random.randint(0, 600) // 40) * 40

        self.WIDTH = 40
        self.HEIGHT = 40

        self.rect = None

    def draw(self, screen):
        """
        Draws food onto the screen

        :param screen: game screen to display food
        """
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

        pygame.draw.rect(screen, RED, self.rect)