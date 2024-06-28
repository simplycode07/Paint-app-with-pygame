import pygame
from . import settings, colors
from math import atan, sin, pi, sqrt, modf

drawing_area = pygame.Surface((settings.resolution[0], settings.resolution[1] - settings.ui_height))
drawing_area.fill(colors["white"])

def clear():
    drawing_area.fill(colors["white"])

class Pen:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size
        self.positions = []

    def add(self, pos):
        self.positions.append(pos)
        print(self.positions)

    def refresh(self, color_to_use=None):
        if not color_to_use: color_to_use = self.color

        if len(self.positions) == 1:
            rect_x = self.positions[0][0] - self.size//2
            rect_y = self.positions[0][1] - self.size//2

            pygame.draw.rect(drawing_area, color_to_use, pygame.Rect(rect_x, rect_y, self.size, self.size))

        while len(self.positions) > 1:
            dy = self.positions[0][1] - self.positions[1][1]
            dx = self.positions[0][0] - self.positions[1][0]

            if abs(dx) > self.size/2 or abs(dy) > self.size/2:
                angle = atan(dy/dx) if dx else 0
                # i wanted the size to vary between 1 and √2 from 0° to 45°
                # i need a better method for this, lerp maybe?
                adjusted_size = self.size * (1 + abs((sqrt(2)-1) * sin(2.0*angle)))

                pygame.draw.line(drawing_area, color_to_use, self.positions[0], self.positions[1], int(adjusted_size))

            # this is to remove noise like texture in small lines
            else:
                rect_x = self.positions[0][0] - self.size//2
                rect_y = self.positions[0][1] - self.size//2
                pygame.draw.rect(drawing_area, color_to_use, pygame.Rect(rect_x, rect_y, self.size, self.size))

            self.positions.pop(0)


        return drawing_area

class Square:
    def __init__(self, color) -> None:
        self.color = color

