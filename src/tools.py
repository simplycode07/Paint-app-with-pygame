import pygame
from . import settings, colors


canvas = pygame.Surface((settings.resolution[0], settings.resolution[1] - settings.ui_height))
canvas.fill(colors.white)

class Pen:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size
        self.positions = []

    def add(self, pos):
        self.positions.append(pos)
        print(self.positions)

    def refresh(self):
        while len(self.positions) > 1:
            pygame.draw.line(canvas, self.color, self.positions[0], self.positions[1], self.size)
            self.positions.pop(0)

        if len(self.positions):
            rect_x = self.positions[0][0] - self.size//2
            rect_y = self.positions[0][1] - self.size//2

            pygame.draw.rect(canvas, self.color, pygame.Rect(rect_x, rect_y, self.size, self.size))
        
        return canvas

