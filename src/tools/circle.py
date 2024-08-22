import pygame
from math import sqrt

from . import drawing_area, timeline

class Circle:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size

        self.image = [pygame.image.load(
            "img/circle.png"), pygame.image.load("img/circle_selected.png")]

        self.positions = []

    def show(self, pos):
        # first time rectangle is rendered
        if len(self.positions) == 1 and self.positions[0] != pos:
            self.old_drawing_area = pygame.Surface(drawing_area.area.get_size())
            # create copy of original drawing area
            self.old_drawing_area.blit(drawing_area.area, (0, 0))
            self.positions.append(pos)

        # replace second position if it exists
        elif len(self.positions) == 2:
            # restore drawing_area from the copy we created
            drawing_area.area.blit(self.old_drawing_area, (0, 0))
            self.positions[1] = pos

        # exit if there is only 1 element in self.positions
        # or position has not changed
        else:
            return

        center, radius = self.change_form(*self.positions)
        pygame.draw.circle(drawing_area.area, self.color, center, radius, self.size)

    def draw(self):
        center, radius = self.change_form(*self.positions)
        rect = pygame.Rect(center[0]-radius, center[1] -
                           radius, 2*radius + 1, 2*radius + 1)

        timeline.append(self.old_drawing_area, rect, 2)

        self.positions = []
        self.old_drawing_area.blit(drawing_area.area, (0, 0))

    def change_form(self, point1, point2):
        # mid point formula basic shit
        center = (((point1[0]+point2[0])//2), ((point1[1]+point2[1])//2))
        # distance formula(pythagoras)
        radius = sqrt((center[0]-point1[0])**2 + (center[1]-point1[1])**2)

        return center, radius


