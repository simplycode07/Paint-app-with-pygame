import pygame
from . import colors
from datetime import datetime

from .tools import drawing_area, Pen, Rect, Circle

def save_image():
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    pygame.image.save(drawing_area, f"{date.lower()}-image.jpg")
    print(f"image saved as - {date.lower()}-image.jpg")

def clear():
    drawing_area.fill(colors["white"])

class ToolManager:
    def __init__(self, color, size):
        self.color = color
        self.size = size

        self.tool_id = 0
        self.tools = [Pen(color, size), Rect(color, size), Circle(color, size)]
    
    # make a manager for tools which handles input and returns surface when refresh is called
    def input(self, pos, mouse_state):
        if self.tool_id == 0:
            if mouse_state[0]:
                self.tools[0].add(pos, self.color)
            elif mouse_state[2]:
                self.tools[0].add(pos, colors["white"])

            elif mouse_state == (0, 0, 0):
                self.tools[0].positions = []

        if self.tool_id == 1 or self.tool_id == 2:
            if mouse_state[0] and len(self.tools[self.tool_id].positions) == 0:
                self.tools[self.tool_id].positions.append(pos)

            if mouse_state[0] and len(self.tools[self.tool_id].positions):
                self.tools[self.tool_id].show(pos)

            # dont draw anything and clear position if the mouse did not move
            if mouse_state[0] == 0 and len(self.tools[self.tool_id].positions) == 1:
                self.tools[self.tool_id].positions = []

            if mouse_state[0] == 0 and len(self.tools[self.tool_id].positions) == 2:
                self.tools[self.tool_id].draw()

    def draw(self):
        if self.tool_id == 0:
            self.tools[0].refresh()

        return drawing_area

    def update_color(self, color):
        self.color = color
        for tool in self.tools: tool.color = color

    def update_size(self, size):
        self.size = size
        for tool in self.tools: tool.size = size

    def get_image(self, tool_id):
        if tool_id == self.tool_id:
            return self.tools[tool_id].image[1]
        else:
            return self.tools[tool_id].image[0]

