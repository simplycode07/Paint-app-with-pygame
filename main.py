import pygame
from src import settings, canvas, colors
from src.ui import UI

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")

# tools = [canvas.Pen(colors["black"], settings.default_size), canvas.Square(colors["black"], settings.default_size)]
tool_manager = canvas.ToolManager(colors["black"], 15)
tool_manager.tool_id = 1

ui = UI(tool_manager)

running = True

display.fill(colors["white"])
display.blit(ui.draw(), (0, 0))

mouse_state = (0, 0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_state = pygame.mouse.get_pressed()

        pos = list(pygame.mouse.get_pos())

        # if mouse is in drawing area
        if pos[1] > settings.ui_height:
            # because the surface starts from (0, ui_height) and the mouse input is with respect to origin of display 
            pos[1] -= settings.ui_height
            tool_manager.input(pos, mouse_state)

        elif mouse_state[0]:
            ui.check_input(pos, canvas)

    display.blit(tool_manager.draw(), (0, settings.ui_height))

    pygame.display.update()

pygame.quit()
