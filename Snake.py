import pygame
import random

from Constants import *


class Snake:
    """
    Snake class, main sprite
    """
    def __init__(self):
        self.x = (random.randint(0, 1000) // 40) * 40
        self.y = (random.randint(0, 600) // 40) * 40

        self.WIDTH = 40
        self.HEIGHT = 40

        self.rect = None

        self.direction = [0, 0, 0, 0]

        self.snake_list = [(self.x, self.y)]

    def draw(self, screen):
        """
        Draws snake onto the screen

        :param screen: game screen to display snake
        """
        for coordinates in self.snake_list:
            self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

            pygame.draw.rect(screen, GREEN, coordinates + (self.WIDTH, self.WIDTH))

    def check_event(self, action):
        """
        Checks direction array to move in specified direction
        """
        if action == 0:
            self.direction = [0] * 4
            self.direction[0] = 1
            self.y -= SNAKE_SPEED
        elif action == 1:
            self.direction = [0] * 4
            self.direction[1] = 1
            self.y += SNAKE_SPEED
        elif action == 2:
            self.direction = [0] * 4
            self.direction[2] = 1
            self.x += SNAKE_SPEED
        elif action == 3:
            self.direction = [0] * 4
            self.direction[3] = 1
            self.x -= SNAKE_SPEED