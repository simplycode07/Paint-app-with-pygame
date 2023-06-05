import pygame
from pygame.locals import *
import random
import time

from datetime import datetime

pygame.init()
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
# basic initialisation stuff
display_size = (1000, 650)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption("Painting App with pygame")
clock = pygame.time.Clock()
font = pygame.font.Font("C:\\Windows\\Fonts\\Arial.ttf", 18)

square_selected = False

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

text = font.render("Clear screen", True, colors["black"], (255, 255, 230))
clear_butt_rect = text.get_rect()
clear_butt_rect.center = (900, 10)
display.fill(colors["white"])

def save_image():
    w = display_size[0]-30
    h = display_size[1]-20
    rect = pygame.Rect(30, 20, w, h)
    sub = display.subsurface(rect)
    screenshot = pygame.Surface((w, h))
    screenshot.blit(sub, (0, 0))
    return screenshot

def draw_sqaure(first_corner, second_corner):
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
    square_selected = False
    click_num = 0
    size = 15
    pen_color = (255, 255, 0)
    eraser_color = colors['white']
    color_button = []
    rect_pos = []
    display.blit(text, clear_butt_rect)
    colors_keys = [*colors]

    #this draws buttons for colors
    for i in range(1,len(colors)):
        color_button.append(pygame.Rect(((15*i)), 10, 10, 10))
        pygame.draw.rect(display, colors[colors_keys[i]], pygame.Rect((15*i), 10, 10, 10))

    #this draws the square tool
    square_rect = pygame.Rect(15, 25, 10, 10)
    pygame.draw.rect(display, (200, 200, 200), square_rect)
    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                print("closing")
                quit()

            if square_selected:
                if pygame.mouse.get_pressed() == (1, 0, 0) and click_num < 2:
                    click_num += 1
                    rect_pos.append(pos)
                    print(rect_pos)
                
                if click_num==2:
                    print(f"drawing square on following points, {rect_pos}")
                    click_num=0
                    first_corner = rect_pos[0] #--> (a,b)
                    second_corner = rect_pos[1] #--> (c,d)
                    # third_corner = (first_corner[0], second_corner[1]) -->(a,d)
                    # fourth_corner = (second_corner[0], first_corner[1]) -->(c,b)
                    left_x, left_y, w, h = draw_sqaure(first_corner, second_corner)
                    pygame.draw.rect(display, pen_color, pygame.Rect(left_x, left_y, w,h))
                    rect_pos = []

            if keys[pygame.K_KP_PLUS] and size < 200:
                size += 1
            if keys[pygame.K_KP_MINUS] and size != 0:
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

                    square_rect = pygame.Rect(15, 25, 10, 10)
                    pygame.draw.rect(display, (200, 200, 200), square_rect)
                    display.blit(text, clear_butt_rect)

                if not square_selected: #because if the 
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
                    print("square pressed")
                    square_selected = not square_selected
                    click_num=0
                    rect_pos=[]

                if (pos[1]-size//2) > 20 and (pos[0]-size//2) > 30 and not square_selected:
                    pygame.draw.rect(display, pen_color, pygame.Rect((pos[0]-size//2), (pos[1]-size//2), size, size))

            if pygame.mouse.get_pressed() == (0, 0, 1):
                if (pos[1]-size//2) > 20 and (pos[0]-size//2) > 30:
                    pygame.draw.rect(display, eraser_color, pygame.Rect(
                        ((pos[0]-size//2), (pos[1]-size//2), size, size)))

        pygame.display.update()
        clock.tick(240)

main()
quit()
