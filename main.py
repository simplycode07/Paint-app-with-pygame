import pygame
from src import settings, canvas, colors
from src.ui import UI

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")

# tools = [canvas.Pen(colors["black"], settings.default_size), canvas.Square(colors["black"], settings.default_size)]
tool_manager = canvas.ToolManager(colors["black"], 15)
tool_manager.tool_id = 0

ui = UI(tool_manager)

running = True

display.fill(colors["white"])
display.blit(ui.draw(), (0, 0))

mouse_state = (0, 0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # temporary until i figure out how i should display images of tools and selected tools
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool_manager.tool_id = 0
            if event.key == pygame.K_2:
                tool_manager.tool_id = 1
            if event.key == pygame.K_3:
                tool_manager.tool_id = 2

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
