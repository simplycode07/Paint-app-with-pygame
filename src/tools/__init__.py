import pygame

from src import settings, colors
from src.undo import TimeLine


class DrawingArea:
    def __init__(self):
        self.area = pygame.Surface(
            (settings.resolution[0], settings.resolution[1] - settings.ui_height))
        self.area.fill(colors["white"])

        self.width = settings.resolution[0]
        self.height = settings.resolution[1] - settings.ui_height

    def resized(self, new_width, new_height):
        old_area = self.area
        self.area = pygame.Surface(
            (new_width, new_height))
        self.area.fill(colors["white"])
        self.area.blit(old_area, (0, 0))

        self.width = new_width
        self.height = new_height

drawing_area = DrawingArea()
timeline = TimeLine()

from .pen import Pen
from .rect import Rect
from .circle import Circle
from .fill import Fill
from .selection_window import Image

__all__ = ['Pen', 'Rect', 'Circle', 'Fill', 'drawing_area', 'timeline', 'Image']
