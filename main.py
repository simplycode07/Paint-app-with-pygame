import pygame
from src import settings, tools, colors

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")
pen = tools.Pen(colors.black, 15)

running = True

display.fill(colors.white)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed() == (1, 0, 0):
            pos = list(pygame.mouse.get_pos())
            if pos[1] > settings.ui_height:
                # because the surface starts from (0, ui_height) and the mouse input is with respect to origin of display 
                pos[1] -= settings.ui_height
                pen.add(pos)

    canvas = pen.refresh()
    display.blit(canvas, (0, settings.ui_height))
    pygame.display.flip()

pygame.quit()
