import pygame

from . import colors
from datetime import datetime

from .tools import *


def save_image():
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    pygame.image.save(drawing_area.area, f"{date.lower()}-image.jpg")
    print(f"image saved as - {date.lower()}-image.jpg")


def clear():
    drawing_area.area.fill(colors["white"])
    timeline.reset()


class ToolManager:
    def __init__(self, color, size):
        self.color = color
        self.size = size

        self.tool_id = 0
        self.tools = [Pen(color, size), Rect(color, size),
                      Circle(color, size), Fill(color, size), Image()]

    # make a manager for tools which handles input and returns surface when refresh is called
    def input(self, pos, mouse_state):
        if self.tool_id == 0:
            if mouse_state[0]:
                self.tools[0].add(pos, self.color)
            elif mouse_state[2]:
                self.tools[0].add(pos, colors["white"])

            elif mouse_state == (0, 0, 0):
                self.tools[0].positions = []
                timeline.end_stroke()

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

        if self.tool_id == 3:
            if mouse_state[0]:
                old_color = drawing_area.area.get_at(pos)
                self.tools[3].draw(old_color, pos)

        if self.tool_id == 4:
            if mouse_state[0] and not self.tools[4].img:
                self.tools[4].start()

    def draw(self):
        if self.tool_id == 0:
            self.tools[0].refresh()

        return drawing_area.area

    def undo(self):
        timeline.undo(drawing_area.area)

    def redo(self):
        timeline.redo(drawing_area.area)

    def update_color(self, color):
        self.color = color
        for tool in self.tools:
            tool.color = color

    def update_size(self, size):
        self.size = size
        for tool in self.tools:
            tool.size = size

    def get_image(self, tool_id):
        if tool_id == self.tool_id:
            return self.tools[tool_id].image[1]
        else:
            return self.tools[tool_id].image[0]

    def change_tool(self, new_tool_id):
        self.tool_id = new_tool_id
