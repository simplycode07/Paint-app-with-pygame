import pygame
from . import settings

pygame.init()

class Pen:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size
        self.canvas = pygame.Surface((settings.resolution[0], settings.resolution[1] - settings.ui_height))
        self.canvas.fill((255, 255, 255))

    def draw(self, pos):
        pygame.draw.rect(self.canvas, self.color, pygame.Rect((pos[0]-self.size//2), (pos[1]-self.size//2), self.size, self.size))
        return self.canvas
