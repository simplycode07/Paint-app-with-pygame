import pygame
from src import settings, canvas, colors
from src.ui import UI

pygame.init()

display = pygame.display.set_mode(settings.resolution)
pygame.display.set_caption("brr")
clock = pygame.time.Clock()

tool_manager = canvas.ToolManager(colors["black"], settings.default_size)
tool_manager.tool_id = 0

ui = UI(tool_manager)

running = True

display.fill(colors["white"])
display.blit(ui.draw(), (0, 0))

mouse_state = (0, 0, 0)

tool_shortcuts = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]

while running:
    redraw_ui = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        mod = pygame.key.get_mods()

        for tool_id, shortcut_key in enumerate(tool_shortcuts):
            if keys[shortcut_key]:
                tool_manager.tool_id = tool_id
                redraw_ui = True

        if event.type == pygame.KEYDOWN:
            for tool_id, shortcut_key in enumerate(tool_shortcuts):
                if event.key == shortcut_key:
                    tool_manager.tool_id = tool_id
                    redraw_ui = True

            if event.key == pygame.K_EQUALS and tool_manager.size < settings.max_size:
                print("increasing size")
                tool_manager.update_size(
                    tool_manager.size + settings.size_step)

            if event.key == pygame.K_MINUS and tool_manager.size > settings.min_size:
                tool_manager.update_size(
                    tool_manager.size - settings.size_step)

            # event with ctrl modifier
            if event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_s:
                    canvas.save_image()
                if event.key == pygame.K_z:
                    tool_manager.undo()
                if event.key == pygame.K_y:
                    tool_manager.redo()

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
