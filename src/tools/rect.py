import pygame
from . import drawing_area, timeline

class Rect:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size

        self.image = [pygame.image.load(
            "img/rect.png"), pygame.image.load("img/rect_selected.png")]

        self.positions = []

    # this will render the rect but without actually changing the drawing_area
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

        rect = pygame.Rect(*self.change_form(*self.positions))
        pygame.draw.rect(drawing_area.area, self.color, rect, self.size)

    def draw(self):
        rect = pygame.Rect(*self.change_form(*self.positions))
        timeline.append(self.old_drawing_area, rect, 1)

        self.positions = []
        self.old_drawing_area.blit(drawing_area.area, (0, 0))

    def change_form(self, point1, point2):
        # first_corner --> (a,b)
        # second_corner --> (c,d)
        # third_corner = (first_corner[0], second_corner[1]) -->(a,d)
        # fourth_corner = (second_corner[0], first_corner[1]) -->(c,b)

        # note: first and second corners are diagonally opposite and so are third and fourth corners
        # did this because as from above the x value for all corners can either be a or c
        left_x = min(point1[0], point2[0])

        # similarly y values can either be b or d, so the left_top corner can be decided by taking least of a,b and c,d
        top_y = min(point1[1], point2[1])

        width = abs(point1[0] - point2[0])
        height = abs(point1[1] - point2[1])

        return (left_x, top_y, width, height)

