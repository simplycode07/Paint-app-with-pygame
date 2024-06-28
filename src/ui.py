import pygame
import os
from . import colors, settings

pygame.init()
if os.name == 'posix':
    font = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
else:
    font = pygame.font.Font("C://Windows//Fonts//Arial.ttf", 18)

class UI:
    def __init__(self, tools):
        # canvas is the surface where the ui will be drawn to when draw() is called
        self.canvas = pygame.Surface((settings.resolution[0], settings.ui_height))
        self.clear()

        self.clear_button_text = font.render("Clear screen", True, colors["black"], (230, 230, 230))
        self.clear_button_rect = self.clear_button_text.get_rect()
        self.clear_button_rect.topright = (settings.resolution[0] - (settings.large_butt_gap), 10)
        
        # self.clear_button_rect = pygame.Rect(1000, 10, 40, 30)

        # this will store all the colors
        self.color_buttons = []
        for i in range(len(colors)):
            start_x = (settings.small_butt_size + settings.small_butt_gap)*i
            start_y = settings.ui_start
            button_rect = pygame.Rect(start_x, start_y, settings.small_butt_size, settings.small_butt_size)

            self.color_buttons.append(ColorButton([*colors.values()][i], button_rect))
        
        self.tool_buttons_rect = []
        for i in range(len(tools)):
            start_x = (settings.small_butt_size + settings.small_butt_gap) * (i+1)
            start_y = settings.ui_start + settings.small_butt_size + settings.small_butt_gap
            button_rect = pygame.Rect(start_x, start_y, settings.small_butt_size, settings.small_butt_size)

            self.tool_buttons_rect.append(button_rect)

        # self.clear_button_rect = pygame.Rect(settings.resolution[0] - (settings.large_butt_width + settings.large_butt_gap), settings.ui_start, settings.large_butt_width, settings.large_butt_height)
        

    def clear(self):
        print("clearing")
        self.canvas.fill(colors["white"])

    # check input
    def check_input(self, pos, color, tool, canvas):
        for button in self.color_buttons:
            if button.rect.collidepoint(pos):
                return (button.color, tool)
        
        if self.clear_button_rect.collidepoint(pos):
            self.clear()
            self.draw()
            canvas.clear()

        return (color, tool)
        # return (color, tool_id)

    def draw(self, current_tool=None):

        for button in self.color_buttons:
            print(f"drawing {button.rect.x}")
            pygame.draw.rect(self.canvas, button.color, button.rect)

        self.canvas.blit(self.clear_button_text, self.clear_button_rect)

        return self.canvas


class ColorButton:
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect
