import pygame
from src import settings, canvas, colors
from src.ui import UI

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")

pen = canvas.Pen(colors["black"], 15)
ui = UI([pen])

running = True
current_tool = None

display.fill(colors["white"])
display.blit(ui.draw(), (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_state = pygame.mouse.get_pressed()

        if mouse_state[0] ^ mouse_state[2]:
            pos = list(pygame.mouse.get_pos())

            # if click is in drawing area
            if pos[1] > settings.ui_height:
                # because the surface starts from (0, ui_height) and the mouse input is with respect to origin of display 
                pos[1] -= settings.ui_height
                pen.add(pos)

            else:
                pen.color, current_tool = ui.check_input(pos, pen.color, current_tool, canvas)

        if mouse_state == (1, 0, 0):
            display.blit(pen.refresh(), (0, settings.ui_height))

        if mouse_state == (0, 0, 1):
            display.blit(pen.refresh(colors["white"]), (0, settings.ui_height))


        # clear input drawing buffer when mouse released
        if mouse_state == (0, 0, 0):
            pen.positions = []

    pygame.display.update()

pygame.quit()
