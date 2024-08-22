import pygame
from collections import deque

from . import drawing_area, timeline

class Fill:
    def __init__(self, color, size):
        self.color = color
        self.size = size

        self.image = [pygame.image.load(
            "img/fill.png"), pygame.image.load("img/fill_selected.png")]

    def draw(self, old_color, seed_position):
        if seed_position[0] < 0 or seed_position[0] > drawing_area.width:
            return drawing_area.area
        if seed_position[1] < 0 or seed_position[1] > drawing_area.height:
            return drawing_area.area

        current_color = drawing_area.area.get_at(seed_position)
        if current_color == self.color:
            return drawing_area.area

        queue = deque([seed_position])
        rect = pygame.Rect(0, 0, drawing_area.width, drawing_area.height)
        timeline.append(drawing_area.area, rect, 3)

        while queue:
            x, y = queue.popleft()
            current_color = drawing_area.area.get_at((x, y))

            if current_color != old_color or current_color == self.color:
                continue

            drawing_area.area.set_at((x, y), self.color)

            if x > 0:
                queue.append((x - 1, y))
            if x < drawing_area.width - 1:
                queue.append((x + 1, y))
            if y > 0:
                queue.append((x, y - 1))
            if y < drawing_area.height - 1:
                queue.append((x, y + 1))

