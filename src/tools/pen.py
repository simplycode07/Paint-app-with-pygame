import pygame
from math import atan, pi, sqrt, sin, cos

from . import drawing_area, timeline

class Pen:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size
        self.positions = []
        self.stroke_end = False

        self.image = [pygame.image.load(
            "img/pen.png"), pygame.image.load("img/pen_selected.png")]

    def add(self, pos, color=None):
        if not color:
            color = self.color

        self.positions.append((pos, color))

    def refresh(self):
        if len(self.positions) == 1:
            # self.positions is list of tuple(list, tuple)
            #                                [x, y], color

            rect_x = self.positions[0][0][0] - self.size//2
            rect_y = self.positions[0][0][1] - self.size//2

            change_rect = pygame.Rect(rect_x, rect_y, self.size, self.size)
            timeline.append(drawing_area.area, change_rect, 0)

            pygame.draw.rect(drawing_area.area, self.positions[0][1], change_rect)

        while len(self.positions) > 1:
            dy = self.positions[0][0][1] - self.positions[1][0][1]
            dx = self.positions[0][0][0] - self.positions[1][0][0]

            if abs(dx) > self.size/2 or abs(dy) > self.size/2:
                angle = atan(dy/dx) if dx else 0
                
                adjusted_size = self.size * cos(pi/4 - abs(angle)) * sqrt(2)

                change_rect = pygame.Rect(
                    *self.change_form(self.positions[0][0], self.positions[1][0], adjusted_size))
                timeline.append(drawing_area.area, change_rect, 0)

                pygame.draw.line(
                    drawing_area.area, self.positions[0][1], self.positions[0][0], self.positions[1][0], int(adjusted_size))

            # this is to remove noise like texture in small lines
            # this actually works somehow
            # ig im a genius or smth
            else:
                rect_x = self.positions[0][0][0] - self.size//2
                rect_y = self.positions[0][0][1] - self.size//2

                change_rect = pygame.Rect(rect_x, rect_y, self.size, self.size)
                timeline.append(drawing_area.area, change_rect, 0)

                pygame.draw.rect(drawing_area.area, self.positions[0][1], pygame.Rect(
                    rect_x, rect_y, self.size, self.size))

            self.stroke_end = False
            self.positions.pop(0)

        return drawing_area.area

    def change_form(self, point1, point2, adjusted_size):
        left_x = min(point1[0], point2[0]) - adjusted_size//2
        top_y = min(point1[1], point2[1]) - adjusted_size//2

        width = abs(point1[0] - point2[0]) + adjusted_size + 1
        height = abs(point1[1] - point2[1]) + adjusted_size + 1

        return (left_x, top_y, width, height)
