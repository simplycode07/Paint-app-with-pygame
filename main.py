import pygame
from src import settings, tools, colors
from src.ui import UI

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")

pen = tools.Pen(colors["black"], 15)
ui = UI()

running = True
current_tool = None

display.fill(colors["white"])
display.blit(ui.draw(), (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_state = pygame.mouse.get_pressed()

        if mouse_state == (1, 0, 0):
            pos = list(pygame.mouse.get_pos())
            if pos[1] > settings.ui_height:
                # because the surface starts from (0, ui_height) and the mouse input is with respect to origin of display 
                pos[1] -= settings.ui_height

                # adds position to input drawing buffer
                pen.add(pos)
            else:
                pen.color, current_tool = ui.onclick(pos, pen.color, current_tool)

        # clear input drawing buffer when mouse released
        if mouse_state == (0, 0, 0):
            pen.positions = []

    canvas = pen.refresh()
    display.blit(canvas, (0, settings.ui_height))
    pygame.display.update()

pygame.quit()
