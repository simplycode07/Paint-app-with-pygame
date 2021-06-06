import pygame
from pygame.locals import *
import random

pygame.init()

# basic initialisation stuff
display_size = (1000,650)
display = pygame.display.set_mode(display_size)
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 18)

# colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
purple = (255,0,255)
random_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
colors = [black,red,green,blue,yellow,cyan,purple,random_color]

text = font.render("Clear screen", True, black, (255,255,230))
text_rect = text.get_rect()
text_rect.center = (900, 10)
display.fill(white)

def main():
    size = 25
    pen_color = (255,255,0)
    eraser_color = white
    color_button = []
    display.blit(text, text_rect)
    for i in range(len(colors)):
        color_button.append(pygame.Rect((5+15*i), 10, 10,10))
        pygame.draw.rect(display, colors[i], pygame.Rect((5+15*i), 10, 10,10))
    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                print("closing")
                pygame.quit()
                break
            if pygame.key.get_pressed()[pygame.K_KP_PLUS] and size < 200:
                size+=1
            if pygame.key.get_pressed()[pygame.K_KP_MINUS] and size != 0:
                size-=1 
            if pygame.mouse.get_pressed() == (1,0,0):
                # for i in range(len(colors)):
                    # if color_button[i].collidepoint(pos):
                    #     color = colors[i]
                if text_rect.collidepoint(pos):
                    pygame.draw.rect(display, white, pygame.Rect(0,20,display_size[0],display_size[1]))
                if color_button[0].collidepoint(pos):
                    pen_color = colors[0]
                if color_button[1].collidepoint(pos):
                    pen_color = colors[1]
                if color_button[2].collidepoint(pos):
                    pen_color = colors[2]
                if color_button[3].collidepoint(pos):
                    pen_color = colors[3]
                if color_button[4].collidepoint(pos):
                    pen_color = colors[4]
                if color_button[5].collidepoint(pos):
                    pen_color = colors[5]
                if color_button[6].collidepoint(pos):
                    pen_color = colors[6]
                if color_button[7].collidepoint(pos):
                    pen_color = colors[7]
                if (pos[1]-size//2) > 20:
                    pygame.draw.rect(display, pen_color, pygame.Rect((pos[0]-size//2), (pos[1]-size//2), size, size))

            if pygame.mouse.get_pressed() == (0,0,1):
                if (pos[1]-size//2) > 20:
                    pygame.draw.rect(display, eraser_color, pygame.Rect(((pos[0]-size//2), (pos[1]-size//2), size, size)))
    
        pygame.display.update()
        clock.tick(240)

main()
pygame.quit()
quit()
