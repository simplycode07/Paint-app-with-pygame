import pygame
from . import settings, colors
from math import atan, sin, sqrt

drawing_area = pygame.Surface((settings.resolution[0], settings.resolution[1] - settings.ui_height))
drawing_area.fill(colors["white"])

def clear():
    drawing_area.fill(colors["white"])

class ToolManager:
    def __init__(self, color, size):
        self.color = color
        self.size = size

        self.tool_id = 0
        self.tools = [Pen(color, size), Rect(color, size)]
    
    # make a manager for tools which handles input and returns surface when refresh is called
    def input(self, pos, mouse_state):
        if self.tool_id == 0:
            if mouse_state[0]:
                self.tools[0].add(pos, self.color)
            elif mouse_state[2]:
                self.tools[0].add(pos, colors["white"])

            elif mouse_state == (0, 0, 0):
                self.tools[0].positions = []

        if self.tool_id == 1:
            if mouse_state[0] and len(self.tools[1].positions) == 0:
                self.tools[1].positions.append(pos)

            if mouse_state[0] and len(self.tools[1].positions):
                self.tools[1].show(pos)

            if mouse_state[0] == 0 and len(self.tools[1].positions) == 1:
                self.tools[1].positions = []

            if mouse_state[0] == 0 and len(self.tools[1].positions) == 2:
                self.tools[1].draw()

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

class Pen:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size
        self.positions = []

    def add(self, pos, color=None):
        if not color: color = self.color

        self.positions.append((pos, color))

    def refresh(self):
        if len(self.positions) == 1:
            # self.positions is list of tuple(list, tuple)
            #                                [x, y], color
            rect_x = self.positions[0][0][0] - self.size//2
            rect_y = self.positions[0][0][1] - self.size//2

            pygame.draw.rect(drawing_area, self.positions[0][1], pygame.Rect(rect_x, rect_y, self.size, self.size))

        while len(self.positions) > 1:
            dy = self.positions[0][0][1] - self.positions[1][0][1]
            dx = self.positions[0][0][0] - self.positions[1][0][0]

            if abs(dx) > self.size/2 or abs(dy) > self.size/2:
                angle = atan(dy/dx) if dx else 0
                # i wanted the size to vary between 1 and √2 from 0° to 45°
                # i need a better method for this, lerp maybe?
                adjusted_size = self.size * (1 + abs((sqrt(2)-1) * sin(2.0*angle)))

                pygame.draw.line(drawing_area, self.positions[0][1], self.positions[0][0], self.positions[1][0], int(adjusted_size))

            # this is to remove noise like texture in small lines
            else:
                rect_x = self.positions[0][0][0] - self.size//2
                rect_y = self.positions[0][0][1] - self.size//2
                pygame.draw.rect(drawing_area, self.positions[0][1], pygame.Rect(rect_x, rect_y, self.size, self.size))

            self.positions.pop(0)
        return drawing_area

class Rect:
    def __init__(self, color, size) -> None:
        self.color = color
        self.size = size
        
        self.positions = []

        self.old_drawing_area = pygame.Surface(drawing_area.get_size())

    # this will render the square but without actually changing the drawing_area
    def show(self, pos):
        # first time rectangle is rendered
        if len(self.positions) == 1:
            # create copy of original drawing area
            self.old_drawing_area.blit(drawing_area, (0, 0))
            self.positions.append(pos)

        # replace second position if it exists
        elif len(self.positions) == 2:
            # restore drawing_area from the copy we created
            drawing_area.blit(self.old_drawing_area, (0, 0))
            self.positions[1] = pos
        else:
            print("i did a fucky wucky")

        print(self.positions)

        rect = pygame.Rect(*self.change_form(*self.positions))
        pygame.draw.rect(drawing_area, self.color, rect, self.size)
    
    def draw(self):
        self.positions = []
        self.old_drawing_area.blit(drawing_area, (0, 0))
    
    def change_form(self, point1, point2):
        # first_corner --> (a,b)
        # second_corner --> (c,d)
        # third_corner = (first_corner[0], second_corner[1]) -->(a,d)
        # fourth_corner = (second_corner[0], first_corner[1]) -->(c,b)

        # note: first and second corners are diagonally opposite and so are third and fourth corners
        #did this because as from above the x value for all corners can either be a or c
        left_x = min(point1[0], point2[0])

        #similarly y values can either be b or d, so the left_top corner can be decided by taking least of a,b and c,d
        top_y = min(point1[1], point2[1])

        width = abs(point1[0] - point2[0]) 
        height = abs(point1[1] - point2[1]) 

        return (left_x, top_y, width, height)


        


