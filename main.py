import pygame
from pygame.locals import *
import random

from math import sqrt
from datetime import datetime

pygame.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
# basic initialisation stuff
display_size = (1000, 650)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption("Painting App with pygame")
clock = pygame.time.Clock()
font = pygame.font.Font("C:\\Windows\\Fonts\\Arial.ttf", 18)

# colors
colors = {
    "white": (255, 255, 255),
    "black":(0,0,0),
    "red":(255,0,0),
    "green":(0,255,0),
    "blue":(0,0,255),
    "yellow":(255,255,0),
    "cyan":(0, 255, 255),
    "purple":(255, 0, 255),
    "rand_col":(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
}

clear_butt_text = font.render("Clear screen", True, colors["black"], (255, 255, 230))
clear_butt_rect = clear_butt_text.get_rect()
clear_butt_rect.center = (900, 10)

square_selected_true = pygame.image.load('img\\square_selected_true.png')
square_selected_false = pygame.image.load('img\\square_selected_false.png')
circle_selected_true = pygame.image.load('img\\circle_selected_true.png')
circle_selected_false = pygame.image.load('img\\circle_selected_false.png')

display.fill(colors["white"])

def save_image():
    w = display_size[0]
    h = display_size[1]-35 #canvas starts from (0,35)
    rect = pygame.Rect(0, 35, w, h)
    sub = display.subsurface(rect)
    screenshot = pygame.Surface((w, h))
    screenshot.blit(sub, (0, 0))
    return screenshot

def draw_square(first_corner, second_corner):
    # first_corner = rect_pos[0] --> (a,b)
    # second_corner = rect_pos[1] --> (c,d)
    # third_corner = (first_corner[0], second_corner[1]) -->(a,d)
    # fourth_corner = (second_corner[0], first_corner[1]) -->(c,b)

    # note: first and second corners are diagonally opposite and so are third and fourth corners
    #did this because as from above the x value for all corners can either be a or c
    if first_corner[0] < second_corner[0]:
        left_x = first_corner[0]
    else:
        left_x = second_corner[0]

    #similarly y values can either be b or d, so the left_top corner can be decided by taking least of a,b and c,d
    if first_corner[1]<second_corner[1]:
        left_y = first_corner[1]
    else:
        left_y = second_corner[1]

    w = abs(first_corner[0] - second_corner[0]) # width will be the difference of x coordinates of the two opposite points
    h = abs(first_corner[1] - second_corner[1]) # same thing with the height
    return left_x,left_y,w,h

def main():
    tool_selected = [0,0]
    click_num = 0
    size = 15
    pen_color = colors['black']
    eraser_color = colors['white']
    color_button = []
    rect_pos = []
    display.blit(clear_butt_text, clear_butt_rect)
    colors_keys = [*colors]

    #this draws buttons for colors
    for i in range(1,len(colors)):
        color_button.append(pygame.Rect(((15*i)), 10, 10, 10))
        pygame.draw.rect(display, colors[colors_keys[i]], pygame.Rect((15*i), 10, 10, 10))

    #this draws the square tool, (15,25)
    square_rect = pygame.Rect(15, 25, 10, 10)
    circle_rect = pygame.Rect(30, 25, 10, 10)
    display.blit(square_selected_false, square_rect)
    display.blit(circle_selected_false, circle_rect)

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                print("closing")
                quit()

            if True in tool_selected: #drawing with tools
                if pygame.mouse.get_pressed() == (1, 0, 0) and click_num < 2 and pos[1] > 35:
                    click_num += 1
                    rect_pos.append(pos)
                
                if click_num==2:
                    click_num=0
                    first_corner = rect_pos[0] #--> (a,b)
                    second_corner = rect_pos[1] #--> (c,d)

                    if tool_selected[0]: # this draws rectangle
                        left_x, left_y, w, h = draw_square(first_corner, second_corner)
                        pygame.draw.rect(display, pen_color, pygame.Rect(left_x, left_y, w,h), size)

                    if tool_selected[1]: # this draws circle
                        center = (((first_corner[0]+second_corner[0])//2), ((first_corner[1]+second_corner[1])//2))#mid point formula basic shit
                        radius = sqrt((center[0]-first_corner[0])**2 + (center[1]-first_corner[1])**2) # distance formula(pythagoras)
                        pygame.draw.circle(display, pen_color, center, radius, size)

                    rect_pos = []

            if keys[pygame.K_KP_PLUS] and size < 200: #changing size of pen
                size += 1
            if keys[pygame.K_KP_MINUS] and size > 5:
                size -= 1
            if (keys[pygame.K_LCTRL] and keys[pygame.K_s]) or (keys[pygame.K_RCTRL] and keys[pygame.K_s]):
                image = save_image()
                date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                pygame.image.save(image, f"{date.lower()}-image.jpg")

            if pygame.mouse.get_pressed() == (1, 0, 0):
                if clear_butt_rect.collidepoint(pos): #draws a white rectangle all over the screen and then redraws all the buttons
                    pygame.draw.rect(display, colors['white'], pygame.Rect(0,0, display_size[0], display_size[1]))
                    for i in range(1,len(colors)):
                        pygame.draw.rect(display, colors[colors_keys[i]], pygame.Rect((15*i), 10, 10, 10))

                    if tool_selected[0]:
                        display.blit(square_selected_true, square_rect)
                    else:
                        display.blit(square_selected_false, square_rect)
                    
                    if tool_selected[1]:
                        display.blit(circle_selected_true, circle_rect)
                    else:
                        display.blit(circle_selected_false, circle_rect)

                    display.blit(clear_butt_text, clear_butt_rect)

                if not True in tool_selected:
                    if color_button[0].collidepoint(pos):
                        pen_color = colors['black']
                    elif color_button[1].collidepoint(pos):
                        pen_color = colors['red']
                    elif color_button[2].collidepoint(pos):
                        pen_color = colors['green']
                    elif color_button[3].collidepoint(pos):
                        pen_color = colors['blue']
                    elif color_button[4].collidepoint(pos):
                        pen_color = colors['yellow']
                    elif color_button[5].collidepoint(pos):
                        pen_color = colors['cyan']
                    elif color_button[6].collidepoint(pos):
                        pen_color = colors['purple']
                    elif color_button[7].collidepoint(pos):
                        pen_color = colors['rand_col']

                if square_rect.collidepoint(pos):
                    print("click on the diagonally opposite ends of the rectangle you want to draw")                
                    for i in range(len(tool_selected)):
                        if i != 0:
                            tool_selected[i]=0
                        else:
                            tool_selected[i] = not tool_selected[i]
                    click_num = 0
                    rect_pos = []                    
                    if tool_selected[0]:
                        display.blit(square_selected_true, square_rect)
                    else:
                        display.blit(square_selected_false, square_rect)
                    display.blit(circle_selected_false, circle_rect)
                if circle_rect.collidepoint(pos):
                    print("click on diametrically opposite points of the circle you want to draw")
                    for i in range(len(tool_selected)):
                        if i != 1:
                            tool_selected[i] = 0
                        else:
                            tool_selected[i] = not tool_selected[i]
                    click_num = 0
                    rect_pos = []
                    if tool_selected[1]:
                        display.blit(circle_selected_true, circle_rect)
                    else:
                        display.blit(circle_selected_false, circle_rect)
                    display.blit(square_selected_false, square_rect)

                if (pos[1]-size//2) > 35 and not True in tool_selected:
                    pygame.draw.rect(display, pen_color, pygame.Rect((pos[0]-size//2), (pos[1]-size//2), size, size))

            if pygame.mouse.get_pressed() == (0, 0, 1):
                if (pos[1]-size//2) > 20 and (pos[0]-size//2) > 30:
                    pygame.draw.rect(display, eraser_color, pygame.Rect(
                        ((pos[0]-size//2), (pos[1]-size//2), size, size)))

        pygame.display.update()
        clock.tick(240)

main()
quit()
