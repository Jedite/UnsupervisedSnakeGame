import pygame
from pygame.locals import *
import sys

from Constants import *


class Menu:
    def __init__(self):
        pygame.init()

        self.reset()

    def reset(self):
        """
        Reset command
        """
        self.running = True
        self.SCREEN = pygame.display.set_mode(WINDOW_SIZE)

    def menu_loop(self):
        """
        Main menu loop
        """
        break_point = 0
        self.running = True
        while self.running:
            pygame.display.update()
            self.SCREEN.fill(BLACK)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    break_point = 1

            if break_point == 1:
                self.running = False