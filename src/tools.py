import pygame

from collections import deque
from math import atan, sqrt, sin

from . import settings, colors
from .undo import TimeLine

class DrawingArea:
    def __init__(self):
        self.area = pygame.Surface(
            (settings.resolution[0], settings.resolution[1] - settings.ui_height))
        self.area.fill(colors["white"])

        self.width = settings.resolution[0]
        self.height = settings.resolution[1] - settings.ui_height

    def resize(self, new_width, new_height):
        self.area = pygame.Surface(
            (new_width, new_height))
        self.area.fill(colors["white"])

        self.width = new_width
        self.height = new_height

drawing_area = DrawingArea()

timeline = TimeLine()

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
                # i wanted the size to vary between 1 and √2 from 0° to 45°
                # i need a better method for this, lerp maybe?
                adjusted_size = self.size * \
                    (1 + abs((sqrt(2)-1) * sin(2.0*angle)))

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


class Rect:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size

        self.image = [pygame.image.load(
            "img/rect.png"), pygame.image.load("img/rect_selected.png")]

        self.positions = []

        self.old_drawing_area = pygame.Surface(drawing_area.area.get_size())

    # this will render the rect but without actually changing the drawing_area
    def show(self, pos):
        # first time rectangle is rendered
        if len(self.positions) == 1 and self.positions[0] != pos:
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


class Circle:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size

        self.image = [pygame.image.load(
            "img/circle.png"), pygame.image.load("img/circle_selected.png")]

        self.positions = []

        self.old_drawing_area = pygame.Surface(drawing_area.area.get_size())

    def show(self, pos):
        # first time rectangle is rendered
        if len(self.positions) == 1 and self.positions[0] != pos:
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


class Fill:
    def __init__(self, color, size):
        self.color = color
        self.size = size

        self.image = [pygame.image.load(
            "img/fill.png"), pygame.image.load("img/fill_selected.png")]

    def draw(self, old_color, seed_position):
        if seed_position[0] < 0 or seed_position[0] > settings.resolution[0]:
            return drawing_area.area
        if seed_position[1] < 0 or seed_position[1] > (settings.resolution[1] - settings.ui_height):
            return drawing_area.area

        current_color = drawing_area.area.get_at(seed_position)
        if current_color == self.color:
            return drawing_area.area

        queue = deque([seed_position])
        rect = pygame.Rect(0, 0, *settings.resolution)
        timeline.append(drawing_area.area, rect, 3)

        while queue:
            x, y = queue.popleft()
            current_color = drawing_area.area.get_at((x, y))

            if current_color != old_color or current_color == self.color:
                continue

            drawing_area.area.set_at((x, y), self.color)

            if x > 0:
                queue.append((x - 1, y))
            if x < settings.resolution[0] - 1:
                queue.append((x + 1, y))
            if y > 0:
                queue.append((x, y - 1))
            if y < settings.resolution[1] - settings.ui_height - 1:
                queue.append((x, y + 1))


class Text:
    def __init__(self) -> None:
        pass
