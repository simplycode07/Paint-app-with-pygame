import pygame
import os
from . import colors, settings

# if os.name == 'posix':
#     font = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
# else:
#     font = pygame.font.Font("C://Windows//Fonts//Arial.ttf", 18)

class UI:
    def __init__(self):
        self.canvas = pygame.Surface((settings.resolution[1], settings.ui_height))
        self.canvas.fill(colors["white"])

        self.color_buttons_rect = []
        for i in range(len(colors)):
            # create rect for buttons with gaps and size defined in settings.py
            button_rect = pygame.Rect((settings.small_butt_size + settings.small_butt_gap)*i, settings.ui_start, settings.small_butt_size, settings.small_butt_size)
            self.color_buttons_rect.append(button_rect)

    def onclick(self, pos, color, tool):
        for i in range(len(self.color_buttons_rect)):
            if self.color_buttons_rect[i].collidepoint(pos):
                return ([*colors.values()][i], tool)

        return (color, tool)
        # return (color, tool_id)

    def draw(self, current_tool=None):
        for i in range(len(self.color_buttons_rect)):
            print(f"drawing {self.color_buttons_rect[i].x}")
            pygame.draw.rect(self.canvas, [*colors.values()][i], self.color_buttons_rect[i])

        return self.canvas

