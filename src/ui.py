import pygame
import os
from . import colors, settings

pygame.init()
if os.name == 'posix':
    font = pygame.font.Font("/usr/share/fonts/TTF/DejaVuSans.ttf", 18)
else:
    font = pygame.font.Font("C://Windows//Fonts//Arial.ttf", 18)

def inverse_color(color):
    inv_color = [0, 0, 0]
    
    for i in range(3):
        inv_color[i] = 255 - color[i]

    return tuple(inv_color)

class UI:
    def __init__(self, tool_manager):
        # canvas is the surface where the ui will be drawn to when draw() is called
        self.width = settings.resolution[0]
        self.height = settings.ui_height
        self.canvas = pygame.Surface((self.width, self.height))
        self.clear()

        self.tool_manager = tool_manager

        # color at 1 is black
        self.selected_color_id = 1

        self.clear_button_text = font.render("Clear screen", True, colors["black"], (230, 230, 230))
        
        self.place_buttons()


    def resized(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        self.canvas = pygame.Surface((self.width, self.height))
    
        self.clear()
        self.place_buttons()
        self.draw()

    def clear(self):
        print("clearing")
        self.canvas.fill(colors["white"])

    # returns if ui is to be redrawn or not
    def check_input(self, pos, canvas):
        for i, button in enumerate(self.color_buttons):
            if button.rect.collidepoint(pos):
                self.selected_color_id = i
                self.tool_manager.update_color(button.color)
                self.clear()
                self.draw()

                return True
        
        for i, button_rect in enumerate(self.tool_buttons_rect):
            if button_rect.collidepoint(pos):
                self.tool_manager.change_tool(i)
                self.clear()
                self.draw()

                return True

        if self.clear_button_rect.collidepoint(pos):
            self.clear()
            self.draw()
            canvas.clear()
            
            return True
        
        return False

    def draw(self):
        for i, button in enumerate(self.color_buttons):
            # increase size of buttons when selected
            if i == self.selected_color_id:
                rect = button.rect.copy()
                rect.width += settings.color_standout_px 
                rect.height += settings.color_standout_px 
                
                rect.center = button.rect.center

                pygame.draw.rect(self.canvas, button.color, rect)

            pygame.draw.rect(self.canvas, button.color, button.rect)

        for i, button_rect in enumerate(self.tool_buttons_rect):
            image = self.tool_manager.get_image(i)
            self.canvas.blit(pygame.transform.scale(image, button_rect.size), button_rect)

        self.canvas.blit(self.clear_button_text, self.clear_button_rect)

        return self.canvas

    def place_buttons(self):
        self.clear_button_rect = self.clear_button_text.get_rect()
        self.clear_button_rect.topright = (self.width - (settings.large_butt_gap), 10)
        
        # self.clear_button_rect = pygame.Rect(1000, 10, 40, 30)

        # this will store all the colors
        self.color_buttons = []
        for i in range(len(colors)):
            start_x = (settings.small_butt_size + settings.small_butt_gap)*i
            start_y = settings.ui_start
            button_rect = pygame.Rect(start_x, start_y, settings.small_butt_size, settings.small_butt_size)

            self.color_buttons.append(ColorButton([*colors.values()][i], button_rect))
        
        self.tool_buttons_rect = []
        for i in range(len(self.tool_manager.tools)):
            start_x = (settings.small_butt_size + settings.small_butt_gap) * (i+1)
            start_y = settings.ui_start + settings.small_butt_size + settings.small_butt_gap
            button_rect = pygame.Rect(start_x, start_y, settings.small_butt_size, settings.small_butt_size)

            self.tool_buttons_rect.append(button_rect)

class ColorButton:
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect
