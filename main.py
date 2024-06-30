import pygame
from src import settings, canvas, colors
from src.ui import UI

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")
clock = pygame.time.Clock()

# tools = [canvas.Pen(colors["black"], settings.default_size), canvas.Square(colors["black"], settings.default_size)]
tool_manager = canvas.ToolManager(colors["black"], 15)
tool_manager.tool_id = 0

ui = UI(tool_manager)

running = True

display.fill(colors["white"])
display.blit(ui.draw(), (0, 0))

mouse_state = (0, 0, 0)

redraw_ui = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            tool_manager.tool_id = 0
            redraw_ui = True
        if keys[pygame.K_2]:
            tool_manager.tool_id = 1
            redraw_ui = True
        if keys[pygame.K_3]:
            tool_manager.tool_id = 2
            redraw_ui = True

        if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and keys[pygame.K_s]:
            canvas.save_image()

        if keys[pygame.K_EQUALS] and tool_manager.size < settings.max_size:
            print("increasing size")
            tool_manager.update_size(tool_manager.size + settings.size_step)

        if keys[pygame.K_MINUS] and tool_manager.size > settings.min_size:
            tool_manager.update_size(tool_manager.size - settings.size_step)

        mouse_state = pygame.mouse.get_pressed()
        pos = list(pygame.mouse.get_pos())

        # if mouse is in drawing area
        if pos[1] > settings.ui_height:
            # because the surface starts from (0, ui_height) and the mouse input is with respect to origin of display 
            pos[1] -= settings.ui_height
            tool_manager.input(pos, mouse_state)

        elif mouse_state[0]:
            redraw_ui = ui.check_input(pos, canvas)

    if redraw_ui:
        display.blit(ui.draw(), (0, 0))

    display.blit(tool_manager.draw(), (0, settings.ui_height))
    pygame.display.update()
    clock.tick(240)

pygame.quit()
